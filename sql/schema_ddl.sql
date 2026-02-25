-- Supply Chain Optimization System - Data Warehouse Schema (Snowflake/Star Schema)

-- 1. Dimension Tables
CREATE TABLE Dim_Time (
    time_id INT PRIMARY KEY,
    full_date DATE,
    day INT,
    month INT,
    quarter INT,
    year INT,
    is_weekend BOOLEAN
);

CREATE TABLE Dim_Products (
    product_id STRING PRIMARY KEY,
    product_name STRING,
    category STRING,
    sub_category STRING,
    unit_price DECIMAL(10, 2),
    weight DECIMAL(10, 2),
    dimensions STRING
);

CREATE TABLE Dim_Suppliers (
    supplier_id STRING PRIMARY KEY,
    supplier_name STRING,
    contact_person STRING,
    email STRING,
    phone STRING,
    country STRING,
    rating DECIMAL(3, 2)
);

CREATE TABLE Dim_Warehouses (
    warehouse_id STRING PRIMARY KEY,
    warehouse_name STRING,
    location STRING,
    city STRING,
    state STRING,
    country STRING,
    capacity INT
);

-- 2. Fact Table
CREATE TABLE Fact_Shipments (
    shipment_id STRING PRIMARY KEY,
    product_id STRING REFERENCES Dim_Products(product_id),
    supplier_id STRING REFERENCES Dim_Suppliers(supplier_id),
    warehouse_id STRING REFERENCES Dim_Warehouses(warehouse_id),
    order_date_id INT REFERENCES Dim_Time(time_id),
    ship_date_id INT REFERENCES Dim_Time(time_id),
    delivery_date_id INT REFERENCES Dim_Time(time_id),
    quantity INT,
    shipping_cost DECIMAL(12, 2),
    status STRING -- Pending, Shipped, Delivered, Delayed
)
CLUSTER BY (order_date_id); -- Optimization: Clustering for performance

-- 2.1 Optimization: Time Travel (Data Retention)
ALTER TABLE Fact_Shipments SET DATA_RETENTION_TIME_IN_DAYS = 30;
ALTER TABLE Dim_Inventory SET DATA_RETENTION_TIME_IN_DAYS = 7;

-- 3. Semi-Structured Data Table (Snowflake specific)
CREATE TABLE Raw_Tracking_Logs (
    log_id INT AUTOINCREMENT PRIMARY KEY,
    shipment_id STRING,
    event_time TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    event_data VARIANT -- Stores JSON tracking info
);

-- 4. Inventory Tracking (Snowflake for real-time insights)
CREATE TABLE Dim_Inventory (
    inventory_id STRING PRIMARY KEY,
    warehouse_id STRING REFERENCES Dim_Warehouses(warehouse_id),
    product_id STRING REFERENCES Dim_Products(product_id),
    current_stock INT,
    reorder_level INT,
    last_updated TIMESTAMP_NTZ
);
