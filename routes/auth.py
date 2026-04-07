from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db_connection

auth = Blueprint("auth",__name__)



@auth.route("/")
def login():
    return render_template("login.html")

@auth.route("/login_validation",methods=["POST"])
def login_validation():
    email = request.form.get("email")
    password = request.form.get("password")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email= %s",(email,))
    exist_user = cursor.fetchone()

    
    if exist_user and check_password_hash(exist_user[3],password):
        session["user_id"] = exist_user[0]
        return redirect(url_for("dashboard.home"))

    flash("Invalid email or password!")
    return redirect(url_for("auth.login"))

@auth.route("/register")
def register():
    return render_template("register.html")

@auth.route("/add_user", methods =["POST"])
def add_user():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    confirmpass = request.form.get("confirmpass")

    if password != confirmpass:
        flash("Password does not match!")
        return redirect(url_for("auth.register"))

    cursor.execute("SELECT * FROM users WHERE email= %s",(email,))
    exist_user = cursor.fetchone()

    if exist_user:
        flash("Email already exist!")
        return redirect(url_for("auth.register"))

    hash_pass = generate_password_hash(password)

    cursor.execute(
        "INSERT INTO users (name,email,password) VALUES (%s, %s, %s)",(name,email,hash_pass)
        )
    conn.commit()
    session["user_id"] = cursor.lastrowid
    return redirect(url_for("dashboard.home"))

@auth.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("auth.login"))