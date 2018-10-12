from flask import render_template, url_for, request, redirect, session
from app import webapp

@webapp.route("/logout")
def LogOut():
    session["error"] = None
    return redirect(url_for("SignIn"))