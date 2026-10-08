import subprocess
import sys
from datetime import datetime


domain = sys.argv[1] if len(sys.argv) > 1 else "gmail.com"

print()
print("======================================")
print("          DNS / MX ANALYSIS")
print("======================================")

print(f"Domain: {domain}")
print(f"Time: {datetime.now()}")

try:

    result = subprocess.run(
        ["dig", "+short", "MX", domain],
        capture_output=True,
        text=True,
        timeout=10
    )

    records = result.stdout.strip()

    if records:

        print()
        print("MX RECORDS:")

        for record in records.splitlines():
            print("  ", record)

        status = "SUCCESS"

    else:

        print()
        print("No MX record found.")

        status = "NO_MX"


except FileNotFoundError:

    print("dig command not installed.")

    status = "TOOL_MISSING"


with open(
    "reports/dns_result.txt",
    "w"
) as file:

    file.write(
        f"Domain: {domain}\n"
        f"Status: {status}\n"
        f"MX Records:\n{records if 'records' in locals() else ''}\n"
    )


print()
print(f"DNS Analysis Status: {status}")
print("Saved: reports/dns_result.txt")
