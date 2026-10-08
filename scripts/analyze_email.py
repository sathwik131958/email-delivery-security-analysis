import glob
import os
import json
from email import policy
from email.parser import BytesParser


files = sorted(glob.glob("data/mailbox/*.eml"))

if not files:
    print("No email found.")
    exit()

email_file = files[-1]

with open(email_file, "rb") as file:
    message = BytesParser(
        policy=policy.default
    ).parse(file)


print()
print("======================================")
print("       EMAIL HEADER ANALYSIS")
print("======================================")

headers = [
    "From",
    "To",
    "Subject",
    "Date",
    "Message-ID",
    "Received",
    "Content-Type",
    "MIME-Version"
]

for header in headers:

    values = message.get_all(header)

    if values:
        for value in values:
            print(f"{header}: {value}")


print()
print("======================================")
print("       SECURITY CHECKS")
print("======================================")

checks = {
    "From header": bool(message.get("From")),
    "To header": bool(message.get("To")),
    "Subject header": bool(message.get("Subject")),
    "Date header": bool(message.get("Date")),
    "Message-ID": bool(message.get("Message-ID")),
    "Received header": bool(message.get_all("Received"))
}

for name, result in checks.items():

    if result:
        print(f"[OK]   {name}")

    else:
        print(f"[WARN] {name} missing")


result = {
    "file": email_file,
    "size_bytes": os.path.getsize(email_file),
    "headers": {
        header: message.get_all(header)
        for header in headers
        if message.get_all(header)
    },
    "security_checks": checks
}


with open(
    "reports/email_analysis.json",
    "w"
) as file:

    json.dump(
        result,
        file,
        indent=4,
        default=str
    )


print()
print("Analysis saved to:")
print("reports/email_analysis.json")
