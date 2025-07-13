import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SENDER = "mail@email.com"
PASSWORD = "password"
SMTP_SERVER = "friday.mail.com"

def send_security_mail(to, html_body, subject="Security Awareness Notice 1"):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SENDER
    msg["To"] = to
    msg.attach(MIMEText(html_body, "html"))

    tried = False
    try:
        print(f"Trying STARTTLS on port 587...")
        with smtplib.SMTP(SMTP_SERVER, 587, timeout=10) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(SENDER, PASSWORD)
            server.sendmail(SENDER, to, msg.as_string())
        print("Mail sent via STARTTLS/587.")
        tried = True
    except Exception as e:
        print(f"Failed on 587 (STARTTLS): {e}")

    if not tried:
        try:
            print(f"Trying SSL on port 465...")
            with smtplib.SMTP_SSL(SMTP_SERVER, 465, timeout=10) as server:
                server.ehlo()
                server.login(SENDER, PASSWORD)
                server.sendmail(SENDER, to, msg.as_string())
            print("Mail sent via SSL/465.")
            tried = True
        except Exception as e:
            print(f"Failed on 465 (SSL): {e}")

    if not tried:
        try:
            print(f"Trying STARTTLS on port 25...")
            with smtplib.SMTP(SMTP_SERVER, 25, timeout=10) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(SENDER, PASSWORD)
                server.sendmail(SENDER, to, msg.as_string())
            print("Mail sent via STARTTLS/25.")
            tried = True
        except Exception as e:
            print(f"Failed on 25 (STARTTLS): {e}")

    if not tried:
        print("All connection attempts failed.")
        print("Check your SMTP server address, port, and credentials.")
        print("If you are on a network that blocks outbound SMTP, try from another location or server.")

if __name__ == "__main__":
    with open("mail_body.html") as f:
        html = f.read()
    send_security_mail("w01f@mail.tech", html)
