# -*- coding: utf-8 -*-
import asyncio
import argparse
from aiosmtpd.controller import Controller
from email.parser import BytesParser
from email.policy import default
from rgbpy import log_style
from rgbpy import purple


class EmailHandler:
    async def handle_DATA(self, server, session, envelope):
        peer = session.peer
        mail_from = envelope.mail_from
        rcpt_tos = envelope.rcpt_tos
        data = envelope.content

        print()
        purple(f'|:  Peer: {peer}')
        purple(f'|:  Mail from: {mail_from}')
        purple(f'|:  Recipients: {rcpt_tos}')

        message = BytesParser(policy=default).parsebytes(data)
        purple(f'|:  {message}')

        return '250 Message accepted for delivery'


async def main(hostname, port):
    controller = Controller(EmailHandler(), hostname=hostname, port=port)
    controller.start()
    log_style(f"SMTP server started on localhost:{port}")

    try:
        while True:
            # Sleep for an hour, then loop
            await asyncio.sleep(3600)
    except KeyboardInterrupt:
        log_style("SMTP server shutting down...", log='error')
        controller.stop()
        

def kyaah_cli():
    """Kyaah command-line utility function"""

    parser = argparse.ArgumentParser(description='Start an async SMTP server.')

    # metavar make the -help to look cleaan
    parser.add_argument('localhost', metavar='localhost', type=str, help='Hostname for the SMTP server')
    parser.add_argument('--port', type=int, default=1025, help='Port for the SMTP server')

    args = parser.parse_args()

    if args.localhost != "localhost":
        error_help = f"""\n\tusage: kyaah [-h] [--port PORT] localhost [localhost ...]

\tStart an async SMTP server.

\tpositional arguments:
\tlocalhost    an integer for the accumulator

\toptions:
\t-h, --help   show this help message and exit
\t--port PORT  Port for the SMTP server"""
        log_style(error_help)
        exit()

    asyncio.run(main(args.localhost, args.port))
