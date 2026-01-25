"""
Generates a code and sends to the user
"""

import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from core.config import EMAIL_USER, EMAIL_PASS
from core.db_settings import execute_query

def send_email(recipient_email: str, subject:str, body:str)->bool:
    """
    Send a text email using Gmail SMTP server
    Args:
        recipient_email: Recipient's email address
        subject: Email subject
        body: Email body text
    """
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    server = None
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        return True

    except Exception as e:
        print(f"Error sending email: {e}")
        return False
    finally:
        if server:
            server.quit()


def generate_code(user_email:str) -> str:
    """
    Generate a random 6-digit code and save it to database
    :return: generate and save code in database
    """
    code = str(random.randint(100000, 999999))
    query = "SELECT * FROM codes WHERE code = (%s)"
    params = (code,)
    result = execute_query(query=query, params=params, fetch="one")
    if result:
        return generate_code(user_email)
    query1 = "INSERT INTO codes (email, code) VALUES (%s, %s)"
    params1 = (user_email, code)
    if execute_query(query=query1, params=params1):
        print("Code sent to your email")
        print("Code", code)
        return code
    print("Something went wrong, try again later")
    return None