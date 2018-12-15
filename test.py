# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 13:54:20 2018

@author: Hesam
"""

def domain_name(url):
    start = url.find(":")
    url = url[start+1:]
    dots = url.count(".")
    if dots == 2:
        ind1 = url.index(".")
        url = url[ind1+1:]
        ind2 = url.index(".")
        return url[:ind2]
    elif dots == 1:
        ind3= url.index(".")
        return url[:ind3]
        