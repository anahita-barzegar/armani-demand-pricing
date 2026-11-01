-- =====================================================
-- Armani Middle East Trading
-- Star Schema Initialization
-- PostgreSQL 18
-- =====================================================

DROP TABLE IF EXISTS fact_weekly_sales CASCADE;
DROP TABLE IF EXISTS dim_product CASCADE;
DROP TABLE IF EXISTS dim_week CASCADE;

-- =====================================================
-- Dimension: Product
-- =====================================================
CREATE TABLE dim_product (
    product_id      SERIAL PRIMARY KEY,
    product_name    VARCHAR(100) NOT NULL UNIQUE,
    category        VARCHAR(50),
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_dim_product_category ON dim_product(category);

-- =====================================================
-- Dimension: Week / Time
-- =====================================================
CREATE TABLE dim_week (
    week_key        INT PRIMARY KEY,
    year            INT,
    week_of_year    INT,
    year_week       VARCHAR(10),
    quarter         INT,
    month           INT,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- Fact Table: Weekly Sales
-- =====================================================
CREATE TABLE fact_weekly_sales (
    id                          SERIAL PRIMARY KEY,
    week_key                    INT NOT NULL REFERENCES dim_week(week_key),
    product_id                  INT NOT NULL REFERENCES dim_product(product_id),
    
    sales_units                 DECIMAL(14,3),
    cogs                        DECIMAL(14,4),
    inventory_level             DECIMAL(14,3),
    demand_forecast             DECIMAL(14,3),
    price_per_unit              DECIMAL(12,4),
    gross_profit                DECIMAL(14,2),
    operating_profit            DECIMAL(14,2),
    revenue                     DECIMAL(14,2),
    inventory_turnover_ratio    DECIMAL(10,4),
    gross_profit_margin         DECIMAL(8,4),
    revenue_growth              DECIMAL(8,4),
    
    loaded_at                   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT uq_fact_week_product UNIQUE (week_key, product_id)
);

CREATE INDEX idx_fact_week      ON fact_weekly_sales(week_key);
CREATE INDEX idx_fact_product   ON fact_weekly_sales(product_id);
CREATE INDEX idx_fact_revenue   ON fact_weekly_sales(revenue);
CREATE INDEX idx_fact_sales     ON fact_weekly_sales(sales_units);

-- =====================================================
-- Enriched View
-- =====================================================
CREATE OR REPLACE VIEW vw_sales_enriched AS
SELECT
    f.id,
    w.week_key,
    w.year,
    w.week_of_year,
    w.year_week,
    w.quarter,
    p.product_name,
    p.category,
    f.sales_units,
    f.cogs,
    f.inventory_level,
    f.demand_forecast,
    f.price_per_unit,
    f.gross_profit,
    f.operating_profit,
    f.revenue,
    f.inventory_turnover_ratio,
    f.gross_profit_margin,
    f.revenue_growth,
    f.loaded_at
FROM fact_weekly_sales f
JOIN dim_week w     ON f.week_key = w.week_key
JOIN dim_product p  ON f.product_id = p.product_id;

DO $$
BEGIN
    RAISE NOTICE 'Star Schema created successfully for Armani Trading!';
END $$;
