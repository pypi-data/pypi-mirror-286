# -*- coding: utf-8 -*-
import os
import sys
import time
import imghdr
import poplib
import pprint
import logging
import smtplib
import imaplib
import email.utils
import email.policy
from email.message import EmailMessage
from rgbpy import log_style
from .server import Serve


# NOTSET    ---  0
# DEBUG     ---  10
# INFO      ---  20
# WARNING   ---  30  (default)
# ERROR     ---  40
# CRITICAL  ---  50


FORMATTER = '[+] [%(asctime)s] [%(levelname)s] %(message)s'
logging.basicConfig(format=FORMATTER)
# Creating an object
LOGGER = logging.getLogger()
# Setting the threshold of LOGGER to DEBUG
LOGGER.setLevel(logging.DEBUG)
# platform-specific path separator (for linux `/`, for windows `\\`)
OS_SEP = os.path.sep


class BaseMail:
    """Base class for mail
    
    In all `BaseMail` mathod there is a keyword argument called `port`, that port is the port of your SMTP server which will listen, make sure to put the port that is convenient to your SMTP server e.g for gmail is 465 (SSL), although kyaah has a dictionary of server, where each server has a list of ports, SMTP server, etc.
    """

    def __init__(
        self,
        sender=None,
        receiver: list = None,
        subject=None,
        body=None,
        password=None,
        **kwgs
    ):
        """For iCloud, the username is typically the first part of your email address, for example, my_email, rather than my_email@icloud.com. If your email client cannot connect to iCloud while using only the name portion of your address, try using the full address as a test.
        """

        self.from_sender = sender
        self.to_receiver = receiver
        self.subject = subject
        self.body = body
        self.password = password
        self.server = kwgs["server"]

        while self.from_sender == None:
            raise UnboundLocalError(f'`sender` is required')
        while self.to_receiver == None:
            raise UnboundLocalError(f'`receiver` is required')

    @property
    def from_sender_addr(self):
        """The sender mail address"""

        return self.from_sender

    @property
    def password_env(self):
        """The sender mail password"""

        return self.password

    @property
    def mail_msg(self):
        """Content of the mail (subject and message body)"""

        subj = self.subject
        body = self.body
        data = f'Subject: {subj}\n\n{body}'
        return data

    def check_required(self):
        """Checking for required values"""

        while self.password == None:
            raise UnboundLocalError(f'`password` is required')
        while self.server == None:
            raise UnboundLocalError(f'`server` is required')

    def mail_head(self, msg, body=None):
        """Contains the sender, receiver and subject"""

        # grab the subject from `mail_msg` method by spliting it,
        # and grab the first index which is the subject,
        # then we slice the first index from index `9` that mean we negate
        # `subj` variable of mail_msg method of this class
        # which is `Subject: `

        msg['From'] = self.from_sender_addr
        # The From field indicates the sender’s address i.e. who sent the e-mail.

        msg['To'] = self.to_receiver
        # The To field indicates the recipient’s address i.e. to whom the e-mail is sent.

        msg['Subject'] = self.mail_msg.split('\n')[0][9:]
        # The Subject field indicates the purpose of e-mail. It should be precise and to the point.

        msg['Date'] = email.utils.formatdate(localtime=True)
        # The Date field indicates the date when the e-mail was sent.

        msg['Message-ID'] = email.utils.make_msgid()

        if body:
            msg.set_content(body)
        
        # CC (Carbon copy). It includes those recipient addresses whom we want to keep informed but not exactly the intended recipient.
        
        # BCC (Black Carbon Copy). It is used when we do not want one or more of the recipients to know that someone else was copied on the message.
        
        # Greeting is the opening of the actual message. Eg. Hi Sir or Hi Guys etc.

        # Text it represents the actual content of the message.

        # Signature is the final part of an e-mail message. It includes Name of Sender, Address, and Contact Number.

        # Python has EmailMessage class which can be used build email messages. This class ahs the required methods to customize different parts of the email message like - the TO and FROM tags, the Subject Line as well as the content of the email.

        # sys.stdout.buffer.write(msg.as_bytes())

    def mail_open(self, msg, port):
        """This open the connection, and login to email address using email address provided together with password/app_password
        """

        with smtplib.SMTP_SSL(self.server, port) as smtp:
            smtp.login(self.from_sender_addr, self.password_env)
            smtp.send_message(msg)

    def local_mail(self, port=1025):
        """Localhost mail"""

        try:
            with smtplib.SMTP(self.server, port) as server:
                server.sendmail(self.from_sender_addr, self.to_receiver, self.mail_msg)
            log_style("Email sent locally successfully!")
        except Exception as e:
            log_style(f"Failed to send email: {e}", log="error")

    def send_mail(self, port=25):
        """Send mail with ssl security"""

        # recepients is the list of receivers email address that you will send emaill address to, if the recepients is not included when call the method it will only send it to the `self.to_receiver` that you pass in as the argument when instanciating the `BaseMail` class
        self.check_required()
        
        for receiver in self.to_receiver:
            with smtplib.SMTP_SSL(self.server, port) as smtp:
                smtp.login(self.from_sender_addr, self.password_env)
                smtp.sendmail(self.from_sender_addr, receiver, self.mail_msg)

    def file_to_send(self, file_to, f_opration, _msg=None, maintype=None):
        """Kyaah file to send utility method, used for `mail_with_image` and `mail_with_file`"""

        # maintype = 'image' for sending image
        # maintype = 'application' for sending files like pdf

        if maintype == 'application':
            with open(file_to, f_opration) as file_send:
                f_read = file_send.read()
                n = file_send.name
                if OS_SEP in n:
                    f_name = n.split(OS_SEP)[-1]
                else:
                    f_name = file_send.name
            _msg.add_attachment(
                f_read, maintype=maintype, subtype='octet-stream', filename=f_name)
        if maintype == 'image':
            with open(file_to, f_opration) as img_send:
                img_read = img_send.read()
                f_type = imghdr.what(img_send.name)
                n = img_send.name
                if OS_SEP in n:
                    f_name = n.split(OS_SEP)[-1]
                else:
                    f_name = img_send.name
            _msg.add_attachment(
                img_read, maintype=maintype, subtype=f_type, filename=f_name)

    def mail_with_image(self, image: list, port=25):
        """Send mail together with an image"""

        self.check_required()

        if len(self.to_receiver) > 1:
            # if the list of to_receiver is more than one
            for receiver in self.to_receiver:
                msg = EmailMessage()
                msg['From'] = self.from_sender_addr
                msg['To'] = receiver
                msg['Subject'] = self.mail_msg.split('\n')[0][9:]
                msg['Date'] = email.utils.formatdate(localtime=True)
                msg['Message-ID'] = email.utils.make_msgid()
                msg.set_content(self.mail_msg.split('\n')[2])

                if type(image) == list:
                    # send message with more than one image
                    for my_img in image:
                        self.file_to_send(
                            my_img, 'rb', _msg=msg, maintype='image')
                    self.mail_open(msg, port)
                else:
                    LOGGER.error(f'only list can be pass as argument in {self.mail_with_image}')
        elif len(self.to_receiver) == 1:
            msg = EmailMessage()
            self.mail_head(msg)
            msg.set_content(self.mail_msg.split('\n')[2])

            if type(image) == list:
                # send message with more than one image, for only one destination
                for my_img in image:
                    self.file_to_send(my_img, 'rb', _msg=msg, maintype='image')
                self.mail_open(msg, port)
            else:
                LOGGER.error(f'only list can be pass as argument in {self.mail_with_image}')

    def mail_with_file(self, mail_files: list, port=25):
        """Send mail together with a list of mail_files"""

        self.check_required()

        msg = EmailMessage()
        self.mail_head(msg)
        msg.set_content(self.mail_msg.split('\n')[2])

        for a_file in mail_files:
            self.file_to_send(a_file, 'rb', _msg=msg, maintype='application')
        self.mail_open(msg, port)

    def mail_with_page(self, file: "String | list", port=25):
        """Send mail with html page. You can pass a keyword args of `file='default'` which will send a default html page provided within this class method, that is for test.

        But if you want to send yor own html page assign the `file` with a value of the absolute location of your html page
        """

        self.check_required()

        msg = EmailMessage()
        self.mail_head(msg)
        msg.set_content(self.mail_msg.split('\n')[2])

        if file != "test" and type(file) != list:
            raise UnboundLocalError(f'`file` must be either `test` for testing, or list of page(s)')

        if file == "test":
            dummy_page = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Document</title>
