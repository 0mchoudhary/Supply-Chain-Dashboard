# Apache Spark Processor for Supply Chain Optimization
# Demonstrates Batch and Streaming (Conceptual) data processing

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window

def run_spark_batch():
    # Initialize Spark Session
    spark = SparkSession.builder \
        .appName("SupplyChainOptimization") \
        .getOrCreate()

    print("Spark: Loading Fact_Shipments...")
    df_shipments = spark.read.csv("data/fact_shipments.csv", header=True, inferSchema=True)
    df_products = spark.read.csv("data/dim_products.csv", header=True, inferSchema=True)

    # 1. Advanced Transformation: Aggregated Freight Cost Analysis
    # Join shipments and products
    df_enriched = df_shipments.join(df_products, "product_id")

    # 2. Window Function: Running total of quantity per warehouse
    window_spec = Window.partitionBy("warehouse_id").orderBy("order_date_id")
    df_with_running_total = df_enriched.withColumn(
        "cumulative_quantity", 
        F.sum("quantity").over(window_spec)
    )

    # 3. Calculate Efficiency Metrics
    # Freight cost per unit
    df_metrics = df_with_running_total.withColumn(
        "cost_per_unit", 
        F.col("shipping_cost") / F.col("quantity")
    )

    # 4. Group by Warehouse and Category for Summary
    df_summary = df_metrics.groupBy("warehouse_id", "category") \
        .agg(
            F.avg("cost_per_unit").alias("avg_freight_cost"),
            F.sum("quantity").alias("total_units"),
            F.count("shipment_id").alias("shipment_count")
        )

    print("Spark Batch Results (Sample):")
    df_summary.show(5)

def run_spark_streaming():
    """
    Simulates real-time IoT log processing using Spark Structured Streaming.
    In a production scenario, this would connect to Kafka or Azure Event Hubs.
    """
    spark = SparkSession.builder \
        .appName("SupplyChainStreaming") \
        .getOrCreate()

    print("Spark: Starting Structured Streaming from 'data/'...")
    
    # Define schema for the JSON tracking logs
    schema = "shipment_id STRING, event_time TIMESTAMP, event_data STRUCT<location: STRING, status_update: STRING, temperature: DOUBLE, vibration_alert: BOOLEAN>"

    # 1. Read Stream from directory
    df_stream = spark.readStream \
        .format("json") \
        .schema(schema) \
        .option("maxFilesPerTrigger", 1) \
        .load("data/streaming_source/") # Conceptual directory

    # 2. Transformation: Alert if temperature exceeds safety limit (Alert Mechanism)
    df_alerts = df_stream.filter("event_data.temperature > 24.5") \
        .select("shipment_id", "event_data.temperature", "event_data.location")

    # 3. Sink: Write results to console for the live demo
    query = df_alerts.writeStream \
        .outputMode("append") \
        .format("console") \
        .start()

    print("Spark Streaming Query Active. Monitoring for sensor alerts...")
    # query.awaitTermination(timeout=30) # Wait 30s for demo
    query.stop()

    print("Spark Processing Complete.")
    spark.stop()

if __name__ == "__main__":
    # In a local environment without Spark installed, this may fail.
    # We provide the code for architectural completeness.
    try:
        run_spark_batch()
    except Exception as e:
        print(f"Spark execution skipped: {e}")
        print("Note: Ensure PySpark is installed to run this script.")
