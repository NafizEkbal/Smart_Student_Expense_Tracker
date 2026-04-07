from flask import Blueprint, session, render_template, redirect, url_for
from db import get_db_connection
dashboard = Blueprint("dashboard",__name__)


@dashboard.route("/home")
def home():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if "user_id" in session:
        cursor.execute(
            "SELECT * FROM users WHERE id=%s",(session["user_id"],)
            )
        user = cursor.fetchone()

        cursor.execute(
            "SELECT * FROM transactions WHERE user_id = %s ORDER BY created_at DESC LIMIT 5",(session["user_id"],)
            )
        transaction = cursor.fetchall() 
        print(transaction)

        cursor.execute(
            "SELECT SUM(amount) FROM transactions WHERE user_id= %s AND transaction_type= 'expense'",(session["user_id"],)
        )
        total_expense = cursor.fetchone()[0] or 0
        print(total_expense)

        cursor.execute(
            "SELECT SUM(amount) FROM transactions WHERE user_id= %s AND transaction_type= 'income'",(session["user_id"],)
        )
        total_income = cursor.fetchone()[0] or 0
        print(total_income)

        return render_template("home.html",user = user, transaction = transaction, total_expense = total_expense, total_income = total_income)
    return redirect(url_for("auth.login"))