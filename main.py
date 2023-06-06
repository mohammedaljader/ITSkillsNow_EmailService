import uvicorn
import json
import os
from fastapi import FastAPI
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from jinja2 import Environment, FileSystemLoader
from aio_pika import connect_robust, IncomingMessage
from dotenv import load_dotenv
load_dotenv('.env')

app = FastAPI()


@app.post("/send-email/")
def send_email(email: str, subject: str, message: str):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "s6.mohammedaljader@gmail.com"
    sender_password = "oapplcpiborcrxfd"

    # Initialize Jinja2 environment
    env = Environment(loader=FileSystemLoader("templates"))

    # Load and render HTML template
    template = env.get_template("email.html")
    html_content = template.render(title=subject, name="Mohammed", code="4312", message=message)

    # Create a multipart message container
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = email

    # Attach the HTML content to the email
    msg.attach(MIMEText(html_content, "html"))

    # Connect to the SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)

    # Send the email
    server.sendmail(sender_email, email, msg.as_string())

    # Close the connection
    server.quit()

    return {"message": "Email sent successfully!"}


def send(email: str, subject: str, message: str):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "s6.mohammedaljader@gmail.com"
    sender_password = "oapplcpiborcrxfd"

    # Initialize Jinja2 environment
    env = Environment(loader=FileSystemLoader("templates"))

    # Load and render HTML template
    template = env.get_template("email.html")
    html_content = template.render(title=subject, name="Mohammed", code="4312", message=message)

    # Create a multipart message container
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = email

    # Attach the HTML content to the email
    msg.attach(MIMEText(html_content, "html"))

    # Connect to the SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)

    # Send the email
    server.sendmail(sender_email, email, msg.as_string())

    # Close the connection
    server.quit()

    return {"message": "Email sent successfully!"}


@app.get('/')
def index():
    return 'Hello World'


async def process_message(message: IncomingMessage):
    async with message.process():
        body = message.body.decode() 
        payload = json.loads(body)  
        email = payload['userPayload']['email']  
        username = payload['userPayload']['username'] 
        fullname = payload['userPayload']['fullName']  
        send(email, username, fullname)

async def start_listener():
    # Connect to RabbitMQ
    RabbitMQ_URL = os.getenv('RabbitMQ_URL')
    connection = await connect_robust(RabbitMQ_URL)
    
    # Create a channel
    channel = await connection.channel()
    
    # get a queue
    queue = await channel.get_queue("auth.queue")
    
    # Start consuming messages
    await queue.consume(process_message)


@app.on_event("startup")
async def startup_event():
    # Start the RabbitMQ listener
    await start_listener()

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
