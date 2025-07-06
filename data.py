import sqlite3

conn = sqlite3.connect('business.db')
c = conn.cursor()

# Revenue vs Expenses
c.execute("DROP TABLE IF EXISTS revenue")
c.execute("CREATE TABLE revenue (month TEXT, revenue INTEGER, expenses INTEGER)")
revenue_data = [
    ("Jan", 10000, 8000),
    ("Feb", 11700, 8600),
    ("Mar", 12500, 9000),
    ("Apr", 15300, 9700),
    ("May", 16500, 10300)
]
c.executemany("INSERT INTO revenue VALUES (?, ?, ?)", revenue_data)

# Sales by Category
c.execute("DROP TABLE IF EXISTS sales")
c.execute("CREATE TABLE sales (category TEXT, amount INTEGER)")
sales_data = [
    ("Electronics", 1100),
    ("Furniture", 700),
    ("Clothing", 460),
    ("Stationery", 250),
    ("Others", 300)
]
c.executemany("INSERT INTO sales VALUES (?, ?)", sales_data)

# Cash Flow
c.execute("DROP TABLE IF EXISTS cashflow")
c.execute("CREATE TABLE cashflow (month TEXT, inflow INTEGER, outflow INTEGER)")
cashflow_data = [
    ("Jan", 10000, 8000),
    ("Feb", 12000, 8600),
    ("Mar", 14000, 9100),
    ("Apr", 15000, 9300),
    ("May", 16000, 10200)
]
c.executemany("INSERT INTO cashflow VALUES (?, ?, ?)", cashflow_data)

# Top Customers
c.execute("DROP TABLE IF EXISTS customers")
c.execute("CREATE TABLE customers (customer_name TEXT, amount INTEGER)")
customer_data = [
    ("John", 10000),
    ("Alice", 8500),
    ("Ravi", 7400),
    ("Maria", 6200),
    ("Liu", 5600)
]
c.executemany("INSERT INTO customers VALUES (?, ?)", customer_data)

# Inventory
c.execute("DROP TABLE IF EXISTS inventory")
c.execute("CREATE TABLE inventory (product TEXT, quantity INTEGER)")
inventory_data = [
    ("Laptop", 30),
    ("Chair", 45),
    ("T-shirt", 60),
    ("Notebook", 75),
    ("Mouse", 40)
]
c.executemany("INSERT INTO inventory VALUES (?, ?)", inventory_data)

# Daily Transactions
c.execute("DROP TABLE IF EXISTS transactions")
c.execute("CREATE TABLE transactions (day TEXT, transactions INTEGER)")
transactions_data = [
    ("Mon", 50),
    ("Tue", 55),
    ("Wed", 52),
    ("Thu", 60),
    ("Fri", 65),
    ("Sat", 58),
    ("Sun", 62)
]
c.executemany("INSERT INTO transactions VALUES (?, ?)", transactions_data)

# Profit Margin
c.execute("DROP TABLE IF EXISTS profit")
c.execute("CREATE TABLE profit (month TEXT, revenue INTEGER, expenses INTEGER, margin INTEGER)")
profit_data = [
    ("Jan", 10000, 8000, 20),
    ("Feb", 11700, 8600, 26),
    ("Mar", 12500, 9000, 28),
    ("Apr", 15300, 9700, 37),
    ("May", 16500, 10300, 38)
]
c.executemany("INSERT INTO profit VALUES (?, ?, ?, ?)", profit_data)

conn.commit()
conn.close()
print("✅ Database initialized successfully.")
