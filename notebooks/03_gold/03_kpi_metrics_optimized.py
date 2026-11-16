# Databricks notebook source
# DBTITLE 1,Configuration
from pyspark.sql import functions as F
from pyspark.sql.window import Window

CATALOG = "gwd_de"

fact_line_items = f"{CATALOG}.gold.fact_invoice_line_items"
fact_payments = f"{CATALOG}.gold.fact_payments"
dim_customers = f"{CATALOG}.gold.dim_customers"
dim_products = f"{CATALOG}.gold.dim_products"

# COMMAND ----------

# DBTITLE 1,Optimized KPI Metrics - Create base filtered data once
df_line_items = spark.table(fact_line_items)

# Create base filtered dataset once to avoid repeated filtering
df_active_line_items = df_line_items.filter(F.col("invoice_status") != "Cancelled")

# COMMAND ----------

# DBTITLE 1,Calculate Total Revenue (Optimized)
total_revenue = df_active_line_items.agg(F.sum("line_total").alias("total_revenue"))

# Write to separate table
total_revenue_table = f"{CATALOG}.gold.kpi_total_revenue"
total_revenue.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable(total_revenue_table)

print(f"✓ Total Revenue calculated and saved to {total_revenue_table}")
display(total_revenue)

# COMMAND ----------

# DBTITLE 1,Calculate Multiple KPIs in Single Operations

# Pre-compute invoice-level aggregations for reuse
invoice_aggregations = df_active_line_items.groupBy("invoice_id") \
    .agg(F.sum("line_total").alias("invoice_total"), \
         F.count("line_total").alias("line_item_count"))

# Average Invoice Value (using pre-computed aggregations)
avg_invoice_value = invoice_aggregations.agg(F.avg("invoice_total").alias("avg_invoice_value"))

# Write average invoice value
avg_invoice_table = f"{CATALOG}.gold.kpi_avg_invoice_value"
avg_invoice_value.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable(avg_invoice_table)

print(f"✓ Average Invoice Value calculated and saved to {avg_invoice_table}")
display(avg_invoice_value)

# COMMAND ----------

# DBTITLE 1,Calculate Top Customers and Top Products Simultaneously

# Load dimension tables once
df_customers = spark.table(dim_customers)
df_products = spark.table(dim_products)

# Calculate customer revenue (reusing df_active_line_items)
customer_revenue = df_active_line_items.groupBy("customer_id") \
    .agg(F.sum("line_total").alias("customer_revenue"))

# Calculate product revenue (reusing df_active_line_items)
product_revenue = df_active_line_items.groupBy("product_id") \
    .agg(F.sum("line_total").alias("product_revenue"))

# Join with customer and product dimensions
customer_revenue_enriched = customer_revenue.join(df_customers, "customer_id", "left") \
    .select("customer_id", "customer_name", "customer_revenue") \
    .orderBy(F.desc("customer_revenue")) \
    .limit(10)

product_revenue_enriched = product_revenue.join(df_products, "product_id", "left") \
    .select("product_id", "product_name", "product_revenue") \
    .orderBy(F.desc("product_revenue")) \
    .limit(10)

# Write both results in parallel
from concurrent.futures import ThreadPoolExecutor

def write_table(df, table_name, description):
    df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(table_name)
    print(f"✓ {description} calculated and saved to {table_name}")

# Execute both writes
with ThreadPoolExecutor(max_workers=2) as executor:
    executor.submit(write_table, customer_revenue_enriched, 
                   f"{CATALOG}.gold.kpi_top_customers", 
                   "Top 10 Customers")
    executor.submit(write_table, product_revenue_enriched,
                   f"{CATALOG}.gold.kpi_top_products",
                   "Top 10 Products")

# Display results for verification
display(customer_revenue_enriched)
display(product_revenue_enriched)

# COMMAND ----------

# DBTITLE 1,Calculate Cancellation Rate (Optimized)
# Get distinct invoice statuses from filtered data (no need to re-filter)
invoice_statuses = df_line_items.select("invoice_id", "invoice_status").distinct()

cancellation_rate = invoice_statuses.agg(
    F.count("invoice_id").alias("total_invoices"),
    F.sum(F.when(F.col("invoice_status") == "Cancelled", 1).otherwise(0)).alias("cancelled_invoices")
).withColumn("cancellation_rate_pct", (F.col("cancelled_invoices") / F.col("total_invoices")) * 100)

# Write cancellation rate
cancellation_rate_table = f"{CATALOG}.gold.kpi_cancellation_rate"
cancellation_rate.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable(cancellation_rate_table)

print(f"✓ Invoice Cancellation Rate calculated and saved to {cancellation_rate_table}")
display(cancellation_rate)

# COMMAND ----------

# DBTITLE 1,Calculate Discount Impact and Revenue by Region (Combined Operations)

# Calculate discount impact
 discount_impact = df_active_line_items.agg(F.sum("discount").alias("total_discount"))

# Calculate revenue by region
 revenue_by_region = df_active_line_items.groupBy("region") \
    .agg(F.sum("line_total").alias("region_revenue"), \
         F.count("invoice_id").alias("invoice_count"),
         F.avg("line_total").alias("avg_region_revenue")) \
    .orderBy(F.desc("region_revenue"))

# Write results
with ThreadPoolExecutor(max_workers=2) as executor:
    executor.submit(write_table, discount_impact,
                   f"{CATALOG}.gold.kpi_discount_impact",
                   "Total Discount")
    executor.submit(write_table, revenue_by_region,
                   f"{CATALOG}.gold.kpi_revenue_by_region",
                   "Revenue by Region")

display(discount_impact)
display(revenue_by_region)

# COMMAND ----------

# DBTITLE 1,Calculate Invoices per Customer (Optimized)
# Use already filtered data to avoid re-filtering
invoices_per_customer = df_active_line_items.select("customer_id", "invoice_id") \
    .distinct() \
    .groupBy("customer_id") \
    .agg(F.count("invoice_id").alias("invoice_count")) \
    .join(df_customers, "customer_id", "left") \
    .select("customer_id", "customer_name", "invoice_count") \
    .orderBy(F.desc("invoice_count")) \
    .limit(20)

invoices_per_customer_table = f"{CATALOG}.gold.kpi_invoices_per_customer"
invoices_per_customer.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable(invoices_per_customer_table)

print(f"✓ Invoices per Customer calculated and saved to {invoices_per_customer_table}")
display(invoices_per_customer)
