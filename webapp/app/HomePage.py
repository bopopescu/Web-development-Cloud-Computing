from flask import render_template, url_for, request, redirect, session, flash, send_file
from werkzeug.utils import secure_filename
from app import webapp
from wand.image import Image
import os
from app import sql
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def DBImageSave(userName,thumbnail,original,trans_a,trans_b,trans_c):
    cnx = sql.get_db()
    cursor = cnx.cursor()
    query = ''' INSERT INTO user2Images (userName, Thumbnail, original, trans_a, trans_b, trans_c)
                       VALUES (%s,%s,%s,%s,%s,%s)
    '''
    cursor.execute(query,(userName,thumbnail,original,trans_a,trans_b,trans_c))
    cnx.commit()

def allowed_file(filename):
    return filename.split(".")[-1] in ALLOWED_EXTENSIONS

def ImageTransSave(filePath,fileName):
    with Image(filename = os.path.join(filePath,fileName)) as img:
        with img.clone() as i:
            i.resize(width = 150,height = 100)
            path_thumbnail = os.path.join(filePath,"thumbnail_"+fileName)
            i.save(filename=path_thumbnail)
        with img.clone() as i:
            i.modulate(brightness = 100, saturation = 170, hue = 100)
            path_a = os.path.join(filePath,"a_"+fileName)
            i.save(filename=path_a)
        with img.clone() as i:
            i.modulate(brightness = 100, saturation = 100, hue = 50)
            path_b = os.path.join(filePath,"b_"+fileName)
            i.save(filename=path_b)
        with img.clone() as i:
            i.modulate(brightness = 80, saturation = 0, hue = 100)
            path_c = os.path.join(filePath,"c_"+fileName)
            i.save(filename=path_c)
    return path_thumbnail,path_a,path_b,path_c

@webapp.route("/homepage", methods=['GET', 'POST'])
def HomePage():
    images = []
    if "error" in session:
        error = session["error"]
    else:
        error = None
        session["error"] = None
    if session["authenticated"]:
        cnx = sql.get_db()
        cursor = cnx.cursor()
        query = "SELECT * FROM user2Images WHERE userName = %s"
        cursor.execute(query,(session["username"],))
        row = cursor.fetchall()
        if row == None:
            return render_template("homepage.html",title = session["username"],images = images, error = error)
        lens = len(row)
        for i in range(lens):
            file_name = row[i][1].split("/")[-1]
            images.append(os.path.join(os.path.join("upload_images",session["username"]),file_name))
        return render_template("homepage.html",title = session["username"],images = images, error = error)
    else:
        session["error"] = "unauthenticated log In"
        return redirect(url_for("SignIn"))

@webapp.route("/homepage/upload", methods=['GET', 'POST'])
def UpLoad():
    if 'my_file' not in request.files:
        session["error"] = "didn't receive any file please try again!"
        return redirect(url_for('HomePage'))
    myFile = request.files["my_file"]
    if myFile.filename == '':
        session["error"] = "No file selected"
        return redirect(url_for('HomePage'))
    if myFile and allowed_file(myFile.filename):
        userPath = os.path.join(webapp.config['UPLOAD_FOLDER'],session["username"])
        if not os.path.exists(userPath):
            os.makedirs(userPath)
        filename = secure_filename(myFile.filename)
        path_original = os.path.join(userPath,filename)
        myFile.save(path_original)
        path_thumbnail,path_a,path_b,path_c = ImageTransSave(userPath, filename)
        DBImageSave(session["username"],path_thumbnail,path_original,path_a,path_b,path_c)
        session["error"] = None
        return redirect(url_for('HomePage')) 
    else:
        session["error"] = "can not recognize the file, please reupload"
        return redirect(url_for("HomePage"))
