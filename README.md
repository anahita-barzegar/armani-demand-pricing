# Armani Middle East Trading — Data Science Assessment

An end-to-end data engineering and data science solution for demand forecasting, financial KPI reporting, and dynamic pricing optimization in the food commodity trading industry.

---

## 1. Business Context & Problem Statement

Armani Middle East Trading specializes in the import and distribution of essential food commodities across regional markets. As trade volumes scale, the organization faces several operational challenges:

1. **Demand Volatility** — Supply chain fluctuations, macroeconomic pressures, and seasonality make accurate commodity forecasting difficult.
2. **Dynamic Pricing Needs** — Static pricing strategies can lead to missed revenue opportunities during high-demand periods or unsold inventory during off-peak windows.
3. **Credit & Liquidity Management** — Balancing competitive sales terms with customer credit default risks and inventory holding costs.

### Mission

Design and build an end-to-end data pipeline, predictive demand engine, financial KPI reporting layer, and dynamic pricing strategy to support data-driven business decisions.

---

## 2. Solution Architecture

The solution follows a modular architecture that separates data ingestion, storage, processing, predictive modeling, and business intelligence.

### Architecture Overview

```text
                 Raw Business Data
                 (Sample_Data.xlsx)
                         |
                         v
                Data Ingestion Layer
                         |
                         v
                  ETL Processing
              (Python / Pandas / NumPy)
                         |
                         v
                  PostgreSQL 18
                  Data Warehouse
                         |
                  Star Schema
                  /          \
                 v            v
          Fact Tables     Dimension Tables
                 \            /
                  \          /
                   v        v
                Analytics Layer
                         |
              +----------+----------+
              |                     |
              v                     v
       Demand Forecasting     Financial KPIs
       (ML Models)             (SQL / Python)
              |                     |
              v                     v
         Demand Signals       Business Metrics
              |                     |
              +----------+----------+
                         |
                         v
                Dynamic Pricing Engine
                         |
                         v
                  Pricing Strategy
                         |
                         v
                 Streamlit Dashboard
```

### Main Components

- **Data Ingestion:** Loading and validating raw business data.
- **ETL Pipeline:** Cleaning, transforming, and preparing analytical datasets.
- **Data Warehouse:** Storing structured business data using a dimensional model.
- **Demand Forecasting:** Predicting future commodity demand using machine learning.
- **Financial Analytics:** Calculating business KPIs and monitoring financial performance.
- **Dynamic Pricing:** Generating pricing recommendations based on demand patterns and business indicators.
- **Dashboard:** Providing an interactive interface for business insights and decision support.

---

## 3. Technology Stack

| Layer | Technology |
|---|---|
| Programming Language | Python 3.11+ |
| Data Processing | Pandas, NumPy |
| Database | PostgreSQL 18 |
| Database Access | SQLAlchemy |
| Forecasting | LightGBM / Prophet / XGBoost |
| Dashboard | Streamlit |
| Containerization | Docker, Docker Compose |
| Task Runner | Makefile |
| Data Source | Excel (XLSX) |

---

## 4. Project Structure

```text
armani-demand-pricing/
│
├── data/
│   └── raw/
│       └── Sample_Data.xlsx
│
├── src/
│   ├── etl/
│   │   └── main.py
│   │
│   └── ...
│
├── notebooks/
│   ├── 02_forecasting.py
│   └── 03_pricing_strategy.py
│
├── dashboard/
│   └── app.py
│
├── requirements.txt
├── docker-compose.yml
├── Makefile
├── .env.example
├── .gitignore
└── README.md
```

---

## 5. Database Design — Star Schema

The analytical database follows a Star Schema dimensional modeling approach.

### Fact Table

**`fact_weekly_sales`**

Stores weekly sales transactions and measurable business metrics.

### Dimension Tables

- **`dim_product`** — Product-related attributes and commodity information.
- **`dim_week`** — Time-related attributes used for weekly analysis and forecasting.

### Design Objectives

- Simplify analytical queries.
- Improve reporting and aggregation performance.
- Support time-series demand forecasting.
- Enable product-level and time-based business analysis.
- Provide a consistent data foundation for pricing optimization.

---

## 6. Prerequisites

Make sure the following tools are installed:

- Docker
- Docker Compose
- Python 3.11+
- Make

Verify the installations:

```bash
docker --version
docker compose version
python3 --version
make --version
```

---

## 7. Getting Started — Full Setup Instructions

### Step 1. Clone the Repository

Clone the project to your local machine:

```bash
git clone https://github.com/anahita-barzegar/armani-demand-pricing.git
```

Navigate to the project directory:

```bash
cd armani-demand-pricing
```

### Step 2. Configure Environment Variables

Create your local environment configuration file:

```bash
cp .env.example .env
```

Update `.env` with your local database credentials and application settings.

**Important:** Never commit your `.env` file or expose sensitive credentials. The `.env` file is excluded from Git tracking.

### Step 3. Place the Dataset

Place the provided dataset in the raw data directory:

```bash
mkdir -p data/raw
cp /path/to/Sample_Data.xlsx data/raw/
```

Make sure the dataset filename matches the expected input filename.

### Step 4. Start Infrastructure Services

Start PostgreSQL and other configured services:

```bash
make up
```

### Step 5. Create a Python Virtual Environment

```bash
python3 -m venv venv
```

Activate the environment:

**Linux / macOS:**

```bash
source venv/bin/activate
```

**Windows:**

```bash
venv\Scripts\activate
```

### Step 6. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 7. Run the ETL Pipeline

Execute the data ingestion and transformation process:

```bash
python -m src.etl.main
```

This step prepares the analytical datasets and loads the processed data into PostgreSQL.

### Step 8. Launch the Dashboard

```bash
streamlit run dashboard/app.py
```

The dashboard will be available at:

http://localhost:8501

### Step 9. Run Demand Forecasting

Execute the forecasting module:

```bash
python notebooks/02_forecasting.py
```

This module is responsible for demand prediction and generating forecasting outputs.

### Step 10. Run Dynamic Pricing Strategy

Execute the pricing optimization module:

```bash
python notebooks/03_pricing_strategy.py
```

This module generates pricing recommendations based on the forecasting results and available business indicators.

---

## 8. Service Endpoints

| Service | URL / Connection |
|---|---|
| PostgreSQL | `localhost:5432` |
| pgAdmin | http://localhost:5050 |
| Streamlit Dashboard | http://localhost:8501 |

Database credentials and service configurations are managed through environment variables.

---

## 9. Running the Project with Docker

To start all configured services:

```bash
make up
```

To stop the services:

```bash
make down
```

To inspect running containers:

```bash
docker compose ps
```

To view service logs:

```bash
docker compose logs -f
```

---

## 10. Security & Configuration

The project uses environment variables to separate application configuration from source code.

- Database credentials are stored in `.env`.
- `.env` is excluded from version control.
- `.env.example` provides a template for required configuration.
- Sensitive credentials should never be committed to the repository.

---

## 11. Future Improvements

Potential extensions to the current solution include:

- Automated model retraining and evaluation.
- Demand forecasting model comparison and hyperparameter optimization.
- Real-time pricing recommendations.
- Customer credit risk scoring.
- Inventory-aware pricing optimization.
- Automated data quality monitoring.
- Pipeline orchestration and scheduling.
- Model performance monitoring and drift detection.

---

## 12. Author

**Anahita Barzegar**

Data Engineer | Data Science & Machine Learning

GitHub: https://github.com/anahita-barzegar

---