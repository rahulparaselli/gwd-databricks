# Databricks notebook source
# DBTITLE 1,Configuration
from pyspark.sql import functions as F
from pyspark.sql.types import DecimalType

CATALOG = "gwd_de"
source_table = f"{CATALOG}.bronze.invoice_line_items"
target_table = f"{CATALOG}.silver.invoice_line_items"

# COMMAND ----------

# DBTITLE 1,Read and Transform
df_bronze = spark.table(source_table)

df_silver = df_bronze.select(
    F.col("invoice_line_id"),
    F.col("invoice_id"),
    F.col("product_id"),
    F.col("quantity"),
    F.coalesce(F.col("unit_price").cast(DecimalType(10, 2)), F.lit(0.00)).alias("unit_price"),
    F.coalesce(F.col("discount"), F.lit(0.00)).alias("discount")
)

df_silver = df_silver.withColumn(
    "line_total",
    (F.col("quantity") * F.col("unit_price") * (F.lit(1) - F.col("discount"))).cast(DecimalType(10, 2))
)

# COMMAND ----------

# DBTITLE 1,Write (upsert)
from delta.tables import DeltaTable

# Bronze re-lands whole files, so MERGE keeps silver current without
# dropping history or rewriting the table. Delta needs BOTH aliases and a
# de-duplicated source, or the merge aborts with MULTIPLE_MATCHING_ROWS_ON_MERGE.
df_silver = df_silver.dropDuplicates(['invoice_line_id'])

try:
    (DeltaTable.forName(spark, target_table)
     .alias("tgt")
     .merge(df_silver.alias("src"), "tgt.`invoice_line_id` = src.`invoice_line_id`")
     .whenMatchedUpdateAll()
     .whenNotMatchedInsertAll()
     .execute())
    how = "merged (upsert)"
except Exception as exc:
    text = str(exc).upper()
    if "TABLE_OR_VIEW_NOT_FOUND" not in text and "DOES NOT EXIST" not in text:
        raise
    # first run only: the table is not there yet, so create it
    df_silver.write.format("delta").mode("overwrite").saveAsTable(target_table)
    how = "created (first run) after " + type(exc).__name__

rows = spark.table(target_table).count()
msg = f"{target_table}: {how}, {rows} rows"
print(msg)
dbutils.notebook.exit(msg)

