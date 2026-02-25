import pandas as pd
import json
import os
import random
from datetime import datetime
# import snowflake.connector # Simulated

class SupplyChainETL:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.df_shipments = None
        self.df_products = None
        self.df_suppliers = None
        self.df_warehouses = None
        self.df_time = None
        self.tracking_logs = None
        self.transformed_shipments = None
        
    def extract_data(self):
        print("Extracting data from files...")
        self.df_shipments = pd.read_csv(f'{self.data_dir}/fact_shipments.csv')
        self.df_products = pd.read_csv(f'{self.data_dir}/dim_products.csv')
        self.df_suppliers = pd.read_csv(f'{self.data_dir}/dim_suppliers.csv')
        self.df_warehouses = pd.read_csv(f'{self.data_dir}/dim_warehouses.csv')
        self.df_time = pd.read_csv(f'{self.data_dir}/dim_time.csv')
        with open(f'{self.data_dir}/tracking_logs.json', 'r') as f:
            self.tracking_logs = json.load(f)
        return self.df_shipments, self.df_products, self.tracking_logs

    def transform_data(self):
        print("Transforming data...")
        # 1. Enrichment: Join Shipments with Products to check unit price
        merged = self.df_shipments.merge(self.df_products, on='product_id')
        
        # 2. Add Business Logic: Flag High Value Shipments
        merged['is_high_value'] = (merged['quantity'] * merged['unit_price']) > 5000
        
        # 3. Clean statuses
        merged['status'] = merged['status'].str.upper()
        
        print(f"Transformation complete. High value shipments found: {merged['is_high_value'].sum()}")
        self.transformed_shipments = merged
        return merged

    def load_to_snowflake(self, snowflake_creds=None):
        """
        Simulated loading to Snowflake.
        In a real scenario, we would use snowflake.connector.pandas_tools.write_pandas
        """
        print("Loading data into Snowflake (Simulated)...")
        if not snowflake_creds:
            print("Warning: No credentials provided. Running in simulation mode.")
            
        # Example logic for real Snowflake load:
        """
        conn = snowflake.connector.connect(**snowflake_creds)
        from snowflake.connector.pandas_tools import write_pandas
        success, nchunks, nrows, _ = write_pandas(conn, self.transformed_shipments, 'FACT_SHIPMENTS')
        conn.close()
        """
        print(f"Successfully loaded {len(self.transformed_shipments)} rows into FACT_SHIPMENTS.")
        
    def process_semi_structured(self):
        print("Processing semi-structured tracking logs...")
        rows_to_load = []
        # Optimization for large datasets: Process a sample for simulation
        sample_logs = self.tracking_logs[:1000] if len(self.tracking_logs) > 1000 else self.tracking_logs
        for log in sample_logs:
            rows_to_load.append({
                'shipment_id': log['shipment_id'],
                'event_time': log['event_time'],
                'event_data': json.dumps(log['event_data'])
            })
        print(f"Prepared {len(rows_to_load)} JSON events for Raw_Tracking_Logs (Sampled from {len(self.tracking_logs)} total).")
        return rows_to_load

    def generate_dashboard_stats(self):
        print("Generating stats for Dashboard...")
        # Helper to convert ID to Date
        def to_date(x): return datetime.strptime(str(x), '%Y%m%d')

        # 1. Core Metrics
        total_shipments = len(self.df_shipments)
        ship_dates = self.df_shipments['ship_date_id'].apply(to_date)
        del_dates = self.df_shipments['delivery_date_id'].apply(to_date)
        avg_lead_time = (del_dates - ship_dates).mean().days
        total_cost = self.df_shipments['shipping_cost'].sum()

        # 2. Monthly Trends (for Line Chart)
        # Join with Dim_Time to get months
        df_trend = self.df_shipments.merge(self.df_time[['time_id', 'month']], left_on='order_date_id', right_on='time_id')
        monthly_counts = df_trend.groupby('month').size().reindex(range(1, 13), fill_value=0).tolist()

        # 3. Warehouse Distribution & Capacity
        warehouse_counts = self.df_shipments['warehouse_id'].value_counts()
        warehouse_map = self.df_warehouses.set_index('warehouse_id')['capacity'].to_dict()
        warehouse_names = self.df_warehouses.set_index('warehouse_id')['warehouse_name'].to_dict()
        
        warehouse_capacity = []
        for wh_id, name in warehouse_names.items():
            count = int(warehouse_counts.get(wh_id, 0))
            cap = int(warehouse_map.get(wh_id, 10000))
            usage = min(int((count / (cap/10)) * 100), 100) # Scaling for demo
            warehouse_capacity.append({"name": name, "usage": usage, "id": wh_id})

        # 4. Top Categories
        category_counts = self.transformed_shipments['category'].value_counts().head(5)
        top_categories = {
            "labels": category_counts.index.tolist(),
            "data": category_counts.values.tolist()
        }

        # 5. Recent Shipments (limit 500 for demoing pagination)
        recent_df = self.transformed_shipments.sort_values('order_date_id', ascending=False).head(500)
        recent_shipments = []
        for _, row in recent_df.iterrows():
            recent_shipments.append({
                "id": row['shipment_id'],
                "product": row['product_name'],
                "origin": "Global Hub", # Simplified for now
                "destination": row['warehouse_id'],
                "status": row['status'].capitalize(),
                "efficiency": f"{random.randint(85, 99)}%"
            })

        # 6. Supplier Performance
        supplier_counts = self.df_shipments['supplier_id'].value_counts()
        supplier_info = self.df_suppliers.set_index('supplier_id')
        supplier_stats = []
        for s_id, count in supplier_counts.head(4).items():
            info = supplier_info.loc[s_id]
            supplier_stats.append({
                "name": info['supplier_name'],
                "country": info['country'],
                "rating": float(info['rating']),
                "shipments": int(count)
            })

        stats = {
            'totalShipments': f"{total_shipments:,}",
            'totalRecordsRaw': total_shipments,
            'avgLeadTime': f"{avg_lead_time:.1f} Days",
            'totalCost': f"${total_cost:,.0f}",
            'lastUpdated': datetime.now().strftime('%H:%M:%S'),
            'monthlyTrends': monthly_counts,
            'warehouseCapacity': warehouse_capacity,
            'warehouseDist': warehouse_counts.to_dict(),
            'topCategories': top_categories,
            'recentShipments': recent_shipments,
            'supplierStats': supplier_stats
        }

        with open('dashboard/public/stats.json', 'w') as f:
            json.dump(stats, f, indent=2)
        print("Dynamic stats exported to dashboard/public/stats.json")

if __name__ == "__main__":
    etl = SupplyChainETL()
    etl.extract_data()
    etl.transform_data()
    etl.load_to_snowflake()
    etl.process_semi_structured()
    etl.generate_dashboard_stats()
