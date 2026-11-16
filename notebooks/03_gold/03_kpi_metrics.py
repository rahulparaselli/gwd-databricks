# Databricks notebook source
# DBTITLE 1,Configuration
from pyspark.sql import functions as F

CATALOG = "gwd_de"

fact_line_items = f"{CATALOG}.gold.fact_invoice_line_items"
fact_payments = f"{CATALOG}.gold.fact_payments"
dim_customers = f"{CATALOG}.gold.dim_customers"
dim_products = f"{CATALOG}.gold.dim_products"

# COMMAND ----------

# DBTITLE 1,Calculate Total Revenue
df_line_items = spark.table(fact_line_items)

# All KPIs except the cancellation rate read this exact active slice;
# scan + cache it ONCE instead of re-reading and re-filtering the fact
# table in every cell.
df_active = df_line_items.filter(F.col("invoice_status") != "Cancelled").cache()

total_revenue = df_active \
    .agg(F.sum("line_total").alias("total_revenue"))

# Write to separate table
total_revenue_table = f"{CATALOG}.gold.kpi_total_revenue"
total_revenue.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable(total_revenue_table)

print(f"✓ Total Revenue calculated and saved to {total_revenue_table}")
# COMMAND ----------

# DBTITLE 1,Calculate Total Quantity
avg_invoice_value = df_active \
    .groupBy("invoice_id") \
    .agg(F.sum("line_total").alias("invoice_total")) \
    .agg(F.avg("invoice_total").alias("avg_invoice_value"))

# Write to separate table
avg_invoice_table = f"{CATALOG}.gold.kpi_avg_invoice_value"
avg_invoice_value.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable(avg_invoice_table)

print(f"✓ Average Invoice Value calculated and saved to {avg_invoice_table}")
# COMMAND ----------

# DBTITLE 1,Calculate Top Customers
df_customers = spark.table(dim_customers)

top_customers = df_active \
    .groupBy("customer_id") \
    .agg(F.sum("line_total").alias("customer_revenue")) \
    .join(df_customers, "customer_id", "left") \
    .select(
        "customer_id",
        "customer_name",
        "customer_revenue"
    ) \
    .orderBy(F.desc("customer_revenue")) \
    .limit(10)

top_customers_table = f"{CATALOG}.gold.kpi_top_customers"
top_customers.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable(top_customers_table)

print(f"✓ Top 10 Customers calculated and saved to {top_customers_table}")
# COMMAND ----------

# DBTITLE 1,Calculate Top Products
df_products = spark.table(dim_products)

top_products = df_active \
    .groupBy("product_id") \
    .agg(F.sum("line_total").alias("product_revenue")) \
    .join(df_products, "product_id", "left") \
    .select(
        "product_id",
        "product_name",
        "product_revenue"
    ) \
    .orderBy(F.desc("product_revenue")) \
    .limit(10)

top_products_table = f"{CATALOG}.gold.kpi_top_products"
top_products.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable(top_products_table)

print(f"✓ Top 10 Products calculated and saved to {top_products_table}")
# COMMAND ----------

# DBTITLE 1,Calculate Cancellation Rate
cancellation_rate = df_line_items \
    .select("invoice_id", "invoice_status") \
    .distinct() \
    .agg(
        F.count("invoice_id").alias("total_invoices"),
        F.sum(F.when(F.col("invoice_status") == "Cancelled", 1).otherwise(0)).alias("cancelled_invoices")
    ) \
    .withColumn("cancellation_rate_pct", (F.col("cancelled_invoices") / F.col("total_invoices")) * 100)

# Write to separate table
cancellation_rate_table = f"{CATALOG}.gold.kpi_cancellation_rate"
cancellation_rate.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable(cancellation_rate_table)

print(f"✓ Invoice Cancellation Rate calculated and saved to {cancellation_rate_table}")
# COMMAND ----------

# DBTITLE 1,Calculate Discount Impact
discount_impact = df_active \
    .agg(F.sum("discount").alias("total_discount"))

# Write to separate table
discount_impact_table = f"{CATALOG}.gold.kpi_discount_impact"
discount_impact.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable(discount_impact_table)

print(f"✓ Total Discount calculated and saved to {discount_impact_table}")
# COMMAND ----------

# DBTITLE 1,Calculate Revenue by Region
revenue_by_region = df_active \
    .groupBy("region") \
    .agg(F.sum("line_total").alias("region_revenue")) \
    .orderBy(F.desc("region_revenue"))

revenue_by_region_table = f"{CATALOG}.gold.kpi_revenue_by_region"
revenue_by_region.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable(revenue_by_region_table)

print(f"✓ Revenue by Region calculated and saved to {revenue_by_region_table}")
# COMMAND ----------

# DBTITLE 1,Calculate Invoices per Customer
invoices_per_customer = df_active \
    .select("customer_id", "invoice_id") \
    .distinct() \
    .groupBy("customer_id") \
    .agg(F.count("invoice_id").alias("invoice_count")) \
    .join(df_customers, "customer_id", "left") \
    .select(
        "customer_id",
        "customer_name",
        "invoice_count"
    ) \
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
