import uvicorn
from fastapi import FastAPI
import smtplib

app = FastAPI()


@app.post("/send-email/")
def send_email(email: str, subject: str, message: str):
    # SMTP server details
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "s6.mohammedaljader@gmail.com"
    sender_password = "oapplcpiborcrxfd"

    # Connect to the SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)

    # Compose the email
    email_content = f"Subject: {subject}\n\n{message}"

    # Send the email
    server.sendmail(sender_email, email, email_content)

    # Close the connection
    server.quit()

    return {"message": "Email sent successfully!"}


@app.get('/')
def index():
    return 'Hello World'


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
