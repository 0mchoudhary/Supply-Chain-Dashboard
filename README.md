# Supply Chain Optimization System

A comprehensive End-to-End Data Engineering and Analytics platform for Supply Chain Optimization. This project demonstrates a modern data stack including Snowflake-style modeling, Python/Spark ETL pipelines, and a premium interactive dashboard.

## 🚀 Features

- **Data Warehousing**: Star/Snowflake schema design with Fact and Dimension tables.
- **Advanced SQL**: Implementation of CTEs, Window Functions, and Semi-Structured (JSON) data handling.
- **ETL/ELT Pipelines**: Python-based data generation and transformation pipelines.
- **Big Data Processing**: Apache Spark (PySpark) for batch and (conceptual) streaming processing.
- **Snowflake Optimization**: Clustering keys, Time Travel (30-day retention), and RBAC security.
- **Interactive Dashboard**: Premium React/Vite dashboard with real-time KPI tracking and data visualization.

## 🛠️ Technology Stack

- **Analytics**: SQL (Snowflake/DuckDB)
- **Data Engineering**: Python, PySpark, Pandas
- **Frontend**: React.js, Vite, Chart.js, Tailwind CSS
- **Design**: Premium Dark Mode UI with Lucide Icons

## 📂 Project Structure

```text
/
├── sql/                # DDL scripts, Advanced Queries, and Local SQL Runner
├── etl/                # Python & PySpark ETL scripts
├── data/               # Generated CSV/JSON datasets (Git ignored)
├── dashboard/          # React/Vite Dashboard source code
├── docs/               # Architecture Diagrams and Presentations
└── README.md
```

## ⚙️ Setup & Installation

### 1. Prerequisites
- Python 3.8+
- Node.js & npm
- Java (for PySpark)

### 2. Install Dependencies

**Python Dependencies:**
```bash
pip install pandas pyspark duckdb
```

**Dashboard Dependencies:**
```bash
cd dashboard
npm install
```

### 3. Generate Data & Run ETL
Generate synthetic supply chain data (10,000+ records) and process it through the pipeline:
```bash
# From the root directory
python3 etl/data_generator.py
python3 etl/etl_pipeline.py
python3 etl/pyspark_processor.py
```

### 4. Run Local SQL Demo
Test advanced window functions and rankings locally using DuckDB:
```bash
python3 sql/run_local_demo.py
```

### 5. Launch the Dashboard
Start the interactive visualization engine:
```bash
cd dashboard
npm run dev -- --port 3000
```
Visit `http://localhost:3000` to view the dashboard.

## 📊 Architecture

The system follows a modern cloud data platform architecture:
1. **Source**: Synthetic generator produces logistics logs and ERP-style CSVs.
2. **Process**: PySpark handles complex transformations and efficiency metrics.
3. **Storage**: Snowflake-style schema with automated stats export for the UI.
4. **Visualize**: React dashboard displays real-time "Supply Chain Reality" including crisis simulations.

## 🛡️ Security & Governance
- **RBAC**: Pre-configured roles for Analysts, Engineers, and Admins.
- **Masking**: PII data masking policy for supplier contact information.
- **Retention**: 30-day Time Travel retention for critical fact tables.

---

Built for **Advanced Supply Chain Analytics**.
