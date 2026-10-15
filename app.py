import json
from pathlib import Path

import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
REPORTS_DIR = BASE_DIR / "reports"
SCREENSHOTS_DIR = BASE_DIR / "screenshots"

st.set_page_config(
    page_title="Email Security Analysis",
    page_icon="✉️",
    layout="wide",
)

st.title("Email Delivery & Network Security Analysis")
st.caption("Blue Team Laboratory | SMTP • DNS/MX • Email Headers • Network Evidence")

def read_text(filename):
    path = REPORTS_DIR / filename
    if path.exists():
        return path.read_text(encoding="utf-8", errors="replace")
    return f"Report not found: {filename}"

def read_json(filename):
    path = REPORTS_DIR / filename
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None

delivery = read_text("delivery_result.txt")
dns = read_text("dns_result.txt")
failure = read_text("failure_test.txt")
analysis = read_json("email_analysis.json")

delivery_ok = "Status: SUCCESS" in delivery

col1, col2, col3 = st.columns(3)
col1.metric("SMTP Delivery", "SUCCESS" if delivery_ok else "CHECK REPORT")
col2.metric("DNS/MX Analysis", "Available" if "MX Records:" in dns else "Check report")
col3.metric("Evidence Screenshots", len(list(SCREENSHOTS_DIR.glob("*.png"))) if SCREENSHOTS_DIR.exists() else 0)

st.divider()

overview, dns_tab, headers_tab, failure_tab, evidence_tab = st.tabs([
    "SMTP Delivery",
    "DNS / MX",
    "Email Headers",
    "Failure Analysis",
    "Screenshots",
])

with overview:
    st.subheader("SMTP Delivery Result")
    st.code(delivery, language="text")
    st.markdown("""
    **Workflow**
    1. Python SMTP client creates a test email.
    2. The client connects to the local SMTP lab server.
    3. The server accepts and stores the message.
    4. The delivery report records the outcome.
    """)
    st.info("The local SMTP lab uses 127.0.0.1:2525. This demonstrates a controlled test environment, not proof of delivery to an external recipient.")

with dns_tab:
    st.subheader("Domain Mail Exchange Investigation")
    st.code(dns, language="text")
    st.caption("MX records identify mail servers configured to receive email for a domain.")

with headers_tab:
    st.subheader("Email Header Security Checks")
    if analysis is not None:
        st.json(analysis)
    else:
        st.warning("email_analysis.json is missing or is not valid JSON.")
    st.caption("A missing Received header can be expected in a locally generated message that has not passed through a real mail-transfer chain.")

with failure_tab:
    st.subheader("SMTP Failure Test")
    st.code(failure, language="text")
    st.markdown("""
    **Investigation checklist**
    - Check whether the SMTP server is running.
    - Confirm the configured host and port.
    - Review the SMTP server log.
    - Compare the failure report with a successful delivery.
    """)
    log_path = BASE_DIR / "logs" / "smtp_server.log"
    if log_path.exists():
        with st.expander("View SMTP server log"):
            st.text(log_path.read_text(encoding="utf-8", errors="replace")[-12000:])

with evidence_tab:
    st.subheader("Project Evidence")
    if SCREENSHOTS_DIR.exists():
        images = sorted(SCREENSHOTS_DIR.glob("*.png"))
        if not images:
            st.info("No PNG screenshots found.")
        for img in images:
            with st.expander(img.name):
                st.image(str(img), caption=img.name, use_container_width=True)
    else:
        st.info("Screenshots folder not found.")

with st.sidebar:
    st.header("Project Information")
    st.write("**Focus:** Blue Team / Email Security")
    st.write("**Environment:** Debian Linux")
    st.write("**Protocol:** SMTP")
    st.write("**Local endpoint:** 127.0.0.1:2525")
    st.divider()
    st.write("Dashboard reads existing project files; it does not send emails or perform live network scans.")
    if st.button("Refresh dashboard"):
        st.rerun()
