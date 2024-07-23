# -*- coding: utf-8 -*-
"""
    ================================
    @ Kyaah software toolkit package
    ================================

          ,-.                                      ,---,     
      ,--/ /|                                    ,--.' |     
    ,--. :/ |                                    |  |  :     
    :  : ' /                                     :  :  :     
    |  '  /        .--,   ,--.--.      ,--.--.   :  |  |,--. 
    '  |  :      /_ ./|  /       \    /       \  |  :  '   | 
    |  |   \  , ' , ' : .--.  .-. |  .--.  .-. | |  |   /' : 
    '  : |. \/___/ \: |  \__\/: . .   \__\/: . . '  :  | | | 
    |  | ' \ \.  \  ' |  ," .--.; |   ," .--.; | |  |  ' | : 
    '  : |--'  \  ;   : /  /  ,.  |  /  /  ,.  | |  :  :_:,' 
    ;  |,'      \  \  ;;  :   .'   \;  :   .'   \|  | ,'     
    '--'         :  \  \  ,     .-./|  ,     .-./`--''       
                  \  ' ;`--`---'     `--`---'                
                   `--`                                      
    
    Kyaah abstract away cognitive over-head of sending SMTP mail, together with other mailing operations things like, mail with file, tokens etc.

    Usage at a glance:
        >>> import kyaah
        
        >>> payload = dict(
        >>>     sender = "myemail@gmail.com",
        >>>     receiver = ["receiver@gmail.com"],
        >>>     subject = "Hellow world!",
        >>>     body = "Lorem ipsum dolor sit amet adipisicing elit, rerum voluptate ipsum volupt.",
        >>>     password = "**********",
        >>> )

        >>> kyaah.send(credentials=payload)
        
    Kyaah uses SSL for email, because most of the servers like gmail, require SSL.
"""

from datetime import datetime

__title__ = 'kyaah'
__version__ = '0.1.16'
__author__ = 'Usman Musa'
__author_email__ = 'usmanmusa1920@gmail.com'
__author_website__ = 'https://usmanmusa1920.github.io'
__repository__ = 'https://github.com/usmanmusa1920/kyaah'
__url__ = 'https://kyaah.readthedocs.io'
__license__ = 'MIT'
__copyright__ = f'Copyright (C) 2022 - {datetime.today().year} Usman Musa'
__description__ = 'Kyaah abstract away cognitive over-head of sending SMTP mail, together with other mailing operations things like, mail with file, tokens etc.'


status_codes = {
    # Information.
    200: ("success",),
    # Client Error.
    400: ("bad_request",),
    401: ("unauthorized",),
    404: ("not_found",),
    # Server Error.
    500: ("internal_server_error",),
    503: ("service_unavailable",),
}


from .utils import Tokens
from .utils import Faker
from .server import Serve
from .api import send
from .api import fetch
from .api import fk
from .api import otp
