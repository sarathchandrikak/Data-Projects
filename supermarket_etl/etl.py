from kaggle.api.kaggle_api_extended import KaggleApi
import os
import pandas as pd
import sqlite3

db_name = 'supermarket_sales.db'

# Extract Data from Kaggle
def extract_data():
    os.environ['KAGGLE_CONFIG_DIR'] = os.path.expanduser("~/.kaggle")

    api = KaggleApi()
    api.authenticate()

    api.dataset_download_files('faresashraf1001/supermarket-sales', path='./data', unzip=True)
    print("Data downloaded.")
    return 

def read_data():
    return pd.read_csv("data/SuperMarket Analysis.csv")

# Transform and Load data

def trans_load_data(df):
    # --- Derived Column Calculations ---
    # 1. Base amount before tax
    df['Base Amount'] = df['Unit price'] * df['Quantity']

    # 2. Tax 5%: Calculated tax amount on the transaction at a 5% rate.
    df['Tax 5%'] = df['Base Amount'] * 0.05

    # 3. Total: Total amount for the transaction including tax.
    df['Total'] = df['Base Amount'] + df['Tax 5%']

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # SQL for creating tables
    create_dim_product_sql = """
    CREATE TABLE IF NOT EXISTS DimProduct (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_line TEXT NOT NULL UNIQUE
    );
    """

    create_dim_location_sql = """
    CREATE TABLE IF NOT EXISTS DimLocation (
        location_id INTEGER PRIMARY KEY AUTOINCREMENT,
        branch TEXT NOT NULL,
        city TEXT NOT NULL,
        UNIQUE(branch, city)
    );
    """

    create_fact_sales_sql = """
    CREATE TABLE IF NOT EXISTS FactSales (
        sale_id TEXT PRIMARY KEY, -- Using Invoice ID as primary key
        product_id INTEGER,
        location_id INTEGER,
        customer_type TEXT,
        gender TEXT,
        unit_price REAL,
        quantity INTEGER,
        tax_5_percent REAL,
        total REAL,
        payment TEXT,
        cogs REAL,
        gross_margin_percentage REAL,
        gross_income REAL,
        rating REAL,
        transaction_date DATE,
        transaction_time TIME,
        FOREIGN KEY (product_id) REFERENCES DimProduct(product_id),
        FOREIGN KEY (location_id) REFERENCES DimLocation(location_id)
    );
    """

    # Create tables
    cursor.execute(create_dim_product_sql)
    cursor.execute(create_dim_location_sql)
    cursor.execute(create_fact_sales_sql)
    conn.commit()
    print("Tables created successfully.")

    # --- Transformation and Loading ---

    # DimProduct
    product_lines = df['Product line'].unique()
    for product_line in product_lines:
        cursor.execute("INSERT OR IGNORE INTO DimProduct (product_line) VALUES (?)", (product_line,))
    conn.commit()
    print("DimProduct loaded.")

    # DimLocation
    locations = df[['Branch', 'City']].drop_duplicates()
    for index, row in locations.iterrows():
        cursor.execute("INSERT OR IGNORE INTO DimLocation (branch, city) VALUES (?, ?)", (row['Branch'], row['City']))
    conn.commit()
    print("DimLocation loaded.")

    # Get IDs for foreign keys
    product_id_map = pd.read_sql_query("SELECT product_line, product_id FROM DimProduct", conn).set_index('product_line').to_dict()['product_id']
    location_id_map = pd.read_sql_query("SELECT branch, city, location_id FROM DimLocation", conn)
    location_id_map['location_key'] = location_id_map['branch'] + '|' + location_id_map['city']
    location_id_map = location_id_map.set_index('location_key').to_dict()['location_id']
    print("Dimension IDs mapped.")

    # FactSales
    fact_data = []
    for index, row in df.iterrows():
        product_id = product_id_map.get(row['Product line'])
        location_key = f"{row['Branch']}|{row['City']}"
        location_id = location_id_map.get(location_key)

        fact_data.append((
            row['Invoice ID'],
            product_id,
            location_id,
            row['Customer type'],
            row['Gender'],
            row['Unit price'],
            row['Quantity'],
            row['Tax 5%'], 
            row['Total'], 
            row['Payment'],
            row['cogs'],
            row['gross margin percentage'], 
            row['gross income'],
            row['Rating'],
            row['Date'],
            row['Time']
        ))

    # Insert into FactSales in batches
    cursor.executemany("""
    INSERT OR REPLACE INTO FactSales (
        sale_id, product_id, location_id, customer_type, gender,
        unit_price, quantity, tax_5_percent, total, payment,
        cogs, gross_margin_percentage, gross_income, rating,
        transaction_date, transaction_time
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, fact_data)
    conn.commit()
    print("FactSales loaded.")

    conn.close()
    print("Data loading complete. SQLite database created/updated.")

def reporting_data():
    # Connect to the database
    conn = sqlite3.connect(db_name)

    # SQL Query for the report
    report_sql = """
    SELECT
        dp.product_line,
        dl.branch,
        dl.city,
        fs.customer_type,
        fs.gender,
        fs.transaction_date,
        fs.transaction_time,
        fs.total,
        fs.gross_income,
        fs.rating,
        SUM(fs.total) OVER (PARTITION BY dl.branch, dl.city ORDER BY fs.transaction_date, fs.transaction_time) AS running_total_sales_per_branch_city,
        AVG(fs.rating) OVER (PARTITION BY dl.city) AS avg_rating_per_city,
        DENSE_RANK() OVER (PARTITION BY dl.branch, dl.city ORDER BY fs.total DESC) AS rank_by_total_sales_per_product_line
    FROM
        FactSales fs
    JOIN
        DimProduct dp ON fs.product_id = dp.product_id
    JOIN
        DimLocation dl ON fs.location_id = dl.location_id
    GROUP BY
        dp.product_line, dl.branch
    """

    print("Executing report query...")
    report_df = pd.read_sql_query(report_sql, conn)
    print("Report generated successfully.")
    print(report_df.head())
    report_df.to_csv("data/output.csv", index=False)
    conn.close()

if __name__ == "__main__":
    try:
        extract_data()
    except:
        pass
    df = read_data()
    trans_load_data(df)
    reporting_data()