# Armani Middle East Trading — Data Science Assessment
## Business Context & Problem Statement

Armani Middle East Trading specializes in the import and distribution of essential food commodities across regional markets. As trade volumes scale, the organization faces key operational challenges:

1. **Demand Volatility** — Supply chain fluctuations, macroeconomic pressures, and seasonality make accurate commodity forecasting difficult.
2. **Dynamic Pricing Needs** — Setting static prices leads to missed revenue during high-demand periods or unsold inventory during off-peak windows.
3. **Credit & Liquidity Management** — Balancing competitive sales terms with exposure to customer credit default risks and inventory holding costs.

**Mission:** Design and build an end-to-end data pipeline, predictive demand engine, financial KPI reporting layer, and dynamic pricing strategy.

---

## Solution Architecture


---

## Tech Stack

| Layer              | Technology                      |
|--------------------|---------------------------------|
| Language           | Python 3.11+                    |
| Data Processing    | Pandas, NumPy                   |
| Database           | PostgreSQL 18                   |
| DB Access          | SQLAlchemy                      |
| Forecasting        | LightGBM / Prophet / XGBoost    |
| Dashboard          | Streamlit                       |
| Containerization   | Docker + Docker Compose         |
| Task Runner        | Makefile                        |

---

## Project Structure


---

## Database Design (Star Schema)

**Fact Table:** `fact_weekly_sales`  
**Dimension Tables:** `dim_product`, `dim_week`

This design is optimized for analytical queries required by forecasting, KPI calculation, and pricing logic.

---

## Prerequisites

- Docker & Docker Compose
- Python 3.11+
- Make

---

## Full Setup Instructions

```bash
# 1. Place dataset
cp /path/to/Sample_Data.xlsx data/raw/

# 2. Start services
make up

# 3. Create virtual environment
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run ETL
python -m src.etl.main

# 6. Launch Dashboard
streamlit run dashboard/app.py
# Dashboard will be available at: http://localhost:8501

# 7. forecasting
python notebooks/02_forecasting.py

# 8. Dynamic pricing
python notebooks/03_pricing_strategy.py

# PostgreSQL → localhost:5432
# pgAdmin    → http://localhost:5050




