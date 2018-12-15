# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 23:13:14 2018

@author: Hesam
"""
import csv
f = open("books.csv")
books = csv.reader(f)

for isbn, title, author, year in books:
     print(f"Book with isbn number {isbn}, title{title} writtern by {author} in year{year} inserted to database.")