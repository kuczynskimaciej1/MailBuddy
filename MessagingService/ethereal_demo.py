import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
#import MessagingService.smtp_data


# Ethereal credentials
ETH_USER = ""
ETH_PASSWORD = ""

def send_email():
    # Email content
    sender_email = ETH_USER
    receiver_email = ""
    subject = "Example Email from Python"
    body = "Hello."

    # Constructing the email
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # Connecting to Ethereal SMTP server
    with smtplib.SMTP_SSL("smtp.poczta.onet.pl", 465) as server:
        #server.starttls()
        server.login(ETH_USER, ETH_PASSWORD)
        server.sendmail(sender_email, receiver_email, message.as_string())

    print("Email sent successfully!")

if __name__ == "__main__":
    send_email()
