import os

from flask import Flask, session,render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from User import user

app = Flask(__name__)

# Check for environment variable
if not os.getenv('DATABASE_URL'):
    raise RuntimeError('DATABASE_URL is not set')

# Configure session to use filesystem
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Set up database
engine = create_engine(os.getenv('DATABASE_URL'))
db = scoped_session(sessionmaker(bind=engine))

@app.route('/',methods = ["GET","POST"])
def index():
    if request.method == 'POST':
         username = request.form['username']
         password = request.form['password']
         
         
#         password_hash = generate_password_hash(password)
         
         if db.execute("SELECT username FROM readers WHERE username=:username", {"username":username}).rowcount == 0:
            return render_template("error.html", message="Your Username is Invalid", username=username)
         else:
             db_pass = (db.execute("SELECT password FROM readers WHERE username=:username", {"username":username}).fetchone())[0]
             if db_pass == password :
                     session['user'] = username
                     return redirect(url_for('search'))
             
             return render_template("error.html", message="Your Password is Invalid", username=username)
     
    return render_template('index.html')
    


#@app.route('/siupform')
#def siupform():
#    render_template('signup.html')

@app.route('/signup', methods = ["GET","POST"])
def signup():
    if request.method == 'POST':
        
        try:   
        # get the user details from the form
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            
    
            # hash the password
    #        password = generate_password_hash(password)
            
            db.execute("INSERT INTO readers (username,password,email) VALUES (:username, :password, :email)", {'username':username, 'password':password, 'email':email})
            db.commit()
            
    #        flash(f'Dear {username} Thanks for signing up please login')
            
            return render_template('rgstr.html', user = username)
        except:
            return render_template("error.html", message="Your cannot use this Username", username="Reader")
    
    # it's a GET request, just render the template
    return render_template('signup.html')

@app.route('/search', methods = ["GET", "POST"])
def search():
    book_list = []
    if request.method == 'POST':
        try:
            isbn = request.form['isbn']
            title = request.form['title']
            author = request.form ['author']
            
#            title = title.split()
#            title = " ".join([title.capitalize() for t in title])
#            
#            author = author.split()
#            author = " ".join([author.capitalize() for a in author])
            
            
            if isbn == "" and title == "":
                book_list = db.execute("SELECT * FROM books WHERE author =:author", {"author": author}).fetchall()
                return render_template('srch_rslt.html', book_list = book_list)
            elif isbn == "" and author == "":
                book_list = db.execute("SELECT * FROM books WHERE title = :title", {"title": title}).fetchall()
                return render_template('srch_rslt.html', book_list = book_list)
            elif author == "" and title == "":
                book_list = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchall()
                return render_template('srch_rslt.html', book_list = book_list)
            else:
                book_list = db.execute("SELECT * FROM books WHERE (isbn, title, author) VALUES (:isbn, :title, :author)", {"isbn": isbn, "title": title, "author":author}).fetchall()
                return render_template('srch_rslt.html', book_list = book_list)
        except:
            return render_template("errorsrch.html", message="No Search result")
    return render_template('signin.html')

@app.route('/book')
def book():
    return render_template('book.html')

@app.route('/rgstr')
def rgstr_user():
        return render_template('rgstr.html')

        
if __name__ == "__main__":
   app.run()