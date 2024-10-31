# email_service.py
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email server configuration
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'chinmay.jena7878@gmail.com'
# EMAIL_HOST_USER = 'travel.exploooration@gmail.com'
EMAIL_HOST_PASSWORD = 'clsq ccrf ckcs tzku'
# EMAIL_HOST_PASSWORD = 'blvz upxg bdih mqht'

def send_email(subject, html_content, recipient=EMAIL_HOST_USER):
    # Set up the email
    message = MIMEMultipart("alternative")
    message["From"] = EMAIL_HOST_USER
    message["To"] = recipient
    message["Subject"] = subject

    # Attach the HTML content
    message.attach(MIMEText(html_content, "html"))

    try:
        # Connect to the SMTP server and send the email
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            server.sendmail(EMAIL_HOST_USER, recipient, message.as_string())
        # print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")
