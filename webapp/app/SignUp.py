from flask import render_template, url_for, request, redirect, session
from app import webapp

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
    session["email"] = request.form["email"]
    
    if "password" in request.form and "com_password" in request.form:
        if request.form["password"] == "" or request.form["com_password"] == "":
            error += "Please enter the password or password comfirm.\n"
        elif request.form["password"] != request.form["com_password"]:
            error += "password doesn't match the comfirm password.\n"        
    
    if error != "":
        session["error"] = error
        return redirect(url_for("SignUp"))
    else:
        session['authenticated'] = True
        return redirect(url_for("HomePage"))
