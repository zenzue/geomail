import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SENDER = "your@email.com"
PASSWORD = "your-app-password"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def send_security_mail(to, html_body, subject="Security Awareness Notice"):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SENDER
    msg["To"] = to

    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER, PASSWORD)
        server.sendmail(SENDER, to, msg.as_string())

if __name__ == "__main__":
    with open("mail_body.html") as f:
        html = f.read()
    send_security_mail("recipient@domain.com", html)