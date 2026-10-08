import smtplib
import time
import uuid

from email.message import EmailMessage
from email.utils import formatdate, make_msgid


SMTP_SERVER = "127.0.0.1"
SMTP_PORT = 2525


message = EmailMessage()

message["From"] = "alice@verimail.test"
message["To"] = "bob@verimail.test"
message["Subject"] = "VeriMailLab Security Test"

message["Date"] = formatdate(localtime=True)

message["Message-ID"] = make_msgid(
    domain="verimail.test"
)

message["X-Test-ID"] = str(uuid.uuid4())

message["X-Security-Project"] = (
    "Email Delivery Security Analysis"
)

message.set_content(
    "This is a controlled test email "
    "for SMTP, DNS, Wireshark and "
    "security analysis."
)


start = time.perf_counter()


with smtplib.SMTP(
    SMTP_SERVER,
    SMTP_PORT,
    timeout=10
) as smtp:

    smtp.set_debuglevel(1)

    smtp.ehlo("client.verimail.test")

    smtp.send_message(message)


elapsed = time.perf_counter() - start


with open(
    "reports/delivery_result.txt",
    "w"
) as file:

    file.write(
        f"Status: SUCCESS\n"
        f"SMTP Server: {SMTP_SERVER}:{SMTP_PORT}\n"
        f"Delivery Time: {elapsed:.4f} seconds\n"
        f"Message-ID: {message['Message-ID']}\n"
    )


print()
print("================================")
print("EMAIL DELIVERY SUCCESS")
print("================================")
print(f"Delivery time: {elapsed:.4f} seconds")
