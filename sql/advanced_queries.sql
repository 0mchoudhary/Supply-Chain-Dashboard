-- Advanced SQL Queries for Supply Chain Analytics

-- 1. CTE & Window Functions: Calculate Moving Average of Shipment Costs per Product
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
    ) as sliding_3_month_avg_cost
FROM ProductMonthlyCosts;

-- 2. Performance Analysis: Ranking Suppliers by Delivery Time (Window Function)
WITH DeliveryStats AS (
    SELECT 
        s.supplier_name,
        f.shipment_id,
        DATEDIFF('day', t_order.full_date, t_delivery.full_date) as delivery_days
    FROM Fact_Shipments f
    JOIN Dim_Suppliers s ON f.supplier_id = s.supplier_id
    JOIN Dim_Time t_order ON f.order_date_id = t_order.time_id
    JOIN Dim_Time t_delivery ON f.delivery_date_id = t_delivery.time_id
    WHERE f.status = 'Delivered'
)
SELECT 
    supplier_name,
    AVG(delivery_days) as avg_delivery_time,
    RANK() OVER (ORDER BY AVG(delivery_days) ASC) as supplier_rank
FROM DeliveryStats
GROUP BY supplier_name;

-- 3. Semi-Structured Data Query (Snowflake Flattening)
SELECT 
    shipment_id,
    event_time,
    event_data:location::STRING as event_location,
    event_data:status_update::STRING as status_update,
    event_data:temperature::FLOAT as sensor_temperature
FROM Raw_Tracking_Logs,
LATERAL FLATTEN(input => event_data) WHERE TYPEOF(event_data) = 'OBJECT';

-- 4. Temporal Analysis using Snowflake Time Travel (Conceptual)
-- To query data as it was 1 hour ago:
-- SELECT * FROM Fact_Shipments AT(OFFSET => -3600);

-- 5. Partitioning & Indexing (Clustering in Snowflake)
-- Snowflake uses micro-partitions and clustering keys instead of traditional indexes.
-- We already have 'CLUSTER BY (order_date_id)' in the DDL.
-- To check clustering depth:
-- SELECT SYSTEM$CLUSTERING_DEPTH('Fact_Shipments');
