from flask import Blueprint,request,render_template,session,redirect,url_for
from db import get_db_connection

transaction = Blueprint("transaction",__name__)

@transaction.route("/add_transaction", methods=['POST','GET'])
def add_transaction():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
        
    if request.method == "POST":
        title = request.form.get("title")
        amount = request.form.get("amount")
        category = request.form.get("category")
        transactionType = request.form.get("transactionType")
        note = request.form.get("note") or None

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO transactions (user_id,title,amount,category,transaction_type,note) VALUES (%s,%s,%s,%s,%s,%s)",(session["user_id"],title,amount,category,transactionType,note))
        conn.commit()
        return redirect(url_for("dashboard.home"))

    return render_template("add_transaction.html")  


@transaction.route("/income")
def income():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `transactions` WHERE transaction_type = 'income' and user_id = %s ORDER BY created_at DESC",(session["user_id"],))
    income = cursor.fetchall()

    return render_template("income.html",income = income)


@transaction.route("/expense")
def expense():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `transactions` WHERE transaction_type = 'expense' and user_id = %s ORDER BY created_at DESC",(session["user_id"],))
    expense = cursor.fetchall()

    return render_template("expense.html",expense = expense)


@transaction.route("/edit_transaction/<int:id>", methods = ['POST','GET'])
def edit_transaction(id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    action = request.form.get("action")
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM transactions WHERE user_id = %s AND id = %s",(session["user_id"],id))
    trans = cursor.fetchone()

    if action == "delete":
        cursor.execute("DELETE FROM transactions WHERE user_id= %s AND id= %s",(session["user_id"],id))
        conn.commit()
        return redirect(url_for("dashboard.home"))

    if action == "update":
        title = request.form.get("title")
        category = request.form.get("category")
        transactionType = request.form.get("transactionType")
        amount = request.form.get("amount")
        note = request.form.get("note")

        cursor.execute("UPDATE transactions SET title=%s, category=%s, transaction_type=%s, amount=%s, note=%s WHERE user_id= %s AND id= %s",(title, category, transactionType, amount, note, session["user_id"], id))
        conn.commit()
        return redirect(url_for("dashboard.home"))

    print(trans)
    return render_template("edit_transaction.html",transaction = trans)