# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 21:10:39 2018

@author: Hesam
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import csv

    
engine = create_engine(os.getenv('DATABASE_URL'))
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    books = csv.reader(f)
    
    for isbn, title, author, year in books:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",{"isbn": isbn,"title": title, "author": author, "year": year})
        print(f"Book with isbn number {isbn}, title{title} writtern by {author} in year{year} inserted to database.")
    db.commit()

if __name__ == "__main__":
    main()