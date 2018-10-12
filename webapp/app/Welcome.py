from flask import render_template, url_for
from app import webapp

#@webapp.route("/welcome")
@webapp.route("/",methods=["GET"])
def Welcome():
    #imageURL = url_for("static",filename = "background1.jpg")
    return render_template("welcome.html", title = "ImageBay")
