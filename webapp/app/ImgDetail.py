from flask import render_template, url_for, request, redirect, session
from app import webapp

testImage = ["background1.jpg","background2.jpg","background3.jpg"]

@webapp.route("/homepage/detail/<imgId>",methods = ["GET"])
def ImgDetail(imgId):
    title = "Imager"
    if session["authenticated"]:
        if "username" in session:
            title = session["username"]
        # get images from localserver   
        return render_template("imgdetail.html",title = title,images = testImage)
    else:
        session["error"] = "unauthenticated log In"
        return redirect(url_for("SignIn"))