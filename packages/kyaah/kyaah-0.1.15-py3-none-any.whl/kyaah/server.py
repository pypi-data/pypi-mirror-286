# -*- coding: utf-8 -*-
"""
Mail servers stuffs with ease!

internal sample:
    >>> box = imaplib.IMAP4_SSL('imap.mail.microsoftonline.com', 993)
"""


server = {
    # Local Mail Settings
    'local': {
        'server': ['localhost'],
        'port': [
            1025, # smtp server
        ]
    },
    # Zoho Mail Settings: POP3, IMAP, and SMTP Server Settings
    # Lycos Mail Settings: POP3, IMAP, and SMTP Servers Settings
    # Laposte Email Settings: POP3, IMAP, SMTP Server Settings
    # Kolab Now Email Settings: POP3, IMAP, and SMTP Server Settings
    # iCloud Email Settings: POP3, IMAP, and SMTP Server Settings
    'icloud': {
        'server': [
            'smtp.mail.me.com',
            # 💡 Note: In comparison to other mail providers, iCloud does not support POP configurations. Rather than that, users can utilize IMAP settings to manually configure an email program's inbound server for usage with their iCloud account, allowing Mail to download messages.
            'imap.mail.me.com'
        ],
        'port': [
            465, # SSL. If you see an error message when using SSL, try using TLS or STARTTLS instead.
            587, # smtp server
            # 💡 Note: In comparison to other mail providers, iCloud does not support POP configurations. Rather than that, users can utilize IMAP settings to manually configure an email program's inbound server for usage with their iCloud account, allowing Mail to download messages.
            993, # imap server, (it listen on port 143, but use 993 for SSL)
        ]
    },
    # Hushmail Email Settings: POP3, IMAP, and SMTP Servers Settings
    # GoDaddy Workspace Email Settings: POP3, IMAP, SMTP Servers
    # GMX.com Email Settings: POP3, IMAP, and SMTP Servers Settings
    # Gmail Email Settings: POP3, IMAP, and SMTP Servers Settings
    'gmail': {
        'server': [
            'smtp.gmail.com',
            'pop.googlemail.com',
            'imap.gmail.com'
        ],
        'port': [
            465, # smtp server (for SSL) it listen on port 25 if not SSL
            587, # smtp server (for TLS)
            995, # pop server, (it listen on port 110, but use 995 for SSL)
            993, # imap server, (it listen on port 143, but use 993 for SSL)
        ]
    },
    # Mail.com Email Settings: POP3, IMAP, and SMTP Servers Settings
    # Gandi Email Settings: POP3, IMAP, and SMTP Server Settings
    # Fastmail Email Settings: POP3, IMAP, and SMTP Servers
    # Execulink Email Settings: POP3, IMAP, SMTP Server Settings
    # EarthLink Email Settings: POP3, IMAP, SMTP Server Settings
    # Currently.com Email Settings: POP3, IMAP, and SMTP Servers
    # Cox Email Settings: POP3, IMAP, SMTP Server Settings
    # Charter Email Settings: POP3, IMAP, and SMTP Server Settings
    # CenturyLink Email Settings: POP3, IMAP, SMTP Server Settings
    # Bluehost Email Settings: POP3, IMAP, SMTP Server Settings
    # Frontier Email Settings: POP3, IMAP, SMTP Server Settings
    # AT&T Email Settings: POP3, IMAP, and SMTP Server Settings
    # Mail.ru Email Settings: POP3, IMAP, and SMTP Server Settings
    # Outlook Email Settings: POP3, IMAP, and SMTP Server Settings
    'outlook': {
        'server': [
            'smtp.office365.com',
            # 'smtp-mail.outlook.com', # SMTP Host for MSN
            'outlook.office365.com',
            # 'pop-mail.outlook.com', # POP3 Host for MSN
            'outlook.office365.com', # SMTP Host for Outlook.com (Hotmail, Live.com, Microsoft 365)
            # 'imap-mail.outlook.com',
        ],
        'port': [
            465, # smtp server (for SSL) it listen on port 25 if not SSL
            587, # smtp server (for TLS)
            995, # pop server, (it listen on port 110, but use 995 for SSL)
            993, # imap server, (it listen on port 143, but use 993 for SSL)
        ]
    },
    # Yahoo Mail Settings: POP3, IMAP, and SMTP Server Settings
    'yahoo': {
        'server': [
            'smtp.mail.yahoo.com',
            'pop.mail.yahoo.com',
            'imap.mail.yahoo.com'
        ],
        'port': [
            465, # smtp server it listen on port 25 if not SSL
            587, # smtp server
            995, # pop server, (it listen on port 110, but use 995 for SSL)
            993, # imap server, (it listen on port 143, but use 993 for SSL)
        ]
    },
    # Xfinity / Comcast Email Settings: POP3, IMAP, SMTP Settings
    # Why Is My Gmail Not Receiving Emails? - Learn How To Fix It
    # Why Have My Emails Disappeared from My Inbox? - How To Fix
    # StackMail Email Settings: POP3, IMAP, SMTP Server Settings
    # Spectrum Email Settings: POP3, IMAP, and SMTP Settings
    # SmarshMail Email Settings: POP3, IMAP, SMTP Server Settings
    # SFR Mail Settings: POP3, IMAP, and SMTP Server Settings
    # Mailfence Email Settings: POP3, IMAP, and SMTP Server Settings
    # Seznam.cz Email Settings: POP3, IMAP, and SMTP Settings
    # Roadrunner Email Settings: POP3, IMAP, and SMTP Settings
    # Rediffmail Email Settings: POP3, IMAP, and SMTP Settings
    # Rackspace Email Settings: POP3, IMAP, SMTP Server Settings
    # ProtonMail Email Settings: POP3, IMAP, and SMTP Servers
    # Posteo Email Settings: POP3, IMAP, and SMTP Server Settings
    # PolarisMail Settings: POP3, IMAP, and SMTP Server Settings
    # OVH Mail Settings: POP3, IMAP, SMTP Server Settings
    # Runbox Email Settings: POP3, IMAP, and SMTP Server Settings
    # AOL Email Settings: POP3, IMAP, and SMTP Servers Settings
}


class Serve:
    """This class handle SMTP server suffs."""

    def mail(mail):
        """It return server related credentials"""
        
        return server[mail]
