# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "6"
# ///
# DBTITLE 1,Test Optimized Silver Transformations
# Comprehensive data quality validation for all optimized silver transformation notebooks

from pyspark.sql import functions as F
from pyspark.sql.types import DecimalType

CATALOG = "gwd_de"

# COMMAND ----------

# DBTITLE 2,Test Customers Transformation
print("Testing optimized customers transformation...")
df_customers = spark.table(f"{CATALOG}.silver.customers")
customers_count = df_customers.count()
print(f"Customers table: {customers_count} rows")

# Validate data quality
null_customer_id = df_customers.filter(F.col("customer_id").isNull()).count()
null_customer_name = df_customers.filter(F.col("customer_name").isNull()).count()
duplicate_customer_ids = df_customers.groupBy("customer_id").count().filter(F.col("count") > 1).count()
invalid_country = df_customers.filter(F.col("country").isin("USA", "UK", "Canada", "Germany")).count()  # Sample validation

print(f"Customers quality check - Null customer_id: {null_customer_id}, Null customer_name: {null_customer_name}, Duplicate customer_ids: {duplicate_customer_ids}")

# COMMAND ----------

# DBTITLE 2,Test Invoices Transformation
print("Testing optimized invoices transformation...")
df_invoices = spark.table(f"{CATALOG}.silver.invoices")
invoices_count = df_invoices.count()
print(f"Invoices table: {invoices_count} rows")

# Validate data quality
null_invoice_id = df_invoices.filter(F.col("invoice_id").isNull()).count()
invalid_date_format = df_invoices.filter(F.col("invoice_date").isNull()).count()
invalid_currency = df_invoices.filter(F.col("currency").isNull()).count()

print(f"Invoices quality check - Null invoice_id: {null_invoice_id}, Invalid dates: {invalid_date_format}, Invalid currency: {invalid_currency}")

# COMMAND ----------

# DBTITLE 2,Test Products Transformation
print("Testing optimized products transformation...")
df_products = spark.table(f"{CATALOG}.silver.products")
products_count = df_products.count()
print(f"Products table: {products_count} rows")

# Validate data quality
null_product_id = df_products.filter(F.col("product_id").isNull()).count()
null_category = df_products.filter(F.col("category").isNull()).count()
negative_cost = df_products.filter(F.col("cost_price") < 0).count()

print(f"Products quality check - Null product_id: {null_product_id}, Null category: {null_category}, Negative cost: {negative_cost}")

# COMMAND ----------

# DBTITLE 2,Test Regions Transformation
print("Testing optimized regions transformation...")
df_regions = spark.table(f"{CATALOG}.silver.regions")
regions_count = df_regions.count()
print(f"Regions table: {regions_count} rows")

# Validate data quality
null_region_code = df_regions.filter(F.col("region_code").isNull()).count()
null_region_name = df_regions.filter(F.col("region_name").isNull()).count()

print(f"Regions quality check - Null region_code: {null_region_code}, Null region_name: {null_region_name}")

# COMMAND ----------

# DBTITLE 2,Test Payments Transformation
print("Testing optimized payments transformation...")
df_payments = spark.table(f"{CATALOG}.silver.payments")
payments_count = df_payments.count()
print(f"Payments table: {payments_count} rows")

# Validate data quality
null_payment_id = df_payments.filter(F.col("payment_id").isNull()).count()
null_payment_amount = df_payments.filter(F.col("payment_amount").isNull()).count()
negative_payment = df_payments.filter(F.col("payment_amount") < 0).count()

print(f"Payments quality check - Null payment_id: {null_payment_id}, Null payment_amount: {null_payment_amount}, Negative payment: {negative_payment}")

# COMMAND ----------

# DBTITLE 2,Test Invoice Line Items Transformation
print("Testing optimized invoice line items transformation...")
df_line_items = spark.table(f"{CATALOG}.silver.invoice_line_items")
line_items_count = df_line_items.count()
print(f"Invoice line items table: {line_items_count} rows")

# Validate data quality
null_line_id = df_line_items.filter(F.col("invoice_line_id").isNull()).count()
negative_quantity = df_line_items.filter(F.col("quantity") < 0).count()
negative_unit_price = df_line_items.filter(F.col("unit_price") < 0).count()
invalid_discount = df_line_items.filter(F.col("discount") < 0).or(F.col("discount") > 1.0).count()
null_line_total = df_line_items.filter(F.col("line_total").isNull()).count()

print(f"Line items quality check - Null line_id: {null_line_id}, Negative quantity: {negative_quantity}, Invalid discount: {invalid_discount}, Null line_total: {null_line_total}")

# COMMAND ----------

# DBTITLE 2,Test Exchange Rates Transformation
print("Testing optimized exchange rates transformation...")
df_exchange_rates = spark.table(f"{CATALOG}.silver.exchange_rates")
exchange_rates_count = df_exchange_rates.count()
print(f"Exchange rates table: {exchange_rates_count} rows")

# Validate data quality
null_date = df_exchange_rates.filter(F.col("date").isNull()).count()
null_currency = df_exchange_rates.filter(F.col("currency").isNull()).count()
null_rate = df_exchange_rates.filter(F.col("rate_to_usd").isNull()).count()
negative_rate = df_exchange_rates.filter(F.col("rate_to_usd") <= 0).count()

print(f"Exchange rates quality check - Null date: {null_date}, Null currency: {null_currency}, Null/negative rate: {null_rate + negative_rate}")

# COMMAND ----------

# DBTITLE 3,Final Validation Summary
print("\n" + "="*50)
print("OPTIMIZED TRANSFORMATIONS VALIDATION SUMMARY")
print("="*50)

tables_summary = [
    ("Customers", customers_count, null_customer_id + null_customer_name + duplicate_customer_ids),
    ("Invoices", invoices_count, null_invoice_id + invalid_date_format + invalid_currency),
    ("Products", products_count, null_product_id + null_category + negative_cost),
    ("Regions", regions_count, null_region_code + null_region_name),
    ("Payments", payments_count, null_payment_id + null_payment_amount + negative_payment),
    ("Line Items", line_items_count, null_line_id + negative_quantity + invalid_discount + null_line_total),
    ("Exchange Rates", exchange_rates_count, null_date + null_currency + null_rate + negative_rate)
]

total_issues = sum([summary[2] for summary in tables_summary])
print(f"Total data quality issues found: {total_issues}")
for table, count, issues in tables_summary:
    print(f"{table}: {count} rows, {issues} issues")

if total_issues == 0:
    print("\n✅ All optimized transformations passed data quality validation!")
else:
    print(f"\n⚠️  {total_issues} data quality issues found - review necessary")

print("\n✅ OPTIMIZED TRANSFORMATIONS TEST COMPLETED")
dbutils.notebook.exit(f"Optimized transformations test completed - {total_issues} issues found")
