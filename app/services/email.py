import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings


def send_email(to_email: str, subject: str, body: str):
    print(f"Sending email to {to_email} with subject: {subject}")
    msg = MIMEMultipart()
    msg["From"] = "no-reply@example.com"
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(settings.mailtrap_host, settings.mailtrap_port) as server:
            server.login(settings.mailtrap_username, settings.mailtrap_password)
            server.sendmail(msg["From"], to_email, msg.as_string())
    except Exception as e:
        print(f"Error sending email: {e}")
