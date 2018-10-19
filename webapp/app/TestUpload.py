from flask import render_template, url_for, request, redirect, session
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


@webapp.route("/test/FileUpload", methods=['GET'])
def testUpload():
    if "error" not in session:
        return render_template("testupload.html",error = None)
    else:
        return render_template("testupload.html",error = session["error"])


@webapp.route("/test/FileUpload", methods=['POST'])
def testUploadSubmit():
    if "userID" not in request.form or "password" not in request.form or \
       "uploadedfile" not in request.files:
        session["error"] = "upload form not compelete!"
        return redirect(url_for("testUpload"))
    myFile = request.files["uploadedfile"]
    cnx = sql.get_db()
    cursor = cnx.cursor()
    query = "SELECT * FROM user2Images WHERE userName = %s AND original = %s"
    cursor.execute(query,(request.form["userID"],os.path.join(os.path.join(webapp.config["UPLOAD_FOLDER"],request.form["userID"]),myFile.filename)))
    row = cursor.fetchone()
    if row != None:
        session["error"] = "Image with same name has already been uploaded!"
        return redirect(url_for("testUpload"))
    if myFile and allowed_file(myFile.filename):
        userPath = os.path.join(webapp.config['UPLOAD_FOLDER'],request.form["userID"])
        if not os.path.exists(userPath):
            os.makedirs(userPath)
        filename = secure_filename(myFile.filename)
        path_original = os.path.join(userPath,filename)
        myFile.save(path_original)
        path_thumbnail,path_a,path_b,path_c = ImageTransSave(userPath, filename)
        DBImageSave(request.form["userID"],path_thumbnail,path_original,path_a,path_b,path_c)
        session["error"] = "the file has been uploaded!"
        return redirect(url_for("testUpload")) 
    else:
        session["error"] = "can not recognize the file, please reupload"
        return redirect(url_for("testUpload"))
    
