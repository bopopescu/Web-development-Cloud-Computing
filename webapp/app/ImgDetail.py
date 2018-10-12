from flask import render_template, url_for, request, redirect, session
from app import webapp

@webapp.route("/homepage/detail")
def ImgDetail():
    title = None
    images = [None,None,None,None]
    if "original_img_path" in request.form:
        title = request.form["original_img_path"]
        images[0] = request.form["original_img_path"]
        images[1] = "1_" + request.form["original_img_path"]
        images[2] = "2_" + request.form["original_img_path"]
        images[3] = "3_" + request.form["original_img_path"]
    return render_template("imgdetail",title = title, images = images)