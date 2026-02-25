# Supply Chain Optimization System Architecture

## Overview
The system is designed as a modern cloud-native data platform, leveraging Snowflake for storage and optimization, and Python/Spark for processing and ETL.

## Architecture Diagram (Mermaid)

```mermaid
graph TD
    subgraph "Data Sources"
        S1[ERP Systems - CSV]
        S2[IoT Sensors - JSON]
        S3[Supplier APIs]
    end

    subgraph "Processing Layer (Python/Spark)"
        P1[Data Generator]
        P2[Python ETL Scripts]
        P3[PySpark Batch Processor]
        P4[Spark Streaming]
    end

    subgraph "Data Warehouse (Snowflake)"
        W1[(Raw Zone - Staging)]
        W2[(Curated Zone - Snowflake Schema)]
        W3[(Analytics Zone - Fact/Dim)]
    end

    subgraph "Optimization & Security"
        O1[Clustering/Indexing]
        O2[Time Travel]
        O3[RBAC & Data Masking]
    end

    subgraph "Presentation Layer"
        D1[Interactive React Dashboard]
        D2[BI Tools / SQL Reports]
    end

    S1 --> P2
    S2 --> P4
    S3 --> P2
    
    P2 --> W1
    P4 --> W1
    P3 --> W2
    
    W1 --> W2
    W2 --> W3
    
    W3 --> O1
    W3 --> O2
    W3 --> O3
    
    W3 --> D1
    W3 --> D2
```

## Key Components

### 1. Data Modeling
- **Star Schema**: Optimized for analytical queries.
- **Snowflake Tables**: Using `VARIANT` for IoT data and `CLUSTER BY` for temporal partitioning.

### 2. ETL/ELT Pipeline
- **Python**: Used for lightweight orchestration and data movement.
- **Spark**: Handles large-scale transformations and window functions (e.g., cumulative inventory tracking).

### 3. Snowflake Optimization
- **Clustering**: Drastically reduces scan time for time-series queries.
- **Time Travel**: Allows querying data at any point in the last 90 days for audit and recovery.

### 4. Security & Governance
- **RBAC**: granular roles for Analysts and Engineers.
- **Dynamic Masking**: Protects sensitive supplier PII.

### 5. Visualization
- **React Dashboard**: Built with Vite and Chart.js for real-time visibility into shipment velocity and hub efficiency.
