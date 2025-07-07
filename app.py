import os
import pandas as pd
from flask import Flask, render_template, jsonify, request, redirect, url_for
import sqlite3
import csv

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

def query_db(query, args=(), one=False):
    conn = sqlite3.connect('business.db')
    cur = conn.cursor()
    cur.execute(query, args)
    rows = cur.fetchall()
    conn.close()
    return (rows[0] if rows else None) if one else rows

@app.route("/dashboard-business")
def dashboard_business():
    return render_template("dashboard_business.html")

@app.route("/dashboard-account")
def dashboard_account():
    return render_template("dashboard_account.html")

@app.route("/")
def upload_page():
    return render_template("upload.html")

@app.route("/api/data")
def get_data():
    revenue_data = [["Month", "Revenue", "Expenses"]] + query_db("SELECT month, revenue, expenses FROM revenue")
    sales_data = [["Category", "Sales"]] + query_db("SELECT category, amount FROM sales")
    cash_flow_data = [["Month", "Cash Inflow", "Cash Outflow"]] + query_db("SELECT month, inflow, outflow FROM cashflow")
    top_customers = [["Customer", "Revenue"]] + query_db("SELECT customer_name, amount FROM customers")
    inventory_data = [["Product", "Quantity"]] + query_db("SELECT product, quantity FROM inventory")
    daily_transactions = [["Day", "Transactions"]] + query_db("SELECT day, transactions FROM transactions")
    profit_margin_data = [["Month", "Revenue", "Expenses", "Profit Margin %"]] + query_db("SELECT month, revenue, expenses, margin FROM profit")

    return jsonify({
        "revenue_expenses": revenue_data,
        "sales_category": sales_data,
        "cash_flow": cash_flow_data,
        "top_customers": top_customers,
        "inventory_levels": inventory_data,
        "daily_transactions": daily_transactions,
        "profit_margin": profit_margin_data
    })

@app.route("/upload-business", methods=["POST"])
def upload_business():
    file = request.files.get("file")
    if not file: return "No file provided", 400

    reader = csv.reader(file.read().decode("utf-8").splitlines())
    headers = next(reader)
    conn = sqlite3.connect("business.db")
    cur = conn.cursor()

    cur.execute("DELETE FROM revenue")
    cur.execute("DELETE FROM sales")
    cur.execute("DELETE FROM customers")
    cur.execute("DELETE FROM inventory")
    cur.execute("DELETE FROM profit")

    for row in reader:
        (
            month, revenue, expenses, _, _, profit_margin,
            category, category_amount,
            customer_name, customer_revenue,
            product, quantity, _, _
        ) = row + [None] * (14 - len(row))

        if month:
            cur.execute("INSERT INTO revenue (month, revenue, expenses) VALUES (?, ?, ?)", (month, revenue, expenses))
            cur.execute("INSERT INTO profit (month, revenue, expenses, margin) VALUES (?, ?, ?, ?)", (month, revenue, expenses, profit_margin))

        if category:
            cur.execute("INSERT INTO sales (category, amount) VALUES (?, ?)", (category, category_amount))

        if customer_name:
            cur.execute("INSERT INTO customers (customer_name, amount) VALUES (?, ?)", (customer_name, customer_revenue))

        if product:
            cur.execute("INSERT INTO inventory (product, quantity) VALUES (?, ?)", (product, quantity))

    conn.commit()
    conn.close()
    return redirect(url_for("dashboard_business"))

@app.route("/upload-account", methods=["POST"])
def upload_account():
    file = request.files["account_csv"]
    if file and file.filename.endswith(".csv"):
        file_path = "uploaded_account.csv"
        file.save(file_path)

        df = pd.read_csv(file_path)

        # Clean and parse
        df["DATE"] = pd.to_datetime(df["DATE"], errors='coerce')
        df = df.dropna(subset=["DATE"])
        df["WITHDRAWAL AMT"] = pd.to_numeric(df["WITHDRAWAL AMT"], errors="coerce").fillna(0)
        df["DEPOSIT AMT"] = pd.to_numeric(df["DEPOSIT AMT"], errors="coerce").fillna(0)

        df["Month"] = df["DATE"].dt.strftime("%b")
        df["Day"] = df["DATE"].dt.strftime("%a")

        cashflow_summary = df.groupby("Month")[["DEPOSIT AMT", "WITHDRAWAL AMT"]].sum().reset_index()
        cashflow_summary.columns = ["month", "inflow", "outflow"]

        transaction_summary = df.groupby("Day").size().reset_index(name="transactions")
        transaction_summary.columns = ["day", "transactions"]

        # Insert into SQLite
        conn = sqlite3.connect("business.db")
        cur = conn.cursor()

        cur.execute("DELETE FROM cashflow")
        cur.execute("DELETE FROM transactions")

        for _, row in cashflow_summary.iterrows():
            cur.execute("INSERT INTO cashflow (month, inflow, outflow) VALUES (?, ?, ?)",
                        (row["month"], row["inflow"], row["outflow"]))

        for _, row in transaction_summary.iterrows():
            cur.execute("INSERT INTO transactions (day, transactions) VALUES (?, ?)",
                        (row["day"], int(row["transactions"])))

        conn.commit()
        conn.close()

        os.remove(file_path)
        return redirect(url_for("dashboard_account"))

    return "Upload failed or unsupported file type", 400

if __name__ == "__main__":
    app.run(debug=True)