</head>
<body>
  <h1 style="color:SlateGray;">Hello world mail from {self.from_sender_addr}</h1>
  <p style="color:brown;">Lorem ipsum dolor sit amet consectetur adipisicing elit. Rerum voluptate ipsum voluptatum doloribus, incidunt totam doloremque quae quibusdam exercitationem sapiente vel veritatis consequuntur earum et. Quod nobis minus minima repellat.</p>
</body>
</html>
'''
            msg.add_alternative(dummy_page, subtype='html')
        else:
            for f_l in file:
                with open(f_l) as f_html:
                    html_f = f_html.read()
                msg.add_attachment(html_f, subtype='html')
        self.mail_open(msg, port)
        
        
def ok(msg):
    """It is ok"""
    
    print(msg + ' ', end='', flush=True)
    num = 0
    for _ in range(3):
        num += 1
        time.sleep(0.3)
        print('.', end='', flush=True)
    print(' OK')
    time.sleep(1)


class FetchPOP:
    """Fetch POP mail, it downloads the emails in the `inbox folder` on the email server to your device. This means that POP3 doesn't retrieve emails located in other folders such as `Sent, Draft, custom folders` and so on.
    """

    def __init__(self, sender, password):
        """Kyaah POP init"""

        self.sender = sender
        self.passwd = password

        _t_ = sender.split('@')[-1]
        svr = _t_.split('.')[0]
        self.svr = svr

        self.mail_box = None

    def conn(self):
        """Making connection"""

        s_mail = Serve.mail(self.svr)

        if s_mail['server'][1] == 'icloud':
            log_style('Not supported')
            raise PermissionError
        
        # Connect to the mail box
        mail_box = poplib.POP3_SSL(s_mail['server'][1], s_mail['port'][2])
        mail_box.user(self.sender)
        mail_box.pass_(self.passwd)
        self.mail_box = mail_box

    def count(self):
        """Fetch POP mail (count), it result is tuple of 2 ints (message count, mailbox size)."""
        
        self.conn()
        return self.mail_box.stat()
    
    def fetch(self, n: int = None):
        """Fetch POP mail (fetch)
        `n` is a message number, when a message number argument is given is a single response: the "scan listing" for that message.
        """
        
        if type(n) == int or n == None:
            pass
        else:
            return False
        
        self.conn()
        NumofMessages = len(self.mail_box.list()[1])
        _list_1 = []

        if n == None:
            for i in range(NumofMessages):
                _list_2 = []
                for msg in self.mail_box.retr(i+1)[1]:
                    _list_2.append(msg)
                _list_1.append(_list_2)
        else:
            for msg in self.mail_box.retr(n+1)[1]:
                _list_1.append(msg)

        if len(_list_1) == 0:
            log_style('unable to get mail', col='yellow')
        else:
            log_style('it\'s ok')
            ok('[+] Well')
        self.mail_box.quit()
        return _list_1
    

class FetchIMAP:
    """Fetch IMAP mail

    It enables us to take any action such as downloading, delete the mail without reading the mail.It enables us to create, manipulate and delete remote message folders called mail boxes.

    IMAP enables the users to search the e-mails.

    It allows concurrent access to multiple mailboxes on multiple mail servers.
    """

    def __init__(self, sender, password):
        """Kyaah IMAP init"""

        self.sender = sender
        self.passwd = password

        _t_ = sender.split('@')[-1]
        svr = _t_.split('.')[0]
        self.svr = svr

        self.imapp = None

    def conn(self):
        """Making connection"""

        s_mail = Serve.mail(self.svr)
        # connect to host using SSL
        imap = imaplib.IMAP4_SSL(s_mail['server'][2], s_mail['port'][3])
        # login to server
        imap.login(self.sender, self.passwd)
        self.imapp = imap

    def folder(self, folder: str='Inbox', see: bool = False) -> list:
        """Fetch IMAP mail folder
        
        :see: if true, it will loop over the folders and display them on terminal

        it return list of mail folders
        """
        
        self.conn()
        # it helps to select a mailbox to access the messages
        status, b = self.imapp.select(folder)

        if status == 'OK':
            ok('Processing mailbox, status:')
        else:
            log_style(
                f'ERROR: Unable to open mailbox, status: status folder: {folder}', col='yellow')
            sys.exit()

        if see:
            print('Folders:\n')
        _list_1 = self.imapp.list()
        _list_2 = []

        for f in _list_1[1]:
            a = f.decode().replace('\\', '')
            b = a.replace('"/"', '==>')
            if see:
                print(b)
                print()
            _list_2.append(b)
        return _list_2
    
    def fetch(self, folder: str='Inbox', query='ALL') -> list:
        """Fetch IMAP mail, it fetches mails in the order (from old to newers).

        NOTE: The `folder` kwargs is to specify which folder to query, by default it will query from Inbox.
            when pass folder name like:
                [Gmail]/All Mail
            ensure to wrapp it with double qoute "" to avoid error, like:
                folder='"[Gmail]/All Mail"'

                others:
                    folder='Inbox'
                    folder="INBOX"
                    folder="Trash"
                    folder='"[Gmail]/All Mail"'
                    folder='"[Gmail]/Drafts"'
                    folder='"[Gmail]/Important"'
                    folder='"[Gmail]/Sent Mail"'
                    folder='"[Gmail]/Spam"'
                    folder='"[Gmail]/Starred"'
                    folder='"[Gmail]/Trash"'

        NOTE: The `query` kwargs is to specify what to query, by default it will query all.
            To get for specific mails by sender:
                query='FROM "googlealerts-noreply@google.com"'

            To get mails by subject:
                query='SUBJECT "Thanks for Subscribing to our Newsletter !"'

            To get mails after a specific date:
                query='SINCE "01-JAN-2020"'

            To get mails before a specific date:
                query='BEFORE "01-JAN-2020"'
        """

        self.conn()
        # select mailbox
        _status_, data = self.imapp.select(folder)
        if _status_ == 'OK':
            ok('Searching mailbox, status:')
        else:
            log_style(
                f'ERROR: Unable to search mailbox, status: {_status_} folder: {folder}', col='yellow')
            sys.exit()

        # search query
        status_, messages = self.imapp.search(None, query)
        log_style(f'There is {len(messages[0].split())} emails found!')
        _list_1 = []

        for num in messages[0].split():
            _list_2 = []
            _status, msg = self.imapp.fetch(num, '(RFC822)')
            for d in msg[0][1].decode().split('\r\n'):
                _list_2.append(d)
            _list_1.append(_list_2)
        self.imapp.close()
        return _list_1

    def create(self, folder):
        """It is used to create mailbox with a specified name"""

        self.conn()
        _status, data = self.imapp.create(folder)
        if _status == 'OK':
            ok('Creating mailbox, status:')
        else:
            log_style(
                f'ERROR: Unable to create mailbox, status: {_status} folder: {folder}', col='yellow')
            sys.exit()
        
    def rename(self, old_box, new_box):
        """It is used to change the name of a mailbox"""

        self.conn()
        _status, data = self.imapp.rename(old_box, new_box)
        if _status == 'OK':
            ok('Renaming mailbox, status:')
        else:
            log_style(
                f'ERROR: Unable to rename mailbox, status: {_status} folder: {old_box}', col='yellow')
            sys.exit()
        
    def delete(self, folder):
        """It is used to permanently delete a mailbox with a given name"""

        self.conn()
        _status, data = self.imapp.delete(folder)
        if _status == 'OK':
            ok('Deleting mailbox, status:')
        else:
            log_style(
                f'ERROR: Unable to delete mailbox, status: {_status} folder: {folder}', col='yellow')
            sys.exit()
        
    def logout(self):
        """This command informs the server that client is done with the session. The server must send BYE untagged response before the OK response and then close the network connection
        """

        self.conn()
        _status, data = self.imapp.logout()
        if _status == 'BYE':
            ok(f'Logging out mailbox, status: {_status}')
        else:
            log_style(f'ERROR: Unable to logout mailbox, status: {_status}', col='yellow')
            sys.exit()
