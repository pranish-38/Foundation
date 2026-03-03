import smtplib
from email.message import EmailMessage
import base64

sender_email = "khawaspranish3@gmail.com"
app_password = "fjiplmrkqhcakyad"
receiver_email = "okaytamang364@gmail.com"

msg = EmailMessage()
msg["Subject"] = "Secure Email Demo"
msg["From"] = sender_email
msg["To"] = receiver_email
msg.set_content("Hello! This is a secure email with Base64 attachment.")

# Base64 attachment
file_content = b"This is a confidential report."
encoded_file = base64.b64encode(file_content)

msg.add_attachment(base64.b64decode(encoded_file),
                   maintype="application",
                   subtype="octet-stream",
                   filename="report.txt")

# Connect and send email
with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.ehlo()                # Identify to server
    server.starttls()             # TLS handshake
    server.ehlo()                # Re-identify after TLS
    server.login(sender_email, app_password)
    server.send_message(msg)

print("Email sent successfully!")