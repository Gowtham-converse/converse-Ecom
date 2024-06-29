import random
import hashlib
from fastapi import HTTPException
from datetime import datetime, timedelta

def generate_otp_and_hash():
    otp = ''.join(str(random.randint(0, 9)) for _ in range(6))
    expiration_time = datetime.now() + timedelta(minutes=20)
    hash_otp = hashlib.sha256(otp.encode()).hexdigest()
    return {"otp": otp, "hash_otp": hash_otp, "expiration_time": expiration_time}


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pydantic import EmailStr
from fastapi import HTTPException

async def send_otp_email(recipient_email: EmailStr, otp: str):
    sender_email = 'loggerkey314@gmail.com'  # Replace with your email address
    password = 'wgaw vdgv xxsc xwjw'  # Replace with your email password

    subject = "OTP Verification"
    body = f"Your OTP for verification is: {otp}"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, password)
            server.sendmail(sender_email, recipient_email, message.as_string())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send OTP email: {str(e)}")