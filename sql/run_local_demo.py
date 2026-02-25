import duckdb
import pandas as pd
import os

def run_local_sql_demo():
    print("\n" + "="*50)
    print("LOG: STARTING LOCAL SQL DEMO (DUCKDB)")
    print("="*50)
    
    # 1. Setup DuckDB Connection
    con = duckdb.connect(database=':memory:')
    
    # Check if data exists
    if not os.path.exists('data/fact_shipments.csv'):
        print("ERR: Data files not found. Please run etl/data_generator.py first.")
        return

    # 2. Register CSVs as Tables
    con.execute("CREATE TABLE Dim_Time AS SELECT * FROM read_csv_auto('data/dim_time.csv')")
    con.execute("CREATE TABLE Dim_Products AS SELECT * FROM read_csv_auto('data/dim_products.csv')")
    con.execute("CREATE TABLE Dim_Suppliers AS SELECT * FROM read_csv_auto('data/dim_suppliers.csv')")
    con.execute("CREATE TABLE Dim_Warehouses AS SELECT * FROM read_csv_auto('data/dim_warehouses.csv')")
    con.execute("CREATE TABLE Fact_Shipments AS SELECT * FROM read_csv_auto('data/fact_shipments.csv')")
    
    # 3. Query 1: Moving Average (Window Function)
    print("\nPROG: Executing Query 1: 3-Month Moving Average Shipping Cost per Product...")
    query1 = """
    WITH ProductMonthlyCosts AS (
        SELECT 
            p.product_name,
            t.month,
            t.year,
            SUM(f.shipping_cost) as total_cost
        FROM Fact_Shipments f
        JOIN Dim_Products p ON f.product_id = p.product_id
        JOIN Dim_Time t ON f.order_date_id = t.time_id
        GROUP BY p.product_name, t.month, t.year
    )
    SELECT 
        product_name,
        month,
        year,
        total_cost,
        AVG(total_cost) OVER (
            PARTITION BY product_name 
            ORDER BY year, month 
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ) as sliding_avg_cost
    FROM ProductMonthlyCosts
    ORDER BY product_name, year, month
    LIMIT 10;
    """
    res1 = con.execute(query1).df()
    print(res1)

    # 4. Query 2: Supplier Ranking (Ranking Function)
    print("\nPROG: Executing Query 2: Supplier Performance Ranking (Avg Delivery Time)...")
    query2 = """
    WITH DeliveryStats AS (
        SELECT 
            s.supplier_name,
            DATEDIFF('day', CAST(t_order.full_date AS DATE), CAST(t_delivery.full_date AS DATE)) as delivery_days
        FROM Fact_Shipments f
        JOIN Dim_Suppliers s ON f.supplier_id = s.supplier_id
        JOIN Dim_Time t_order ON f.order_date_id = t_order.time_id
        JOIN Dim_Time t_delivery ON f.delivery_date_id = t_delivery.time_id
        WHERE UPPER(f.status) = 'DELIVERED'
    )
    SELECT 
        supplier_name,
        AVG(delivery_days) as avg_days,
        RANK() OVER (ORDER BY AVG(delivery_days) ASC) as rank
    FROM DeliveryStats
    GROUP BY supplier_name;
    """
    res2 = con.execute(query2).df()
    print(res2)

    print("\n" + "="*50)
    print("LOG: LOCAL SQL DEMO COMPLETE")
    print("="*50)

if __name__ == "__main__":
    run_local_sql_demo()
