import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# AWS SES SMTP configuration
smtp_server = "email-smtp.us-east-1.amazonaws.com"  # Replace with your AWS SES SMTP endpoint
smtp_port = 587  # Use 465 for SSL or 587 for STARTTLS
aws_access_key = "AKIAQAFGKCS7UIMR53XU"  # Replace with your AWS SMTP username
aws_secret_key = "BEDzS9y48HJF0jg0+sifogVBGH87lR4XpSKtm6kdEGZ9"  # Replace with your AWS SMTP password

# Email details
sender_email = "bimalkhimdung@gmail.com"  # Verified email address in AWS SES
recipient_email = "bimal.rai@realhrsoft.com"  # Recipient's email address
subject = "Test Email from AWS SES"
body = "This is a test email sent using AWS SES SMTP integration."

# Create the email
msg = MIMEMultipart()
msg["From"] = sender_email
msg["To"] = recipient_email
msg["Subject"] = subject
msg.attach(MIMEText(body, "plain"))

# Connect to the AWS SES SMTP server and send the email
try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Secure the connection with STARTTLS
    server.login(aws_access_key, aws_secret_key)
    server.send_message(msg)
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")
finally:
    server.quit()
