# -*- coding: utf-8 -*-
import json
import math
import random
import geocoder
import requests
# from itsdangerous import Serializer #(itsdangerous==2.1.2)
# from itsdangerous.serializer import Serializer #(itsdangerous==2.1.2)
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer #(itsdangerous==0.24)


class IzItDanger:
    """IzItDanger class for generating salting 🤔
    
    A reqular expression that matches any character that
    should never appear in base 64 encodings would be:
    [^A-Za-z0-9+/=]

    we follow the base64 pattern of [^A-Za-z0-9+/=] that should never appear in base64, (in regex)

    NOTE: usage:
        >>> pass_cls = IzItDanger()
        >>> pass_salt = pass_cls._salt
        >>> print(pass_salt)
    """

    token_sm_alpha = "abcdefghijklmnopqrstuvwxyz"
    token_cap_alpha = token_sm_alpha.upper()
    token_num = "0123456789"
    # token_char = "/+="
    token_sum = token_sm_alpha + token_cap_alpha + token_num

    # We times the above variable (token_sum) by 2 (total length is 124),
    # so that we will randomly select from it without any restriction,
    # since we make the minimum length of the salt to be 32 and the maximum to be 64,
    # and also it will randomly select from that range of (32 - 64)

    token_times = token_sum * 2
    token_list = list(token_times)
    random.shuffle(token_list) # shuffling the above list
    token_generate = "".join(token_list)
    
    def __init__(self, token_generate = token_generate):
        self.token_generate = "".join(token_generate)
        
    @property
    def _salt(self):
        """Salting with this class method

        By using the random sample method, where we make:
            population = self.token_generate
            k = random.randint(32, 64)
        """

        salt = "".join(random.sample(self.token_generate, random.randint(32, 64)))
        return salt # return type is string
    
    @staticmethod
    def get_token(mysecret, secret_key, expires_min=1):
        """Get token"""

        s = Serializer(secret_key, expires_min * 60)
        # s = Serializer(secret_key) #(itsdangerous==2.1.2)
        # mysecret = IzItDanger()._salt
        # return s.dumps([1,2,3,4])
        # return s.dumps("mysecret")
        return s.dumps(mysecret)
    
    @staticmethod
    def verify_token(secret_key, token):
        """Verify token (sign)"""

        s = Serializer(secret_key)
        try:
            load_token = s.loads(token)
        except:
            return None
        return load_token
    
    def __str__(self):
        """Dunder str"""

        return f"IzItDanger class"
    

class Tokens:
    """The base class for Tokens. It really work for python app, and secret key must be provided."""

    def __init__(self): ...
    
    def mail_otp(self, _range=6):
        """Send otp code"""

        digits = "0123456789"
        OTP = ""
        for _ in range(_range):
            OTP += digits[math.floor(random.random()*10)]
        return OTP
    
    @staticmethod
    def link(mysecret, age=1):
        """Method that ease making link session age

        Usage:
            >>> import kyaah
            >>> url = "https://kyaah.readthedocs.io"
            >>> tokenised_link = kyaah.Tokens.link(url)
        
            >>> payload = dict(
            >>>     sender = "myemail@gmail.com",
            >>>     receiver = ["receiver@gmail.com"],
            >>>     subject = "Kyaah link age utility",
            >>>     body = "Hi! you can follow this link {l} and update your password, it will expire in 60 seconds. Thank you!",
            >>>     password = "*********",
            >>> )

            >>> print(tokenised_link)
            >>> secret = tokenised_link[0]
            >>> data = tokenised_link[1]
            
            >>> mail = kyaah.send(credentials=payload)
            >>> print(kyaah.Tokens.unlink(secret, data))
            
        Make sure to save the `secret` some where safe (database, private repository, etc).
        And the `data` is the encode data with a session age (default is 1-minute).

        In real, it could be use if want to reset email address, by given amount of time, that the link will be expired!
        """

        secret = IzItDanger()._salt
        d = IzItDanger.get_token(mysecret, secret, age)
        return [secret, d]
    
    @staticmethod
    def unlink(secret_key, token):
        """Method that ease unlinking session age

        Usage:
            >>> import kyaah
            >>> secret = "***********"
            >>> data = "***********"
            >>> tokenised_unlink = kyaah.Tokens.unlink(secret, data)
        """

        # secret = IzItDanger()._salt
        d = IzItDanger.verify_token(secret_key, token)
        return d
    

class Faker:
    """Class that give you random email address"""
    
    _source = [
        "https://www.guerrillamail.com/ajax.php?f=get_email_address&ip=",
        "&agent=Mozilla_foo_bar"
    ]
    
    def __init__(self, url=_source, ip="me"):
        """Faker init"""

        self.url = url
        self.ip = ip

    def what_ip(self):
        """Find ip address of the requester"""

        g = geocoder.ip(self.ip).raw
        ip = g.get("ip")
        return ip
    
    @property
    def make_request(self):
        """This method make a request along side with an ip address from `what_ip` method of this class."""

        url_first = self.url[0]
        url_mid = self.url[1]
        url_end = self.what_ip()
        
        com_url = url_first + url_end + url_mid
        r = requests.get(com_url).text
        return r
    
    def faker(self) -> dict:
        """Give the actual maill address generated from guerrillamail"""

        gue_raw = json.loads(self.make_request)
        _fake = gue_raw["email_addr"]
        return {"fake_email": _fake}
    
    
# from itsdangerous import TimestampSigner as ts
# s = ts("secretkey")
# string = s.sign("foo")
# s.unsign(string, max_age=5)
