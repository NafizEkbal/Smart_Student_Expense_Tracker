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
