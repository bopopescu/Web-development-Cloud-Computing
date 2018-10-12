from flask import render_template, session, url_for, request, redirect, flash
from app import webapp

# temp user table
user_1 = {"username":"John","pwd":"123456"}
webapp.secret_key = '\x80\xa9s*\x12\xc7x\xa9d\x1f(\x03\xbeHJ:\x9f\xf0!\xb1a\xaa\x0f\xee'


@webapp.route("/signin",methods=['GET','POST'])
def SignIn():
    username = None
    error = None
    #imageURL = url_for("static",filename = "background2.jpg")
    if "username" in session:
        username = session["username"]
    if "resubmit" in session and session["resubmit"]:
        if "error" in session:
            error = session["error"]
            session["error"] = None

    session["resubmit"] = False
    return render_template("signin.html",title = "ImageBay",username=username,error=error)

@webapp.route("/signin_submit",methods=['POST'])
def SignInSubmit():
    if "username" in request.form and request.form["username"] == user_1["username"] \
    and "password" in request.form and request.form["password"] == user_1["pwd"]:
        session['authenticated'] = True
        session["username"] = request.form["username"]
        flash("You have successfully login!")
        return redirect(url_for("HomePage"))
    
    if 'username' in request.form:
        session["username"] = request.form["username"]

    session["resubmit"] = True
    session["error"] = "username or password incorrect!"
    return redirect(url_for("SignIn"))
