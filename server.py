import http.server
import json
import os
import sys
import webbrowser
import threading
import time
import socket
from urllib.parse import urlparse
from urllib.request import urlopen
from urllib.error import URLError

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


def read_license_from_registry():
    if os.name != 'nt':
        return None
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\AsliPOS")
        license_key = winreg.QueryValueEx(key, "LicenseKey")[0]
        license_expiry = winreg.QueryValueEx(key, "LicenseExpiry")[0]
        winreg.CloseKey(key)
        return {
            "licenseKey": str(license_key).strip().upper(),
            "licenseExpiry": str(license_expiry).strip()
        }
    except Exception:
        return None


def read_license_config():
    env_key = os.environ.get('ASLI_LICENSE_KEY', '').strip().upper()
    env_expiry = os.environ.get('ASLI_LICENSE_EXPIRY', '').strip()
    if env_key and env_expiry:
        return {"licenseKey": env_key, "licenseExpiry": env_expiry, "source": "env"}

    reg_data = read_license_from_registry()
    if reg_data:
        reg_data["source"] = "registry"
        return reg_data

    return {"licenseKey": "", "licenseExpiry": "", "source": "missing"}


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

        if parsed.path == '/api/license':
            self._json(read_license_config())
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
                'products':      payload.get('products', []),
                'telegramToken':   payload.get('telegramToken', ''),
                'telegramChatId':  payload.get('telegramChatId', '')
            }
            write_json(SETTINGS_FILE, settings_to_save)
            self._json({'ok': True})
            return
        
        if parsed.path == '/api/settlement':
            # Send Telegram notification
            settle  = payload.get('settle', {})
            settings = read_json(SETTINGS_FILE, DEFAULT_SETTINGS)
            token   = settings.get('telegramToken', '')
            chat_id = settings.get('telegramChatId', '')
            if token and chat_id:
                threading.Thread(
                    target=send_telegram,
                    args=(token, chat_id, settle),
                    daemon=True
                ).start()
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

def send_telegram(token, chat_id, settle):
    try:
        bakery   = settle.get('bakery', 'فرن الأصلي')
        date     = settle.get('date', '')
        time_str = settle.get('time', '')
        total_ll = settle.get('totalLL', 0)
        rate     = settle.get('rate', 90000)
        count    = settle.get('count', 0)
        delivery = settle.get('deliveryCount', 0)
        total_usd = total_ll / rate if rate else 0

        # Format numbers with commas
        def fmt(n):
            return '{:,}'.format(int(n))

        msg = (
            '\U0001f9fe *' + bakery + ' \u2014 \u0625\u063a\u0644\u0627\u0642 \u0627\u0644\u062d\u0633\u0627\u0628*\n'
            '\U0001f4c5 ' + date + ' \u2014 ' + time_str + '\n'
            '\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n'
            '\U0001f4e6 \u0627\u0644\u0637\u0644\u0628\u064a\u0627\u062a: *' + str(count) + '*\n'
            '\U0001f6f5 \u062a\u0648\u0635\u064a\u0644: *' + str(delivery) + '*\n'
            '\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n'
            '\U0001f4b0 \u0627\u0644\u0645\u0628\u064a\u0639\u0627\u062a: *' + fmt(total_ll) + ' \u0644.\u0644*\n'
            '\U0001f4b5 \u0628\u0627\u0644\u062f\u0648\u0644\u0627\u0631: *$' + '{:.2f}'.format(total_usd) + '*'
        )

        url = 'https://api.telegram.org/bot' + token + '/sendMessage'
        data = json.dumps({
            'chat_id':    chat_id,
            'text':       msg,
            'parse_mode': 'Markdown'
        }).encode('utf-8')

        from urllib.request import Request
        req = Request(url, data=data, headers={'Content-Type': 'application/json'})
        urlopen(req, timeout=10)
        print('  Telegram notification sent')
    except Exception as e:
        print('  Telegram error: ' + str(e))

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
