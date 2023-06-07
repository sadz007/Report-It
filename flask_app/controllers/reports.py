from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.m_users import User
from flask_app.models.m_reports import Report
from flask_app.controllers import users
import time 

####### RENDERING AND GET METHODS #####

@app.route("/report/home")
def home():
    if "user_id" not in session:
        flash("BOOOOOOOM You Need to Register !!")
        return redirect("/")
    
    user = User.get_id(session["user_id"])
    
    reports = Report.get_all_reports()

    return render_template("dashboard.html", user=user, reports=reports)


@app.route("/report/create")
def report_create():
    user = User.get_id(session["user_id"])
    return render_template("create_report.html",user=user)



@app.route("/report/<int:id>")
def show_report(id):
    user = User.get_id(session["user_id"])
    report = Report.get_report_id(id)

    return render_template("show_report.html", user = user, report=report)

@app.route("/report/edit/<int:id>")
def edit_report(id):
    report = Report.get_report_id(id)

    return render_template("edit_report.html", report=report)


### POSTING METHODS AND FORM REQUEST ###

@app.route("/report", methods=["POST"])
def create_my_report():
    
    report = Report.create_report(request.form)

    if report:
        return redirect(f"/report/{report}")
    
    return redirect(f"/report/create")


@app.route("/report/update/<int:id>", methods = ["POST"])
def report_update(id):
    report = Report.update_report(request.form, session["user_id"])

    if not report:
        return redirect(f"/report/edit/{id}")
    return redirect(f"/report/{report}")

@app.route("/report/delete/<int:id>")
def delete_my_report(id):
    Report.delete_report(id)
    return redirect("/report/home")