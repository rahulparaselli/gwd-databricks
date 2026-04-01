# GWD Data Engineering Project - Complete Documentation

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture Overview](#architecture-overview)
3. [Technology Stack](#technology-stack)
4. [Data Pipeline Layers](#data-pipeline-layers)
5. [Bronze Layer - Raw Data Ingestion](#bronze-layer---raw-data-ingestion)
6. [Silver Layer - Data Cleaning & Transformation](#silver-layer---data-cleaning--transformation)
7. [Gold Layer - Analytical Layer](#gold-layer---analytical-layer)
8. [Dimensional Model & Relationships](#dimensional-model--relationships)
9. [KPI Calculations](#kpi-calculations)
10. [Dashboard & Visualizations](#dashboard--visualizations)
11. [Pipeline Orchestration](#pipeline-orchestration)
12. [How to Run the Pipeline](#how-to-run-the-pipeline)
13. [Data Lineage](#data-lineage)

---

## 🎯 Project Overview

This is an end-to-end data engineering project implementing the **Medallion Architecture** (Bronze-Silver-Gold) for business intelligence and KPI reporting. The project processes invoice, customer, product, and payment data to generate actionable business insights through automated data pipelines and interactive dashboards.

**Business Use Case:** Retail/E-commerce analytics platform for tracking sales performance, customer behavior, product trends, and regional revenue distribution.

---

## 🏗️ Architecture Overview

### Medallion Architecture (Lakehouse Pattern)

```
┌─────────────────────────────────────────────────────────────┐
│                         BRONZE LAYER                         │
│                      (Raw Data Ingestion)                     │
│   customers | products | invoices | invoice_line_items       │
│              payments | exchange_rates | countries            │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                         SILVER LAYER                         │
│                 (Cleaned & Standardized Data)                 │
│    Data Quality | Deduplication | Type Conversion            │
│         Standardization | Negative Handling                   │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                          GOLD LAYER                          │
│                    (Business Analytics)                       │
│                                                               │
│  ┌─────────────────┐   ┌─────────────────┐                  │
│  │   DIMENSIONS    │   │      FACTS      │                  │
│  │                 │   │                 │                  │
│  │ • dim_customers │   │ • fact_invoice  │                  │
│  │ • dim_products  │   │   _line_items   │                  │
│  │ • dim_regions   │   │ • fact_payments │                  │
│  └─────────────────┘   └─────────────────┘                  │
│                           │                                   │
│                           ▼                                   │
│                    ┌──────────────┐                          │
│                    │  KPI METRICS │                          │
│                    └──────────────┘                          │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  DASHBOARD   │
                    └──────────────┘
```

**Key Principles:**
- **Bronze:** Store raw data as-is from source systems (schema-on-read)
- **Silver:** Apply data quality, standardization, and business rules
- **Gold:** Build business-ready analytical tables (star schema)

---

## 💻 Technology Stack

| Component | Technology |
|-----------|-----------|
| **Platform** | Databricks (AWS) |
| **Storage** | Delta Lake |
| **Compute** | Serverless Compute |
| **Processing** | PySpark |
| **Catalog** | Unity Catalog (gwd_de) |
| **Orchestration** | Databricks Workflows / Notebook Runner |
| **Visualization** | Lakeview Dashboards |
| **Language** | Python, SQL |

---

## 📊 Data Pipeline Layers

### Layer Structure

```
gwd-databricks/
├── notebooks/
│   ├── 01_setup/          # Catalog initialization
│   ├── 02_bronze/         # Raw data ingestion
│   ├── 03_silver/         # Data transformations (7 notebooks)
│   ├── 04_gold/           # Analytical layer (3 notebooks)
│   └── 05_utils/          # Utility notebooks
└── pipeline/
    └── orchestrator_pipeline  # Master pipeline runner
```

---

## 🥉 Bronze Layer - Raw Data Ingestion

### Purpose
Ingest raw data from source systems without transformations. This layer acts as a landing zone for all source data.

### Location
- **Catalog:** `gwd_de.bronze`

### Tables

| Table | Description | Row Count (Approx) |
|-------|-------------|-------------------|
| `customers` | Customer master data | 300 |
| `products` | Product catalog | 50 |
| `invoices` | Invoice headers | 2,000 |
| `invoice_line_items` | Invoice line-level details | 15,000 |
| `payments` | Payment transactions | 1,500 |
| `exchange_rates` | Currency exchange rates | 100 |
| `countries` | Country/region mapping | 50 |

### Notebook
- **Location:** `notebooks/02_bronze/nb_ingest_all_bronze.ipynb`
- **Function:** Reads raw data and writes to bronze tables as Delta format

### Characteristics
- ✅ No transformations applied
- ✅ Preserves original data types
- ✅ Maintains full history
- ✅ Schema-on-read approach
- ✅ Delta Lake format for ACID transactions

### Example Schema (Bronze Invoices)
```
invoice_id: string
customer_id: string
invoice_date: date
invoice_month: long
currency: string
region: string
invoice_status: string
```

---

## 🥈 Silver Layer - Data Cleaning & Transformation

### Purpose
Clean, validate, standardize, and enrich data to make it ready for analytics.

### Location
- **Catalog:** `gwd_de.silver`

### Transformations Applied

#### 1. **Data Quality & Cleaning**
- **Missing Value Handling:**
  - Fill nulls in customer names with "Unknown"
  - Fill nulls in regions with "Unknown"
  - Set default values for missing prices
  
- **Duplicate Removal:**
  - Remove duplicate customer records (by customer_id)
  - Remove duplicate product records (by product_id)
  - Deduplicate invoices
  
- **Negative Quantity Handling:**
  - Filter out negative quantities (returns/adjustments)
  - Or create separate return tables if needed

#### 2. **Data Standardization**
- **Text Standardization:**
  ```python
  # Convert to uppercase
  F.upper(F.col("customer_name"))
  
  # Trim whitespace
  F.trim(F.col("region"))
  
  # Standardize status values
  F.when(F.col("status") == "paid", "Paid")
   .when(F.col("status") == "open", "Open")
   .otherwise("Cancelled")
  ```

- **Date Handling:**
  ```python
  # Convert string to date
  F.to_date(F.col("invoice_date"), "yyyy-MM-dd")
  
  # Extract month
  F.month(F.col("invoice_date"))
  ```

- **Type Conversions:**
  ```python
  # Convert to decimal for financial accuracy
  F.col("unit_price").cast(DecimalType(10, 2))
  F.col("discount").cast(DecimalType(5, 2))
  ```

#### 3. **Business Logic & Enrichment**
- **Line Total Calculation:**
  ```python
  line_total = quantity * unit_price * (1 - discount/100)
  ```

- **Currency Standardization:**
  - Join with exchange_rates table
  - Convert all amounts to base currency (USD)
  
- **Region Mapping:**
  - Standardize country names
  - Map countries to regions (North, South, East, West)

### Silver Layer Notebooks

| Notebook | Source Table | Target Table | Key Transformations |
|----------|-------------|--------------|---------------------|
| `02_bronze_to_silver_customers` | bronze.customers | silver.customers | • Remove duplicates<br>• Uppercase names<br>• Handle nulls |
| `02_bronze_to_silver_products` | bronze.products | silver.products | • Deduplicate by product_id<br>• Validate prices<br>• Standardize categories |
| `02_bronze_to_silver_invoices` | bronze.invoices | silver.invoices | • Validate dates<br>• Standardize status<br>• Map regions |
| `02_bronze_to_silver_invoice_line_items` | bronze.invoice_line_items | silver.invoice_line_items | • Calculate line_total<br>• Remove negatives<br>• Validate quantities |
| `02_bronze_to_silver_payments` | bronze.payments | silver.payments | • Validate amounts<br>• Standardize methods<br>• Link to invoices |
| `02_bronze_to_silver_exchange_rates` | bronze.exchange_rates | silver.exchange_rates | • Validate rates<br>• Handle date ranges |
| `02_bronze_to_silver_regions` | bronze.countries | silver.regions | • Map country to region<br>• Standardize names |

### Example Transformation Code

```python
# Silver Customers Transformation
df_customers = spark.table("gwd_de.bronze.customers")

df_silver_customers = df_customers \
    .dropDuplicates(["customer_id"]) \
    .withColumn("customer_name", F.upper(F.trim(F.col("customer_name")))) \
    .withColumn("customer_type", F.coalesce(F.col("customer_type"), F.lit("Standard"))) \
    .withColumn("country", F.upper(F.trim(F.col("country")))) \
    .filter(F.col("customer_id").isNotNull())

df_silver_customers.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("gwd_de.silver.customers")
```

### Data Quality Checks (Applied in Silver)
✅ Not null constraints on primary keys  
✅ Referential integrity (foreign key validation)  
✅ Value range checks (prices > 0, dates valid)  
✅ Format validation (email, phone patterns)  
✅ Duplicate detection and removal  

---

## 🥇 Gold Layer - Analytical Layer

### Purpose
Build business-ready analytical tables using **dimensional modeling (star schema)** for optimized query performance and business intelligence.

### Location
- **Catalog:** `gwd_de.gold`

### Components
1. **Dimension Tables** - Descriptive attributes
2. **Fact Tables** - Measurable business events
3. **KPI Metrics** - Pre-aggregated business metrics

---

## 🌟 Dimensional Model & Relationships

### Star Schema Design

```
                    ┌─────────────────┐
                    │  dim_customers  │
                    ├─────────────────┤
                    │ customer_id PK  │
                    │ customer_name   │
                    │ customer_type   │
                    │ country         │
                    └────────┬────────┘
                             │
                             │ 1
                             │
                             │ *
              ┌──────────────┴──────────────┐
              │                             │
    ┌─────────▼──────────────┐    ┌─────────▼──────────────┐
    │ fact_invoice_line_items│    │    fact_payments       │
    ├────────────────────────┤    ├────────────────────────┤
    │ invoice_line_id PK     │    │ payment_id PK          │
    │ invoice_id             │    │ invoice_id             │
    │ product_id FK ────┐    │    │ customer_id FK         │
    │ customer_id FK    │    │    │ region                 │
    │ region FK ────┐   │    │    │ payment_date           │
    │ quantity      │   │    │    │ payment_amount         │
    │ unit_price    │   │    │    │ payment_method         │
    │ discount      │   │    │    └────────────────────────┘
    │ line_total    │   │    │
    │ invoice_date  │   │    │
    │ currency      │   │    │
    │ invoice_status│   │    │
    └───────────────┘   │    │
                        │    │
              ┌─────────┘    │
              │              │
              │ *            │ *
              │              │
              │ 1            │ 1
    ┌─────────▼────────┐   ┌─▼────────────┐
    │  dim_products    │   │ dim_regions  │
    ├──────────────────┤   ├──────────────┤
    │ product_id PK    │   │ region PK    │
    │ product_name     │   │ region_name  │
    │ category         │   └──────────────┘
    │ cost_price       │
    └──────────────────┘
```

### Dimension Tables

#### 1. dim_customers
**Purpose:** Customer master dimension for analyzing customer behavior

```sql
CREATE TABLE gwd_de.gold.dim_customers (
    customer_id STRING,      -- Primary Key
    customer_name STRING,    -- Customer name
    customer_type STRING,    -- Retail/Wholesale/Corporate
    country STRING          -- Customer location
);
```

**Source:** `silver.customers`  
**Grain:** One row per customer  
**Rows:** ~300 customers

#### 2. dim_products
**Purpose:** Product catalog dimension for product analysis

```sql
CREATE TABLE gwd_de.gold.dim_products (
    product_id STRING,       -- Primary Key
    product_name STRING,     -- Product name
    category STRING,         -- Product category
    cost_price DECIMAL(10,2) -- Cost price
);
```

**Source:** `silver.products`  
**Grain:** One row per product  
**Rows:** ~50 products

#### 3. dim_regions
**Purpose:** Geographic dimension for regional analysis

```sql
CREATE TABLE gwd_de.gold.dim_regions (
    region STRING,           -- Primary Key
    region_name STRING       -- Region full name
);
```

**Source:** `silver.invoices` (distinct regions)  
**Grain:** One row per region  
**Rows:** 4 regions (North, South, East, West)

### Fact Tables

#### 1. fact_invoice_line_items
**Purpose:** Core transaction fact table for sales analysis

```sql
CREATE TABLE gwd_de.gold.fact_invoice_line_items (
    invoice_line_id STRING,   -- Primary Key
    invoice_id STRING,        -- Invoice reference
    product_id STRING,        -- FK → dim_products
    customer_id STRING,       -- FK → dim_customers
    region STRING,            -- FK → dim_regions
    quantity BIGINT,          -- Number of units sold
    unit_price DECIMAL(10,2), -- Price per unit
    discount DECIMAL(5,2),    -- Discount applied
    line_total DECIMAL(10,2), -- Revenue (quantity × unit_price)
    invoice_date DATE,        -- Transaction date
    currency STRING,          -- Transaction currency
    invoice_status STRING     -- Paid/Open/Cancelled
);
```

**Sources:** `silver.invoice_line_items` JOIN `silver.invoices`  
**Grain:** One row per invoice line item  
**Rows:** ~15,000 line items  
**Measures:** quantity, unit_price, discount, line_total

#### 2. fact_payments
**Purpose:** Payment transaction fact table for cash flow analysis

```sql
CREATE TABLE gwd_de.gold.fact_payments (
    payment_id STRING,        -- Primary Key
    invoice_id STRING,        -- Invoice reference
    customer_id STRING,       -- FK → dim_customers
    region STRING,            -- FK → dim_regions
    payment_date DATE,        -- Payment date
    payment_amount DECIMAL(10,2), -- Payment amount
    payment_method STRING     -- Payment method
);
```

**Sources:** `silver.payments` JOIN `silver.invoices`  
**Grain:** One row per payment transaction  
**Rows:** ~1,500 payments  
**Measures:** payment_amount

### Relationships Explained

**1. Customer Analysis Path:**
```
dim_customers → fact_invoice_line_items
  (customer_id)
```
- Allows queries like: "Total revenue by customer"
- Enables customer segmentation and ranking

**2. Product Analysis Path:**
```
dim_products → fact_invoice_line_items
  (product_id)
```
- Allows queries like: "Top-selling products by revenue"
- Enables product performance analysis

**3. Regional Analysis Path:**
```
dim_regions → fact_invoice_line_items
  (region)
```
- Allows queries like: "Revenue distribution by region"
- Enables geographic sales analysis

**4. Payment Analysis Path:**
```
dim_customers → fact_payments
  (customer_id)
```
- Allows queries like: "Payment patterns by customer"
- Enables cash flow analysis

### Gold Layer Notebooks

| Notebook | Purpose | Tables Created |
|----------|---------|----------------|
| `01_dimension_tables` | Build all dimension tables | • dim_customers<br>• dim_products<br>• dim_regions |
| `02_fact_tables` | Build fact tables with dimensional context | • fact_invoice_line_items<br>• fact_payments |
| `03_kpi_metrics` | Calculate business KPIs | • 9 KPI metric tables |

---

## 📈 KPI Calculations

### Overview
Each KPI is stored in a separate Delta table for easy consumption by dashboards and reports.

### KPI Metrics

#### 1. **Total Revenue**
**Table:** `gwd_de.gold.kpi_total_revenue`

**Calculation:**
```sql
SELECT SUM(line_total) as total_revenue
FROM gwd_de.gold.fact_invoice_line_items
WHERE invoice_status != 'Cancelled'
```

**Business Meaning:** Total sales revenue excluding cancelled orders  
**Current Value:** $12,905,079.85  
**Use Case:** Overall business performance, revenue tracking

---

#### 2. **Average Invoice Value**
**Table:** `gwd_de.gold.kpi_avg_invoice_value`

**Calculation:**
```sql
SELECT AVG(invoice_total) as avg_invoice_value
FROM (
    SELECT invoice_id, SUM(line_total) as invoice_total
    FROM gwd_de.gold.fact_invoice_line_items
    WHERE invoice_status != 'Cancelled'
    GROUP BY invoice_id
)
```

**Business Meaning:** Average transaction size  
**Current Value:** $8,672.77  
**Use Case:** Pricing strategy, upselling opportunities

---

#### 3. **Total Quantity Sold**
**Table:** `gwd_de.gold.kpi_total_quantity`

**Calculation:**
```sql
SELECT SUM(quantity) as total_quantity
FROM gwd_de.gold.fact_invoice_line_items
WHERE invoice_status != 'Cancelled'
```

**Business Meaning:** Total units sold across all products  
**Use Case:** Inventory planning, demand forecasting

---

#### 4. **Top 10 Customers by Revenue**
**Table:** `gwd_de.gold.kpi_top_customers`

**Calculation:**
```sql
SELECT 
    c.customer_id,
    c.customer_name,
    SUM(f.line_total) as customer_revenue
FROM gwd_de.gold.fact_invoice_line_items f
JOIN gwd_de.gold.dim_customers c ON f.customer_id = c.customer_id
WHERE f.invoice_status != 'Cancelled'
GROUP BY c.customer_id, c.customer_name
ORDER BY customer_revenue DESC
LIMIT 10
```

**Business Meaning:** Identify highest-value customers  
**Top Customer:** Customer_274 - $117,949.35  
**Use Case:** Customer retention, VIP programs, account management

---

#### 5. **Top 10 Products by Revenue**
**Table:** `gwd_de.gold.kpi_top_products`

**Calculation:**
```sql
SELECT 
    p.product_id,
    p.product_name,
    SUM(f.line_total) as product_revenue
FROM gwd_de.gold.fact_invoice_line_items f
JOIN gwd_de.gold.dim_products p ON f.product_id = p.product_id
WHERE f.invoice_status != 'Cancelled'
GROUP BY p.product_id, p.product_name
ORDER BY product_revenue DESC
LIMIT 10
```

**Business Meaning:** Identify best-selling products  
**Top Product:** Product_43 - $301,278.70  
**Use Case:** Inventory optimization, marketing focus, product strategy

---

#### 6. **Invoice Cancellation Rate**
**Table:** `gwd_de.gold.kpi_cancellation_rate`

**Calculation:**
```sql
SELECT 
    COUNT(DISTINCT invoice_id) as total_invoices,
    SUM(CASE WHEN invoice_status = 'Cancelled' THEN 1 ELSE 0 END) as cancelled_invoices,
    (cancelled_invoices / total_invoices) * 100 as cancellation_rate_pct
FROM gwd_de.gold.fact_invoice_line_items
```

**Business Meaning:** Percentage of orders that get cancelled  
**Current Value:** 25.6% (512 out of 2,000 invoices)  
**Use Case:** Quality control, customer satisfaction, process improvement

---

#### 7. **Total Discount Impact**
**Table:** `gwd_de.gold.kpi_discount_impact`

**Calculation:**
```sql
SELECT SUM(discount) as total_discount
FROM gwd_de.gold.fact_invoice_line_items
WHERE invoice_status != 'Cancelled'
```

**Business Meaning:** Total discount amount given to customers  
**Current Value:** $198.75  
**Use Case:** Pricing strategy, promotion effectiveness, margin analysis

---

#### 8. **Revenue by Region**
**Table:** `gwd_de.gold.kpi_revenue_by_region`

**Calculation:**
```sql
SELECT 
    region,
    SUM(line_total) as region_revenue
FROM gwd_de.gold.fact_invoice_line_items
WHERE invoice_status != 'Cancelled'
GROUP BY region
ORDER BY region_revenue DESC
```

**Business Meaning:** Geographic revenue distribution  
**Results:**
- West: $3,596,773.35 (27.9%)
- South: $3,347,260.15 (25.9%)
- East: $3,015,954.75 (23.4%)
- North: $2,945,091.60 (22.8%)

**Use Case:** Regional marketing, territory planning, expansion strategy

---

#### 9. **Invoices per Customer**
**Table:** `gwd_de.gold.kpi_invoices_per_customer`

**Calculation:**
```sql
SELECT 
    c.customer_id,
    c.customer_name,
    COUNT(DISTINCT f.invoice_id) as invoice_count
FROM gwd_de.gold.fact_invoice_line_items f
JOIN gwd_de.gold.dim_customers c ON f.customer_id = c.customer_id
WHERE f.invoice_status != 'Cancelled'
GROUP BY c.customer_id, c.customer_name
ORDER BY invoice_count DESC
LIMIT 20
```

**Business Meaning:** Customer purchase frequency  
**Most Active:** Customer_193 - 14 invoices  
**Use Case:** Customer loyalty programs, engagement tracking, retention analysis

---

## 📊 Dashboard & Visualizations

### GWD Business Intelligence Dashboard
**Location:** AI/BI Dashboard - "GWD Business Intelligence Dashboard"

### Dashboard Layout

#### Row 1: Key Metrics (4 Counter Cards)
| Widget | Metric | Value | Format |
|--------|--------|-------|--------|
| Counter 1 | Total Revenue | $12.91M | Currency (compact) |
| Counter 2 | Avg Invoice Value | $8.67K | Currency (compact) |
| Counter 3 | Cancellation Rate | 25.6% | Percentage (red if >20%) |
| Counter 4 | Total Discount | $198.75 | Currency |

#### Row 2: Regional Performance
| Widget | Type | Data Source | Purpose |
|--------|------|-------------|---------|
| Revenue by Region | Bar Chart | kpi_revenue_by_region | Compare regional sales performance |

**Visualization Details:**
- X-axis: Region (East, North, South, West)
- Y-axis: Revenue (currency format)
- Color: Distinct color per region
- Sorted: Descending by revenue

#### Row 3: Top Performers (2 Columns)
| Widget | Type | Data Source | Purpose |
|--------|------|-------------|---------|
| Top 10 Customers | Bar Chart | kpi_top_customers | Identify high-value customers |
| Top 10 Products | Bar Chart | kpi_top_products | Identify best-selling products |

#### Row 4: Customer Insights
| Widget | Type | Data Source | Purpose |
|--------|------|-------------|---------|
| Top 20 Customers by Frequency | Table | kpi_invoices_per_customer | Track customer engagement |

### Dashboard Datasets

All dashboard widgets use pre-calculated KPI tables:
```python
datasets = {
    "total_revenue": "SELECT total_revenue FROM gwd_de.gold.kpi_total_revenue",
    "avg_invoice_value": "SELECT avg_invoice_value FROM gwd_de.gold.kpi_avg_invoice_value",
    "cancellation_rate": "SELECT cancellation_rate_pct FROM gwd_de.gold.kpi_cancellation_rate",
    "total_discount": "SELECT total_discount FROM gwd_de.gold.kpi_discount_impact",
    "revenue_by_region": "SELECT region, region_revenue FROM gwd_de.gold.kpi_revenue_by_region",
    "top_customers": "SELECT customer_name, customer_revenue FROM gwd_de.gold.kpi_top_customers",
    "top_products": "SELECT product_name, product_revenue FROM gwd_de.gold.kpi_top_products",
    "invoices_per_customer": "SELECT customer_name, invoice_count FROM gwd_de.gold.kpi_invoices_per_customer"
}
```

---

## 🔄 Pipeline Orchestration

### Master Orchestrator Notebook
**Location:** `gwd-databricks/pipeline/orchestrator_pipeline`

### Purpose
Run the entire data pipeline from start to finish with a single notebook execution.

### Execution Flow

```
┌────────────────┐
│  1. Setup      │  Initialize catalog and schemas
│  Catalog       │
└───────┬────────┘
        │
        ▼
┌────────────────┐
│  2. Bronze     │  Ingest all raw data
│  Ingestion     │  (7 tables)
└───────┬────────┘
        │
        ▼
┌────────────────┐
│  3. Silver     │  Transform and clean data
│  Transformation│  (7 parallel notebooks)
│                │  • customers
│                │  • products
│                │  • invoices
│                │  • invoice_line_items
│                │  • payments
│                │  • exchange_rates
│                │  • regions
└───────┬────────┘
        │
        ▼
┌────────────────┐
│  4. Gold       │  Build dimension tables
│  Dimensions    │  (3 dimension tables)
└───────┬────────┘
        │
        ▼
┌────────────────┐
│  5. Gold       │  Build fact tables
│  Facts         │  (2 fact tables)
└───────┬────────┘
        │
        ▼
┌────────────────┐
│  6. Gold       │  Calculate KPIs
│  KPIs          │  (9 KPI tables)
└───────┬────────┘
        │
        ▼
┌────────────────┐
│  ✓ Complete    │  Pipeline finished
└────────────────┘
```

### Orchestrator Code Structure

```python
# Step 1: Setup
dbutils.notebook.run(
    "/Users/.../notebooks/01_setup/nb_init_catalog",
    timeout_seconds=600
)

# Step 2: Bronze
dbutils.notebook.run(
    "/Users/.../notebooks/02_bronze/nb_ingest_all_bronze",
    timeout_seconds=600
)

# Step 3: Silver (7 notebooks)
dbutils.notebook.run(
    "/Users/.../notebooks/03_silver/02_bronze_to_silver_customers",
    timeout_seconds=600
)
# ... (repeat for all 7 silver notebooks)

# Step 4: Gold Dimensions
dbutils.notebook.run(
    "/Users/.../notebooks/04_gold/01_dimension_tables",
    timeout_seconds=600
)

# Step 5: Gold Facts
dbutils.notebook.run(
    "/Users/.../notebooks/04_gold/02_fact_tables",
    timeout_seconds=600
)

# Step 6: Gold KPIs
dbutils.notebook.run(
    "/Users/.../notebooks/04_gold/03_kpi_metrics",
    timeout_seconds=600
)
```

### Error Handling
- Each notebook run has 600-second timeout
- If any notebook fails, the orchestrator stops
- Success messages printed after each step
- Full execution time: ~10-15 minutes (depending on data volume)

---

## 🚀 How to Run the Pipeline

### Option 1: Run Master Orchestrator (Recommended)
**Easiest way to run the entire pipeline:**

1. Open the orchestrator notebook:
   ```
   /Users/rahulparaselli8374@gmail.com/gwd-databricks/pipeline/orchestrator_pipeline
   ```

2. Click **"Run All"** in the notebook

3. Monitor progress as each step completes:
   - ✓ Setup completed
   - ✓ Bronze layer ingestion completed
   - ✓ Silver transformations completed
   - ✓ Gold dimensions completed
   - ✓ Gold facts completed
   - ✓ Gold KPIs completed

4. Total execution time: ~10-15 minutes

### Option 2: Run Individual Notebooks
**For debugging or partial pipeline runs:**

#### Step 1: Setup (First Time Only)
```
notebooks/01_setup/nb_init_catalog
```
Creates catalog and schemas: bronze, silver, gold

#### Step 2: Bronze Layer
```
notebooks/02_bronze/nb_ingest_all_bronze
```
Loads raw data into bronze tables

#### Step 3: Silver Layer (Run all 7)
```
notebooks/03_silver/02_bronze_to_silver_customers
notebooks/03_silver/02_bronze_to_silver_products
notebooks/03_silver/02_bronze_to_silver_invoices
notebooks/03_silver/02_bronze_to_silver_invoice_line_items
notebooks/03_silver/02_bronze_to_silver_payments
notebooks/03_silver/02_bronze_to_silver_exchange_rates
notebooks/03_silver/02_bronze_to_silver_regions
```

#### Step 4: Gold Layer - Dimensions
```
notebooks/04_gold/01_dimension_tables
```
Creates dim_customers, dim_products, dim_regions

#### Step 5: Gold Layer - Facts
```
notebooks/04_gold/02_fact_tables
```
Creates fact_invoice_line_items, fact_payments

#### Step 6: Gold Layer - KPIs
```
notebooks/04_gold/03_kpi_metrics
```
Calculates and stores all 9 KPIs

### Option 3: Schedule as Databricks Job
**For production automation:**

1. Create a new Databricks Job
2. Add the orchestrator notebook as a single task
3. Configure schedule (e.g., daily at 6 AM)
4. Set up email notifications for success/failure
5. Use serverless compute for cost optimization

### Verification Steps

After running the pipeline, verify data:

```sql
-- Check bronze row counts
SELECT 'customers' as table_name, COUNT(*) as row_count FROM gwd_de.bronze.customers
UNION ALL
SELECT 'invoices', COUNT(*) FROM gwd_de.bronze.invoices
UNION ALL
SELECT 'invoice_line_items', COUNT(*) FROM gwd_de.bronze.invoice_line_items;

-- Check silver data quality
SELECT COUNT(*) as total_customers, 
       COUNT(DISTINCT customer_id) as unique_customers
FROM gwd_de.silver.customers;

-- Check gold dimensional model
SELECT 'dim_customers' as table_name, COUNT(*) FROM gwd_de.gold.dim_customers
UNION ALL
SELECT 'dim_products', COUNT(*) FROM gwd_de.gold.dim_products
UNION ALL
SELECT 'fact_invoice_line_items', COUNT(*) FROM gwd_de.gold.fact_invoice_line_items;

-- Check KPI calculations
SELECT * FROM gwd_de.gold.kpi_total_revenue;
SELECT * FROM gwd_de.gold.kpi_top_customers;
```

---

## 📊 Data Lineage

### Complete Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        SOURCE SYSTEMS                            │
│   CSV Files | APIs | Databases | Cloud Storage                  │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                         BRONZE LAYER                             │
│                   Unity Catalog: gwd_de.bronze                   │
├──────────────────┬──────────────────┬────────────────────────────┤
│  customers       │  products        │  invoices                  │
│  (300 rows)      │  (50 rows)       │  (2,000 rows)              │
├──────────────────┼──────────────────┼────────────────────────────┤
│  invoice_line    │  payments        │  exchange_rates            │
│  _items          │  (1,500 rows)    │  (100 rows)                │
│  (15,000 rows)   │                  │                            │
└────────┬─────────┴────────┬─────────┴─────────┬──────────────────┘
         │                  │                   │
         ▼                  ▼                   ▼
┌─────────────────────────────────────────────────────────────────┐
│                         SILVER LAYER                             │
│                   Unity Catalog: gwd_de.silver                   │
│                                                                  │
│  Transformations Applied:                                        │
│  • Data Quality Checks                                           │
│  • Deduplication                                                 │
│  • Standardization (uppercase, trim)                             │
│  • Type Conversions (string → decimal)                           │
│  • Business Logic (line_total calculation)                       │
│  • Null Handling                                                 │
├──────────────────┬──────────────────┬────────────────────────────┤
│  customers       │  products        │  invoices                  │
│  (clean)         │  (clean)         │  (clean)                   │
├──────────────────┼──────────────────┼────────────────────────────┤
│  invoice_line    │  payments        │  exchange_rates            │
│  _items (clean)  │  (clean)         │  (clean)                   │
└────────┬─────────┴────────┬─────────┴─────────┬──────────────────┘
         │                  │                   │
         │                  ▼                   │
         │     ┌────────────────────────┐       │
         │     │   Dimensional Model    │       │
         │     │   Design & Build       │       │
         │     └───────────┬────────────┘       │
         │                 │                    │
         ▼                 ▼                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                          GOLD LAYER                              │
│                   Unity Catalog: gwd_de.gold                     │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              DIMENSION TABLES                              │ │
│  ├────────────────────┬────────────────────┬──────────────────┤ │
│  │  dim_customers     │  dim_products      │  dim_regions     │ │
│  │  (300 rows)        │  (50 rows)         │  (4 rows)        │ │
│  └────────────────────┴────────────────────┴──────────────────┘ │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              FACT TABLES                                   │ │
│  ├──────────────────────────────┬─────────────────────────────┤ │
│  │  fact_invoice_line_items     │  fact_payments              │ │
│  │  (15,000 rows)                │  (1,500 rows)               │ │
│  │  • Links to dim_customers    │  • Links to dim_customers   │ │
│  │  • Links to dim_products     │  • Payment transaction data │ │
│  │  • Links to dim_regions      │                             │ │
│  └──────────────────────────────┴─────────────────────────────┘ │
│                                │                                 │
│                                ▼                                 │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              KPI METRICS (9 tables)                        │ │
│  ├────────────────────────────────────────────────────────────┤ │
│  │  1. kpi_total_revenue                                      │ │
│  │  2. kpi_avg_invoice_value                                  │ │
│  │  3. kpi_total_quantity                                     │ │
│  │  4. kpi_top_customers                                      │ │
│  │  5. kpi_top_products                                       │ │
│  │  6. kpi_cancellation_rate                                  │ │
│  │  7. kpi_discount_impact                                    │ │
│  │  8. kpi_revenue_by_region                                  │ │
│  │  9. kpi_invoices_per_customer                              │ │
│  └────────────────────────────────────────────────────────────┘ │
└──────────────────────────────┬───────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    LAKEVIEW DASHBOARD                            │
│              GWD Business Intelligence Dashboard                 │
│                                                                  │
│  • 4 Counter Widgets (Key Metrics)                              │
│  • 3 Bar Charts (Regional, Customers, Products)                 │
│  • 1 Table (Customer Frequency)                                 │
│  • Auto-refresh from gold KPI tables                            │
└─────────────────────────────────────────────────────────────────┘
```

### Table Dependencies

#### Bronze → Silver Dependencies
```
bronze.customers              → silver.customers
bronze.products               → silver.products
bronze.invoices               → silver.invoices
bronze.invoice_line_items     → silver.invoice_line_items
bronze.payments               → silver.payments
bronze.exchange_rates         → silver.exchange_rates
bronze.countries              → silver.regions
```

#### Silver → Gold Dependencies
```
silver.customers              → gold.dim_customers
silver.products               → gold.dim_products
silver.invoices               → gold.dim_regions

silver.invoice_line_items  \
silver.invoices            / → gold.fact_invoice_line_items

silver.payments            \
silver.invoices            / → gold.fact_payments
```

#### Gold → KPI Dependencies
```
gold.fact_invoice_line_items           → All KPI tables
gold.dim_customers                     → kpi_top_customers
                                       → kpi_invoices_per_customer
gold.dim_products                      → kpi_top_products
```

### Column Lineage Examples

#### Example 1: Total Revenue Lineage
```
Source: bronze.invoice_line_items.quantity
                                 .unit_price

  ↓ Silver Transformation
  
silver.invoice_line_items.line_total = quantity * unit_price

  ↓ Gold Fact Build
  
gold.fact_invoice_line_items.line_total

  ↓ KPI Calculation
  
gold.kpi_total_revenue.total_revenue = SUM(line_total)

  ↓ Dashboard Display
  
Dashboard: Total Revenue Counter Widget
```

#### Example 2: Customer Revenue Lineage
```
Source: bronze.customers.customer_id
                        .customer_name
        bronze.invoice_line_items.line_total

  ↓ Silver Transformation
  
silver.customers (cleaned & standardized)
silver.invoice_line_items (validated)

  ↓ Gold Dimension Build
  
gold.dim_customers.customer_id
                 .customer_name

  ↓ Gold Fact Build
  
gold.fact_invoice_line_items (linked to customers)

  ↓ KPI Calculation
  
gold.kpi_top_customers = 
  GROUP BY customer_id, customer_name
  SUM(line_total) as customer_revenue

  ↓ Dashboard Display
  
Dashboard: Top 10 Customers Bar Chart
```

---

## 📝 Additional Notes

### Best Practices Implemented

1. **Medallion Architecture**
   - Clear separation of raw, cleaned, and analytical data
   - Enables data quality improvement at each layer
   - Supports data reprocessing without affecting source

2. **Dimensional Modeling**
   - Star schema for optimized query performance
   - Separate facts and dimensions for flexibility
   - Conformed dimensions for enterprise consistency

3. **Delta Lake Features**
   - ACID transactions ensure data consistency
   - Time travel for data versioning
   - Schema evolution support
   - Optimized file layout for performance

4. **Data Quality**
   - Validation at silver layer
   - Deduplication and null handling
   - Type safety with explicit conversions
   - Business rule enforcement

5. **Performance Optimization**
   - Pre-aggregated KPI tables
   - Partitioning by date (where applicable)
   - Z-ordering for frequently filtered columns
   - Compact tables regularly

### Troubleshooting

**Issue: Bronze ingestion fails**
- Check source data availability
- Verify file paths and formats
- Ensure catalog permissions

**Issue: Silver transformation errors**
- Review data quality logs
- Check for schema changes in bronze
- Validate business logic calculations

**Issue: Gold layer build failures**
- Ensure silver layer completed successfully
- Check referential integrity (foreign keys)
- Verify join conditions

**Issue: KPI calculations incorrect**
- Review filter conditions (e.g., excluding cancelled)
- Validate aggregation logic
- Check for duplicate records in source

**Issue: Dashboard not updating**
- Refresh dataset queries
- Verify KPI tables have data
- Check warehouse connectivity

### Maintenance Tasks

**Daily:**
- Run orchestrator pipeline (automated)
- Monitor job execution status
- Review data quality metrics

**Weekly:**
- Optimize Delta tables (`OPTIMIZE` command)
- Review KPI trends and anomalies
- Check storage usage

**Monthly:**
- Archive old bronze data
- Vacuum Delta tables (remove old versions)
- Update documentation for schema changes
- Review and optimize slow queries

---

## 🎓 Learning Resources

### Databricks Documentation
- [Medallion Architecture](https://www.databricks.com/glossary/medallion-architecture)
- [Delta Lake](https://docs.delta.io/)
- [Unity Catalog](https://docs.databricks.com/data-governance/unity-catalog/index.html)
- [Lakeview Dashboards](https://docs.databricks.com/dashboards/lakeview.html)

### Data Modeling
- [Star Schema Design](https://en.wikipedia.org/wiki/Star_schema)
- [Kimball Dimensional Modeling](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/)

---

## 👥 Contributors

**Project:** GWD Data Engineering Team  
**Architecture:** Medallion Pattern with Star Schema  
**Platform:** Databricks on AWS  
**Last Updated:** 2024

---

## 📄 License

Internal use only - GWD Data Engineering Project

---

**End of Documentation**

For questions or support, contact the data engineering team.
