from flask import render_template, url_for, request, redirect, session
from app import webapp

test_image = ["background1.jpg","background2.jpg","background3.jpg"]

@webapp.route("/homepage")
def HomePage():
    title = "Imager"
    if session["authenticated"]:
        if "username" in session:
            title = session["username"]
        return render_template("homepage.html",title = title,images = test_image)
    else:
        session["error"] = "unauthenticated log In"
        return redirect(url_for("SignIn"))