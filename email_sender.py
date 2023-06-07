from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from jinja2 import Environment, FileSystemLoader


def send_emails(email: str, subject: str, message: str, code: str, fullName: str):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "s6.mohammedaljader@gmail.com"
    sender_password = "oapplcpiborcrxfd"

    # Initialize Jinja2 environment
    env = Environment(loader=FileSystemLoader("templates"))

    # Load and render HTML template
    template = env.get_template("email.html")
    html_content = template.render(title=subject, name=fullName, code=code, message=message)

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
