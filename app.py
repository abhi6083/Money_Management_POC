from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)

def query_db(query, args=(), one=False):
    conn = sqlite3.connect('business.db')
    cur = conn.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    conn.close()
    return (rv[0] if rv else None) if one else rv

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/api/data")
def get_data():
    # Revenue
    revenue_data = [["Month", "Revenue", "Expenses"]] + query_db("SELECT month, revenue, expenses FROM revenue")

    # Sales Category
    sales_data = [["Category", "Sales"]] + query_db("SELECT category, amount FROM sales")

    # Cash Flow
    cash_flow_data = [["Month", "Cash Inflow", "Cash Outflow"]] + query_db("SELECT month, inflow, outflow FROM cashflow")

    # Top Customers
    top_customers = [["Customer", "Revenue"]] + query_db("SELECT customer_name, amount FROM customers")

    # Inventory Levels
    inventory_data = [["Product", "Quantity"]] + query_db("SELECT product, quantity FROM inventory")

    # Daily Transactions
    daily_transactions = [["Day", "Transactions"]] + query_db("SELECT day, transactions FROM transactions")

    # Profit Margin
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

if __name__ == "__main__":
    app.run(debug=True)
