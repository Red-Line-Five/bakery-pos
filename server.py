import http.server
import json
import os
import sys
import webbrowser
import threading
import time
import socket
from urllib.parse import urlparse

PORT = 5050
DATA_FILE = 'data.json'
SETTINGS_FILE = 'settings.json'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DEFAULT_DATA = {
    "invoices": [],
    "settlements": [],
    "masarif": [],
    "orderNum": 0
}

DEFAULT_SETTINGS = {
    "bakery": "Forn Al Asli",
    "whatsapp_owner": "",
    "rate": 90000,
    "adminPass": "1234",
    "deliveryFee": 0,
    "gsheetUrl": "",
    "extras": [],
    "extraRules": {"categories": {}, "types": {}},
    "products": []
}


def read_json(filename, default):
    path = os.path.join(BASE_DIR, filename)
    if not os.path.exists(path):
        write_json(filename, dict(default))
        return dict(default)
    try:
        with open(path, 'r', encoding='utf-8-sig') as f:
            result = json.load(f)
            return result
    except Exception as e:
        print('  WARNING: could not read ' + filename + ': ' + str(e))
        return dict(default)


def write_json(filename, data):
    path = os.path.join(BASE_DIR, filename)
    tmp = path + '.tmp'
    try:
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        if os.path.exists(path):
            os.replace(tmp, path)
        else:
            os.rename(tmp, path)
    except Exception as e:
        print('  ERROR writing ' + filename + ': ' + str(e))


class Handler(http.server.SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def log_message(self, format, *args):
        if len(args) > 0 and '/api/' in str(args[0]):
            status = args[1] if len(args) > 1 else '?'
            print('  [' + str(status) + '] ' + str(args[0]))

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == '/api/data':
            self._json(read_json(DATA_FILE, DEFAULT_DATA))
            return

        if parsed.path == '/api/settings':
            self._json(read_json(SETTINGS_FILE, DEFAULT_SETTINGS))
            return

        super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length)

        try:
            payload = json.loads(body.decode('utf-8'))
        except Exception:
            self._error('Invalid JSON')
            return

        if parsed.path == '/api/data':
            # Save only transactional data
            data_to_save = {
                'invoices':    payload.get('invoices', []),
                'settlements': payload.get('settlements', []),
                'masarif':     payload.get('masarif', []),
                'orderNum':    payload.get('orderNum', 0)
            }
            write_json(DATA_FILE, data_to_save)
            self._json({'ok': True})
            return

        if parsed.path == '/api/settings':
            # Save only settings/config data
            settings_to_save = {
                'bakery':        payload.get('bakery', ''),
                'whatsapp_owner':payload.get('whatsapp_owner', ''),
                'rate':          payload.get('rate', 90000),
                'adminPass':     payload.get('adminPass', '1234'),
                'deliveryFee':   payload.get('deliveryFee', 0),
                'gsheetUrl':     payload.get('gsheetUrl', ''),
                'extras':        payload.get('extras', []),
                'extraRules':    payload.get('extraRules', {'categories': {}, 'types': {}}),
                'products':      payload.get('products', [])
            }
            write_json(SETTINGS_FILE, settings_to_save)
            self._json({'ok': True})
            return

        self._error('Unknown endpoint')

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def _json(self, data):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', len(body))
        self._cors()
        self.end_headers()
        self.wfile.write(body)

    def _error(self, msg):
        body = json.dumps({'error': msg}).encode('utf-8')
        self.send_response(400)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(body))
        self._cors()
        self.end_headers()
        self.wfile.write(body)

    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')


def open_browser():
    time.sleep(1.2)
    webbrowser.open('http://localhost:' + str(PORT) + '/bakery-pos.html')


if __name__ == '__main__':
    os.chdir(BASE_DIR)

    # Check if port already in use
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    in_use = sock.connect_ex(('localhost', PORT)) == 0
    sock.close()

    if in_use:
        print('')
        print('  Server already running on port ' + str(PORT))
        print('  Opening browser...')
        webbrowser.open('http://localhost:' + str(PORT) + '/bakery-pos.html')
        input('  Press Enter to exit...')
        sys.exit(0)

    # Verify required files exist
    html_path = os.path.join(BASE_DIR, 'bakery-pos.html')
    if not os.path.exists(html_path):
        print('')
        print('  ERROR: bakery-pos.html not found in:')
        print('  ' + BASE_DIR)
        print('  Make sure all files are in the same folder.')
        input('  Press Enter to exit...')
        sys.exit(1)

    # Start browser in background thread
    threading.Thread(target=open_browser, daemon=True).start()

    print('')
    print('  POS Server - Forn Al Asli')
    print('  http://localhost:' + str(PORT))
    print('  Keep this window open while using POS.')
    print('  Press Ctrl+C to stop.')
    print('')

    try:
        server = http.server.HTTPServer(('localhost', PORT), Handler)
        server.serve_forever()
    except KeyboardInterrupt:
        print('')
        print('  Server stopped.')
        sys.exit(0)
    except Exception as e:
        print('')
        print('  ERROR: ' + str(e))
        input('  Press Enter to exit...')
        sys.exit(1)
