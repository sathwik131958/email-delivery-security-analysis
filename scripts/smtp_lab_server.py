#!/usr/bin/env python3

import socketserver
import os
import datetime

HOST = "127.0.0.1"
PORT = 2525

MAILBOX = "data/mailbox"
LOG = "logs/smtp_server.log"

os.makedirs(MAILBOX, exist_ok=True)
os.makedirs("logs", exist_ok=True)


def log(message):
    line = f"{datetime.datetime.now().isoformat(timespec='seconds')} {message}"

    print(line, flush=True)

    with open(LOG, "a") as f:
        f.write(line + "\n")


class SMTPHandler(socketserver.StreamRequestHandler):

    def handle(self):

        client = self.client_address

        log(f"CONNECT {client}")

        self.wfile.write(
            b"220 VeriMailLab SMTP Service Ready\r\n"
        )

        sender = None
        recipients = []
        data = []
        in_data = False

        while True:

            raw = self.rfile.readline()

            if not raw:
                break

            line = raw.decode(
                "utf-8",
                "replace"
            ).rstrip("\r\n")

            log(f"CMD {line[:200]}")

            # EMAIL DATA MODE
            if in_data:

                if line == ".":

                    message = "\r\n".join(data) + "\r\n"

                    timestamp = datetime.datetime.now().strftime(
                        "%Y%m%d_%H%M%S_%f"
                    )

                    filename = os.path.join(
                        MAILBOX,
                        f"email_{timestamp}.eml"
                    )

                    with open(
                        filename,
                        "w",
                        encoding="utf-8"
                    ) as f:

                        f.write(message)

                    log(
                        f"DELIVERED {filename} "
                        f"sender={sender} "
                        f"recipients={recipients}"
                    )

                    self.wfile.write(
                        b"250 2.0.0 Message accepted for delivery\r\n"
                    )

                    in_data = False
                    data = []

                else:

                    data.append(line)

                continue

            command = line.upper()

            # EHLO / HELO
            if command.startswith("EHLO") or command.startswith("HELO"):

                self.wfile.write(
                    b"250-VeriMailLab\r\n"
                    b"250-SIZE 10485760\r\n"
                    b"250 8BITMIME\r\n"
                )

            # MAIL FROM
            elif command.startswith("MAIL FROM:"):

                sender = line[10:].strip()

                self.wfile.write(
                    b"250 2.1.0 Sender OK\r\n"
                )

            # RCPT TO
            elif command.startswith("RCPT TO:"):

                recipients.append(
                    line[8:].strip()
                )

                self.wfile.write(
                    b"250 2.1.5 Recipient OK\r\n"
                )

            # DATA
            elif command == "DATA":

                if not recipients:

                    self.wfile.write(
                        b"503 Need RCPT TO first\r\n"
                    )

                else:

                    self.wfile.write(
                        b"354 End data with <CR><LF>.<CR><LF>\r\n"
                    )

                    in_data = True

            # QUIT
            elif command == "QUIT":

                self.wfile.write(
                    b"221 2.0.0 Bye\r\n"
                )

                break

            else:

                self.wfile.write(
                    b"502 Command not implemented\r\n"
                )

        log(f"DISCONNECT {client}")


class SMTPServer(socketserver.ThreadingTCPServer):

    allow_reuse_address = True


if __name__ == "__main__":

    with SMTPServer(
        (HOST, PORT),
        SMTPHandler
    ) as server:

        log(
            f"SMTP LAB SERVER listening on "
            f"{HOST}:{PORT}"
        )

        try:

            server.serve_forever()

        except KeyboardInterrupt:

            print("\nServer stopped.")
