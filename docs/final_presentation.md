# Final Presentation: Supply Chain Optimization System

## Executive Summary
This project demonstrates a robust, scalable data infrastructure for Supply Chain Optimization. By combining advanced SQL, modern ETL practices, and interactive visualizations, we provide actionable insights into logistics efficiency and cost management.

## Project Highlights

### 1. Advanced Data Engineering
- **SQL Mastery**: Implemented CTEs and Window Functions for sliding window cost analysis and supplier ranking.
- **Spark Integration**: Processed 10,000+ shipment records with Batch + Streaming (Conceptual) workflows.
- **Semi-Structured Handling**: Native processing of JSON IoT tracking logs within Snowflake using VARIANT types.

### 2. Performance Tuning
- **Partitioning & Clustering**: Used clustering keys on `order_date_id` to optimize query performance in Snowflake.
- **Data Resilience**: Implemented Snowflake Time Travel for 30-day data retention and auditability.
- **Efficiency**: Reduced data scan requirements through intelligent Snowflake schema design.

### 3. Enterprise Security
- **Role-Based Access**: Multi-tier security model (Analyst, Engineer, Admin).
- **Data Privacy**: Automatic masking of PII (Emails, Phones) using Snowflake Dynamic Masking.

### 4. Interactive Analytics
- **Dashboard**: A premium React-based dashboard providing real-time visibility.
- **KPIs**: Lead time tracking, shipment velocity, and hub capacity utilization.

## Conclusion
The system successfully bridges the gap between raw logistics data and strategic decision-making, ensuring the supply chain is resilient, efficient, and secure.
