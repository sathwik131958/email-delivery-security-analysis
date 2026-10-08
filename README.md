# Email Delivery and Network Security Analysis

## Overview

This project investigates the basic journey of an email using a
controlled local SMTP environment.

The project combines SMTP protocol analysis, DNS/MX investigation,
email-header analysis, Wireshark packet capture and delivery-failure
investigation.

## Objectives

- Understand email architecture
- Study SMTP commands and responses
- Analyze DNS MX records
- Analyze email headers
- Capture SMTP traffic using Wireshark
- Measure delivery latency
- Investigate SMTP failure conditions
- Identify basic security considerations

## Architecture

Python SMTP Client
        |
        | SMTP
        v
Local SMTP Server
        |
        v
Controlled Mailbox

DNS/MX and Wireshark are used for analysis.

## Technology Stack

- Python 3
- SMTP
- Linux/Debian
- Wireshark
- DNS/MX
- dig
- Git

## SMTP Commands

EHLO
MAIL FROM
RCPT TO
DATA
QUIT

## Network Analysis

Wireshark captures traffic on the Linux loopback interface.

The SMTP laboratory uses:

127.0.0.1:2525

## DNS Analysis

DNS MX records are queried to identify mail servers responsible
for receiving email for a domain.

## Email Header Analysis

The project analyzes:

- From
- To
- Subject
- Date
- Message-ID
- Content-Type
- MIME-Version

## Failure Analysis

An SMTP connection failure is demonstrated by stopping the
local SMTP server and attempting delivery.

## Security Relevance

The project demonstrates beginner-level Blue Team techniques:

- Network traffic analysis
- SMTP protocol investigation
- DNS investigation
- Email-header analysis
- Packet capture
- Failure detection
- Evidence collection

## Conclusion

The project demonstrates the basic email delivery process and
provides a controlled environment for analyzing SMTP, DNS,
TCP traffic, email headers and delivery failures.
