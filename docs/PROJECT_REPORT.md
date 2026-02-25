# Project Report: Supply Chain Optimization System

## 1. Executive Summary
The **Supply Chain Optimization System** is a comprehensive, end-to-end data engineering and analytics platform designed to streamline logistics, enhance inventory management, and provide actionable business intelligence. By leveraging a modern data stack—including **Snowflake** for scalable warehousing, **Apache Spark** for high-volume processing, and **React** for interactive visualization—the system bridges the gap between raw supply chain data and strategic decision-making.

---

## 2. System Architecture
The architecture is built on a modular, cloud-native design, ensuring scalability and high performance across the entire data lifecycle.

### Data Flow Overview:
1.  **Ingestion**: Synthetic data generators produce ERP-style CSVs and IoT-based JSON tracking logs.
2.  **Processing**: A hybrid ETL/ELT approach using Python for orchestration and PySpark for complex transformations.
3.  **Storage**: A robust Snowflake Schema designed for analytical efficiency, utilizing modern warehouse features like `VARIANT` types and Micro-partitioning.
4.  **Security**: Enterprise-grade security with Role-Based Access Control (RBAC) and Dynamic Data Masking.
5.  **Visualization**: A premium React-based dashboard providing real-time KPIs and "Supply Chain Reality" insights.

> *For detailed diagrams, see [Architecture Documentation](architecture.md).*

---

## 3. Data Generation & Ingestion
To facilitate robust testing and demonstration, the system includes a dedicated synthetic data generation layer.

-   **Logistics Volume**: Generates 10,000+ shipment records with randomized yet realistic constraints.
-   **ERP Simulation**: Produces structured CSV datasets for Products, Suppliers, and Warehouses.
-   **IoT Event Emulation**: Creates high-velocity JSON logs simulating sensor readings (temperature, GPS) for in-transit shipments.

---

## 4. Data Modeling & Warehouse Design
The core of the system is the **Snowflake Data Model**, optimized for complex analytical queries and high-concurrency reporting.

### Star/Snowflake Schema Entities:
-   **Fact_Shipments**: The central transactional table tracking shipment IDs, costs, and statuses.
-   **Dim_Products**: Detailed product metadata including categories and unit prices.
-   **Dim_Suppliers**: Supplier information with integrated rating and contact details.
-   **Dim_Warehouses**: Geographic locations and capacity metrics.
-   **Dim_Time**: A dedicated temporal dimension for granular time-series analysis (Daily, Monthly, Quarterly).
-   **Raw_Tracking_Logs**: A specialized table using Snowflake’s `VARIANT` type to ingest semi-structured JSON sensor data.

### Key Performance Optimizations:
-   **Clustering Keys**: The `Fact_Shipments` table is clustered by `order_date_id` to optimize temporal scans.
-   **Micro-partitioning**: Leverages Snowflake’s automatic partitioning for sub-second query performance on large datasets.
-   **Time Travel**: Configured with a 30-day retention period for auditing and historical data recovery.

---

## 5. ETL & Big Data Processing
The processing layer is designed to handle both structured batch data and semi-structured event logs.

### PySpark Implementation:
-   **Complex Transformations**: Used for window functions (e.g., calculates cumulative shipment volumes per warehouse).
-   **Scalability**: Handles 10,000+ records in the demonstration, with an architecture ready for millions.
-   **Data Consistency**: Implements rigorous cleaning and validation logic to ensure data integrity across the pipeline.

### Advanced SQL Engineering:
-   **Window Functions**: Implemented for cumulative cost analysis and supplier performance ranking.
-   **CTEs**: Utilized for modular, readable query structures in the reporting layer.
-   **Lateral Flattening**: Native JSON processing to extract IoT sensor data (e.g., location, temperature) from `VARIANT` columns.

---

## 6. Security & Governance
A multi-layered security model ensures data protection and compliance.

-   **RBAC (Role-Based Access Control)**: Discrete roles defined for `ANALYST`, `DATA_ENGINEER`, and `ADMIN`.
-   **Dynamic Data Masking**: PII (Personally Identifiable Information) like supplier phone numbers and emails are automatically masked for non-authorized roles.
-   **Governance**: Centralized DDL and security scripts ensure reproducible and auditable environment setups.

---

## 7. Interactive Visualization Dashboard
The presentation layer provides a "Premium Dark Mode" interface for supply chain managers, built with React, Vite, and Chart.js.

### Key Visualizations & Features:
-   **Executive KPIs Tracker**: Instant visibility into **Total Shipments**, **Average Lead Time**, and **Logistics Cost** with real-time trend indicators.
-   **Shipment Velocity Analysis**: High-fidelity line charts tracking monthly shipment volumes to identify seasonal peaks.
-   **Inventory Distribution by Hub**: Interactive doughnut charts showing SKU allocation across different warehouse nodes.
-   **Global Shipment Registry**: A searchable, paginated registry with real-time status tracking (Pending, Shipped, Delivered, Delayed) and efficiency ratings.
-   **Warehouse Capacity Monitor**: Visual progress bars alerting managers to high-utilization hubs (e.g., alerts for usage > 90%).
-   **Lead Time Forecasting**: Predictive analytics chart comparing **Actual Days** vs **Projected Days** to optimize future route planning.
-   **Supplier Performance Matrix**: Scorecards with vendor ratings, contact summaries, and total shipment volume metrics.

---

## 8. Conclusion & Future Roadmap
The Supply Chain Optimization System demonstrates the power of a modern data stack in solving complex logistics challenges. 

### Future Enhancements:
-   **Predictive Analytics**: Integrating Machine Learning models for demand forecasting and delay prediction.
-   **Real-time Streaming**: Enhancing the Spark layer with **Structured Streaming** for sub-minute latency.
-   **Automated Replenishment**: Triggering automated API calls to suppliers when inventory drops below reorder levels.

---
*Report Generated: 2026-02-25*
*Project Owner: Om Choudhary*
