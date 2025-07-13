# Email Security Awareness Collector

**Author:** w01f
**Purpose:** Educational – For Security Awareness and Internal Security Testing Lab (University Level)

---

## Overview

This project demonstrates how information can be silently collected via email opens for security awareness purposes. It consists of a Python Flask server that records client metadata when a specially crafted email is opened. The setup logs IP, device, geolocation (if possible), and client information into an SQLite database, and can also send instant Telegram alerts.

**Educational Use Only! Do not use for unauthorized testing.**

---

## Features

* Collects data via:

  * HTML image beacon (for IP/User-Agent)
  * JavaScript POST (browser: device, timezone, geolocation, etc.)
* Data stored in SQLite database
* Sends Telegram notification for every new event
* Modern responsive email template
* Easy deployment with Docker Compose
* Can be exposed to the Internet using [ngrok](https://ngrok.com/) for testing

---

## Architecture

```
[Email Receiver] -> [Your Email Template]
      |                    |
      |      [beacon.png] and/or JS POST
      v                    v
         [Flask Collector Server (Docker)]
                   |
              [SQLite DB]
                   |
             [Telegram Bot]
```

---

## Setup

### 1. Clone the repository

```bash
git clone git@github.com:zenzue/geomail.git
cd geomail
```

---

### 2. Configure Environment Variables

Edit `docker-compose.yml` and set your **Telegram bot token** and **chat ID**:

```yaml
environment:
  - TELEGRAM_BOT_TOKEN=your_telegram_bot_token
  - TELEGRAM_CHAT_ID=your_telegram_chat_id
```

---

### 3. Build and Start the Collector Server

```bash
docker compose build
docker compose up
```

The server will be available at [http://localhost:8000](http://localhost:8000).

---

### 4. Expose to the Internet Using Ngrok

**(For external email testing or mobile opens.)**

1. [Download ngrok](https://ngrok.com/download)

2. Run ngrok on the collector’s port:

   ```bash
   ngrok http 8000
   ```

3. Ngrok will show a public forwarding URL like `https://abcd1234.ngrok.io`.

4. **Update your email template** to use this ngrok address, e.g.:

   ```html
   <img src="https://abcd1234.ngrok.io/beacon.png" style="display:none;">
   ```

   And in the JavaScript collector POST URL.

---

### 5. Prepare and Send Email

* Edit `mail_body.html` to include your ngrok URL.
* Use `send_mail.py` to send the template to a test address.

---

### 6. View Collected Data

* All data is stored in `collected_data/collected_data.db`.
* You can use `sqlite3` CLI or any SQLite viewer.

---

## File Structure

```
.
├── collector_server.py      # Main Flask server
├── mail_body.html          # Responsive, stealthy email template
├── send_mail.py            # Example script to send the email
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── collected_data/         # SQLite DB location (persistent)
```

---

## Educational Purpose and Ethics

* **This project is for lab use and security awareness demonstrations only.**
* Do not use on real users or external parties without clear, documented permission.

---

## Author

* **w01f**
  [github.com/zenzue](https://github.com/zenzue/)
  Internal Security Research & Education

---

## License

For educational use only. Not for commercial or unauthorized penetration testing.