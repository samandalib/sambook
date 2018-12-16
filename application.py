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
    '''
    this function is the home page of web application and gets the username and password for log in,
    it search in database in https://adminer.cs50.net for the username and password and if the user exists
    returns the search page to the user, else it will direct to an error page for invalisd username/password
    '''
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
    '''
    This function is for sign up to the application, in the POST method it gets the user properties from the html form and insert it to the 'reader' table 
    on the database, if the user does not enter any of the required fields, it will be directed to an error.html page. In the GET method it only
    renders the signup.html page
    '''
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
    
    '''
    this function checks to see if there is a user in session dictionary, if there is, it checks to see if the request method is 
    POST, if it is it will search the database according to the inputs of the user, else, it will just show the search form. If it finds any
    row in database in coordination with the user inputs, it will represent it using the srch_rslt.html, else it will render errorsrch.html.
    If there user is not in session, it will render an error page saying not Loged in.
    '''
    
    if 'user' in session:
        username = session['user']
        book_list = []
        if request.method == 'POST':
            try:
                isbn = request.form['isbn']
                title = request.form['title']
                author = request.form ['author']
                          
                if isbn == "" and title == "":
                    book_list = db.execute("SELECT * FROM books WHERE author = :author", {"author": author}).fetchall()
                    return render_template('srch_rslt.html', book_list = book_list, user=username)
                elif isbn == "" and author == "":
                    book_list = db.execute("SELECT * FROM books WHERE title = :title", {"title": title}).fetchall()
                    return render_template('srch_rslt.html', book_list = book_list, user=username)
                elif author == "" and title == "":
                    book_list = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchall()
                    return render_template('srch_rslt.html', book_list = book_list, user=username)
                else:
                    book_list = db.execute("SELECT * FROM books WHERE (isbn, title, author) VALUES (:isbn, :title, :author)", {"isbn": isbn, "title": title, "author":author}).fetchall()
                    return render_template('srch_rslt.html', book_list = book_list, user=username)
            except:
                return render_template("errorsrch.html", message="No Search result", username=username)
        
        return render_template('signin.html', user=username)

    else:
        return render_template("error.html", message="You are not Logged In")

@app.route("/logout")
def logout():
    '''
    if the user clicks on the Log Out link in any pages, it will call this function that will end the session and log out the user
    '''
    if 'user' in session:
        session.pop('user')
        return render_template('logout.html')

@app.route('/book')
def book():
    return render_template('book.html')

@app.route('/rgstr')
def rgstr_user():
        return render_template('rgstr.html')

        
if __name__ == "__main__":
   app.run()