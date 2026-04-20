#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
فرن الأصلي — Local Server
شغّل هذا الملف عبر start.bat
"""

import http.server
import json
import os
import sys
import webbrowser
import threading
import time
from urllib.parse import urlparse

PORT = 5050
DATA_FILE = 'data.json'
SETTINGS_FILE = 'settings.json'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Default data if files don't exist ──
DEFAULT_DATA = {
    "invoices": [],
    "settlements": [],
    "masarif": [],
    "orderNum": 0
}

DEFAULT_SETTINGS = {
    "bakery": "فرن الأصلي",
    "whatsapp_owner": "",
    "rate": 90000,
    "adminPass": "1234",
    "deliveryFee": 0,
    "gsheetUrl": "",
    "extras": [
        {"id": "x1", "name": "خضرة", "price": 30000},
        {"id": "x2", "name": "7 حبوب", "price": 30000},
        {"id": "x3", "name": "جريش", "price": 30000},
        {"id": "x4", "name": "أسمر", "price": 30000},
        {"id": "x5", "name": "عسكر", "price": -20000},
        {"id": "x6", "name": "محمصة", "price": 0},
        {"id": "x7", "name": "لفى", "price": 0},
        {"id": "x8", "name": "مقطة", "price": 0}
    ],
    "extraRules": {
        "categories": {},
        "types": {}
    }
}


def read_json(filename, default):
    path = os.path.join(BASE_DIR, filename)
    if not os.path.exists(path):
        write_json(filename, default)
        return default
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return default


def write_json(filename, data):
    path = os.path.join(BASE_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


class Handler(http.server.SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def log_message(self, format, *args):
        pass  # silent

    def do_GET(self):
        parsed = urlparse(self.path)

        # API: get data
        if parsed.path == '/api/data':
            data = read_json(DATA_FILE, DEFAULT_DATA)
            self._json(data)
            return

        # API: get settings
        if parsed.path == '/api/settings':
            settings = read_json(SETTINGS_FILE, DEFAULT_SETTINGS)
            self._json(settings)
            return

        # Serve files normally
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

        # API: save data (invoices, settlements, masarif, orderNum)
        if parsed.path == '/api/data':
            write_json(DATA_FILE, payload)
            self._json({'ok': True})
            return

        # API: save settings (bakery name, rate, extras, etc.)
        if parsed.path == '/api/settings':
            write_json(SETTINGS_FILE, payload)
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
    time.sleep(1)
    webbrowser.open(f'http://localhost:{PORT}/bakery-pos.html')


if __name__ == '__main__':
    os.chdir(BASE_DIR)

    # Start browser in background
    threading.Thread(target=open_browser, daemon=True).start()

    print('')
    print('  POS Server - Forn Al Asli')
    print('  http://localhost:5050')
    print('  Press Ctrl+C to stop')
    print('')

    server = http.server.HTTPServer(('localhost', PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n  Server stopped.')
        sys.exit(0)
