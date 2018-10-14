from flask import render_template, url_for, request, redirect, session, flash, send_file
from app import webapp
import os
from app import sql

@webapp.route("/homepage/detail/<imgId>",methods = ["GET"])
def ImgDetail(imgId):
    if session["authenticated"]:
        cnx = sql.get_db()
        cursor = cnx.cursor()
        query = "SELECT * FROM user2Images WHERE userName = %s AND Thumbnail = %s"
        cursor.execute(query,(session["username"],imgId))
        row = cursor.fetchone()
        if row == None:
            flash("Can't find images, please reupload!")
            return redirect(url_for("HomePage"))
        images = [row[2],row[3],row[4],row[5]]
        return render_template("imgdetail.html",title = session["username"],images = images)
    else:
        session["error"] = "unauthenticated log In"
        return redirect(url_for("SignIn"))