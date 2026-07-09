import smtplib
from email.message import EmailMessage
from flask import current_app


def send_email(to_address: str, subject: str, body: str) -> bool:
    if not current_app.config.get("EMAIL_ENABLED"):
        current_app.logger.info("Email sending disabled.")
        return False

    host = current_app.config.get("SMTP_HOST")
    port = current_app.config.get("SMTP_PORT", 587)
    username = current_app.config.get("SMTP_USERNAME")
    password = current_app.config.get("SMTP_PASSWORD")
    from_address = current_app.config.get("EMAIL_FROM")

    if not all([host, port, username, password, from_address]):
        current_app.logger.error("Missing email configuration, skipping send.")
        return False

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = from_address
    message["To"] = to_address
    message.set_content(body)

    try:
        smtp = smtplib.SMTP(host, port, timeout=30)
        if current_app.config.get("SMTP_USE_TLS"):
            smtp.starttls()
        smtp.login(username, password)
        smtp.send_message(message)
        smtp.quit()
        current_app.logger.info("Email sent to %s", to_address)
        return True
    except Exception as exc:
        current_app.logger.error("Failed to send email to %s: %s", to_address, exc)
        return False
