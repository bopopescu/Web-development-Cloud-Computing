from flask import render_template, url_for, request, redirect, session,g
from app import webapp
import mysql.connector
from app import config


def connect_to_database():
    return mysql.connector.connect(user=config.db_config['user'], 
                                   password=config.db_config['password'],
                                   host=config.db_config['host'],
                                   database=config.db_config['database'])

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db

@webapp.route("/signup", methods = ["GET","POST"])
def SignUp():
    username = None
    error = None
    email = None    
    if "username" in session:
        username = session["username"]
    if "error" in session:
        error = session["error"]
    if "email" in session:
        email = session["email"]
    return render_template("signup.html",title = "ImageBay", email = email, error = error, username = username)


@webapp.route("/signup_submit",methods = ["POST"])
def SignUpSubmit():
    error = ""
    if "username" in request.form:
        if request.form["username"] == "":
            error += "Please enter a username.\n"
        elif len(request.form["username"]) > 20:
            error += "The username is too long. Please retry.\n"
        for char in request.form["username"]:
            if char not in "ABCDEFJHIJKLMNOPQRSTUVWXYZabcdefjhijklmnopqrstuvwxyz0123456789_":
                error += "Username should only contain letters, numbers and '_'.\n"
                break
    session["username"] = request.form["username"]
        
    if "email" in request.form:
        if request.form["email"] == "":
            error += "Please enter the email address.\n"
    
    if "password" in request.form and "com_password" in request.form:
        if request.form["password"] == "" or request.form["com_password"] == "":
            error += "Please enter the password or password comfirm.\n"
        elif request.form["password"] != request.form["com_password"]:
            error += "password doesn't match the comfirm password.\n"
    session["password"] = request.form["password"]
    
    if error != "":
        session["error"] = error
        return redirect(url_for("SignUp"))
    else:
        session['authenticated'] = True
        

    cnx = get_db()
    cursor = cnx.cursor()

    query = ''' INSERT INTO userinfo (user_name, user_email, user_password)
                       VALUES (%s,%s,%s)
    '''
    
    cursor.execute(query,(session["username"],request.form["email"],request.form["password"]))
    cnx.commit()

    return redirect(url_for("HomePage"))
    
