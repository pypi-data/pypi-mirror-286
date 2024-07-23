# -*- coding: utf-8 -*-
from . import Serve
from . import Faker
from . import Tokens
from rgbpy import log_style
from .utils import vault
from .base import LOGGER, BaseMail, FetchPOP, FetchIMAP


def send(include: str = "plain", local: "False | True" = False, credentials: dict = None):
    """This send function for sending any kind of mail operation, being it:
        :local mail
        :plain mail,
        :mail with attach image,
        :mail with attach file,
        :mail with attach html page,
        
    In the case of sending local mail, over-write the value of the `local` to `True`

    `include` is what should be included in the mail (image, file, or page):
    
    Usage:
        >>> import kyaah
        
        >>> payload = dict(
        >>>     sender = myemail@gmail.com,
        >>>     receiver = ["receiver@gmail.com"],
        >>>     subject = "Hellow world!",
        >>>     body = "Lorem ipsum dolor sit amet adipisicing elit, rerum voluptate ipsum volupt.",
        >>>     password = "**********",
        >>> )
        
        
        >>> # NOTE for sending local mail
            ::To test your mail locally, first boot up the python mail server on a different terminal by:
                `python3 -m smtpd -c DebuggingServer -n localhost:1025`
                then open another terminal and run your python script including the code above.
        >>> kyaah.send(local=True, credentials=payload)
        
        
        >>> # NOTE for sending a simple SMTP mail
        >>> kyaah.send(credentials=payload)
        
        
        >>> # NOTE for sending simple mail with image(s)
        >>> payload["image"] = ["/home/user/Desktop/media/image1.jpg", "/home/user/Desktop/media/image2.jpg"]
        >>> kyaah.send(include='image', credentials=payload)
        
        
        >>> # NOTE for sending simple mail with file(s)
        >>> payload["file"] = ["requirements.txt", "helloworld.py", "/home/user/Desktop/media/image1.jpg"]
        >>> kyaah.send(include='file', credentials=payload)
        
        
        >>> # NOTE for sending simple mail with page
        >>> payload["page"] = ["/home/user/Desktop/index.html"]
        >>> kyaah.send(include='page', credentials=payload)
    """
    
    try: env = credentials["env"]
    except: env = False

    if env == True:
        auth = vault(credentials["sender"], credentials["password"])
        credentials["sender"] = auth[0]
        credentials["password"] = auth[1]
        
    _em_ = credentials["sender"]
    _t_ = _em_.split("@")[-1]
    svr = _t_.split(".")[0]
    s_mail = Serve.mail(svr)

    if local == True: mail_server = "localhost"
    else: mail_server = s_mail["server"][0]
    
    base = BaseMail(
        **credentials,
        # slicing the first index of the server list, even though it's only one item
        server = mail_server
    )
    
    if local == True:
        try:
            # slicing the first index of the port list, even though it's only one item
            base.local_mail(port=credentials["port"])
        except:
            base.local_mail()
    else:
        # slicing the first index of the port list, even though it's only one item
        prt = s_mail['port'][0]
        
        if include == "plain":
            base.send_mail(port=prt)
        elif include == "image":
            try: image = credentials["image"]
            except: raise KeyError("A missing credential found `image`")
            base.mail_with_image(image, port=prt)
        elif include == "file":
            try: file = credentials["file"]
            except: raise KeyError("A missing credential found `file`")
            base.mail_with_file(file, port=prt)
        elif include == "page":
            try: page = credentials["page"]
            except: raise KeyError("A missing credential found `page`")
            base.mail_with_page(file=page, port=prt)
        else:
            raise ValueError("`include` value must be either [image, file, page]")
        
        
def fetch(maa: str = "pop", credentials: dict = None):
    r"""Fetch mail (POP) & (IMAP)

    ::`maa` (Message accessing agent), it should be either `pop` or `imap`
    
    Usage:
        >>> import kyaah

        >>> payload = dict(sender="myemail@gmail.com", password="**********")
        >>> f = kyaah.fetch(credentials=payload)

        >>> f.folder()
        >>> f.folder(see=True)
        >>> f.folder(see=True, folder='"[Gmail]/All Mail"')
        >>> f.folder(see=True, folder='"[Imap]/Trash"')
        
        >>> f.fetch('Inbox')
    """

    if maa.lower().strip() not in ["pop", "imap"]:
        raise ValueError("`maa` value must be either [pop, imap]")
    
    if maa == "pop":
        f = FetchPOP(**credentials)
    else:
        f = FetchIMAP(**credentials)
    return f


def fk(style: "False | True" = True):
    """This function generate a random email address for you."""

    if style == False:
        LOGGER.info(Faker().faker())
    else:
        log_style(Faker().faker())


def otp(_range: int = None):
    """This function give you a random OTP code."""

    if _range:
        return Tokens().mail_otp(_range)
    return Tokens().mail_otp()
