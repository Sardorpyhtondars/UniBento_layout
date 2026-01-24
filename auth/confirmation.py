import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from core.db_settings import execute_query
from core.config import EMAIL_USER, EMAIL_PASS


def send_email(recipient_email: str, subject: str, body: str) -> bool:
    """
    Sends an email using smtplib server
    :param recipient_email: Email of the recipient
    :param subject: Subject of the email
    :param body: Body of the email
    :return: True if email was sent
    """
    massage = MIMEMultipart()
    massage['From'] = EMAIL_USER
    massage['To'] = recipient_email
    massage['Subject'] = subject

    massage.attach(MIMEText(body, 'plain'))

    server = None
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(massage)
        return True

    except Exception as e:
        print(f"Error sending email: {e}")
        return False
    finally:
        if server:
            server.quit()


def generate_code(user_email: str) -> int:
    """
    Generates a random 6 character code
    :param user_email: user's email from which email will be sent
    :return: code
    """
    code = str(random.randint(100000, 999999))

    query = "SELECT * FROM codes WHERE code = %s"
    params = (code,)
    result = execute_query(query=query, params=params, fetch="one")

    if result:
        return generate_code(user_email)

    query1 = "INSERT INTO codes (email, code) VALUES (%s, %s)"
    params1 = (user_email, code)
    execute_query(query=query1, params=params1)

    return code