# -*- coding: utf-8 -*-
import os
from . import BaseMail


class Vault(BaseMail):
    """This class handle environment variable information
    
    use this class if you want to access your `mail address` and `password` from environment variable, all what you need is to put your `mail address environment variable` in place of your email address, like-wise the password too!
    """
    
    @property
    def from_sender_addr(self):
        """Get sender mail address from environment variable"""

        return os.environ.get(self.from_sender)
    
    @property
    def password_env(self):
        """Get sender mail password/app_password from environment variable"""
        
        return os.environ.get(self.password)
