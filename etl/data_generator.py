import pandas as pd
import numpy as np
import random
import json
from datetime import datetime, timedelta
import os

def generate_supply_chain_data(num_records=1000):
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)

    # 1. Dim_Time
    start_date = datetime(2023, 1, 1)
    date_list = [start_date + timedelta(days=x) for x in range(365)]
    time_data = []
    for d in date_list:
        time_data.append({
            'time_id': int(d.strftime('%Y%m%d')),
            'full_date': d.strftime('%Y-%m-%d'),
            'day': d.day,
            'month': d.month,
            'quarter': (d.month - 1) // 3 + 1,
            'year': d.year,
            'is_weekend': d.weekday() >= 5
        })
    df_time = pd.DataFrame(time_data)
    df_time.to_csv('data/dim_time.csv', index=False)

    # 2. Dim_Products
    products = [
        ('P001', 'Solar Panel 100W', 'Energy', 'Solar', 150.00, 5.2, '100x60x5'),
        ('P002', 'Lithium Battery 12V', 'Energy', 'Storage', 200.00, 8.5, '30x20x15'),
        ('P003', 'Charge Controller 30A', 'Energy', 'Electronics', 45.00, 1.2, '15x10x5'),
        ('P004', 'Inverter 1000W', 'Energy', 'Electronics', 120.00, 3.5, '25x15x10'),
        ('P005', 'Electric Scooter X1', 'Transport', 'Vehicles', 899.00, 15.0, '120x50x110'),
        ('P006', 'Wipro Eco-Turbine', 'Energy', 'Wind', 2500.00, 25.0, '200x100x100')
    ]
    df_products = pd.DataFrame(products, columns=['product_id', 'product_name', 'category', 'sub_category', 'unit_price', 'weight', 'dimensions'])
    df_products.to_csv('data/dim_products.csv', index=False)

    # 3. Dim_Suppliers
    suppliers = [
        ('S001', 'EcoPower Systems', 'Alice Smith', 'alice@ecopower.com', '+123456789', 'USA', 4.8),
        ('S002', 'SunVolt Solar', 'Bob Jones', 'bob@sunvolt.com', '+987654321', 'China', 4.5),
        ('S003', 'EnergyTech Ltd', 'Charlie Brown', 'charlie@energytech.com', '+4422334455', 'Germany', 4.9)
    ]
    df_suppliers = pd.DataFrame(suppliers, columns=['supplier_id', 'supplier_name', 'contact_person', 'email', 'phone', 'country', 'rating'])
    df_suppliers.to_csv('data/dim_suppliers.csv', index=False)

    # 4. Dim_Warehouses
    warehouses = [
        ('W001', 'Jersey Central', '123 Harbor Way', 'Jersey City', 'NJ', 'USA', 50000),
        ('W002', 'Shanghai Port', '456 East Road', 'Shanghai', 'SH', 'China', 100000),
        ('W003', 'Berlin Hub', '789 Industrial Blvd', 'Berlin', 'BE', 'Germany', 75000)
    ]
    df_warehouses = pd.DataFrame(warehouses, columns=['warehouse_id', 'warehouse_name', 'location', 'city', 'state', 'country', 'capacity'])
    df_warehouses.to_csv('data/dim_warehouses.csv', index=False)

    # 5. Fact_Shipments
    shipments = []
    tracking_logs = []
    
    statuses = ['Delivered', 'Shipped', 'Pending', 'Delayed']
    
    for i in range(num_records):
        shipment_id = f'SHP{1000 + i}'
        prod = random.choice(products)
        supp = random.choice(suppliers)
        wh = random.choice(warehouses)
        
        ord_date = random.choice(date_list)
        ship_date = ord_date + timedelta(days=random.randint(1, 4))
        # CRISIS SIMULATION: 20-30 days delay and 5x costs
        del_date = ship_date + timedelta(days=random.randint(20, 30))
        
        status = random.choice(statuses)
        qty = random.randint(1, 50)
        cost = (qty * (float(prod[4]) * 0.1) + random.randint(20, 100)) * 5
        
        shipments.append({
            'shipment_id': shipment_id,
            'product_id': prod[0],
            'supplier_id': supp[0],
            'warehouse_id': wh[0],
            'order_date_id': int(ord_date.strftime('%Y%m%d')),
            'ship_date_id': int(ship_date.strftime('%Y%m%d')),
            'delivery_date_id': int(del_date.strftime('%Y%m%d')),
            'quantity': qty,
            'shipping_cost': round(cost, 2),
            'status': status
        })
        
        # Semi-structured JSON logs
        tracking_logs.append({
            'shipment_id': shipment_id,
            'event_time': del_date.strftime('%Y-%m-%dT%H:%M:%S'),
            'event_data': {
                'location': random.choice(['Port Customs', 'In Transit', 'Local Depot']),
                'status_update': status,
                'temperature': round(float(random.uniform(18.0, 25.0)), 1),
                'vibration_alert': random.choice([True, False])
            }
        })

    df_shipments = pd.DataFrame(shipments)
    df_shipments.to_csv('data/fact_shipments.csv', index=False)
    
    with open('data/tracking_logs.json', 'w') as f:
        json.dump(tracking_logs, f, indent=2)

    print(f"Generated {num_records} records in data/ directory.")

if __name__ == "__main__":
    generate_supply_chain_data(10000)
 