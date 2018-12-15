# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 18:20:17 2018

@author: Hesam
"""

class User(object):
    def __init__(self,username,password,email):
        self.username=username
        self.password=password
        self.email=email
def user(username,password,email):
    return User(username,password,email)