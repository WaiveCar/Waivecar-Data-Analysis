from flask import Flask, render_template, request, redirect, url_for, flash, make_response, session, abort
import subprocess as sub
import os
from sqlalchemy.orm import sessionmaker
from table import *
engine = create_engine('sqlite:///tutorial.db', echo=True)

app = Flask(__name__, static_folder=os.getcwd())

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('home.html')
    else:
        return render_template('advertisers.html')
    
@app.route('/login', methods=['POST'])
def do_admin_login():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
    
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    result = query.first()
    if result:    
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path) 

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run()
    
