# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "6"
# ///
# DBTITLE 0,Configuration
from pyspark.sql import functions as F

CATALOG = "gwd_de"
source_table = f"{CATALOG}.bronze.customers"
target_table = f"{CATALOG}.silver.customers"

# COMMAND ----------

# DBTITLE 0,Read and Transform
df_bronze = spark.table(source_table)

# Explicit column control; standardises country names.
# Use vectorized string functions for better performance
df_silver = df_bronze.select(
    "customer_id",
    "customer_name",
    F.initcap("customer_type").alias("customer_type"),
    F.coalesce(
        F.when(F.col("country") == "U.S.A", "USA")
         .otherwise(F.initcap(F.col("country"))),
        F.lit("Unknown")
    ).alias("country"),
    "signup_date"
)

# Bronze contains duplicate customer_ids; ensure exactly one row per customer_id
df_silver = df_silver.dropDuplicates(["customer_id"])

# COMMAND ----------

# DBTITLE 1,Write (upsert)
from delta.tables import DeltaTable

# Bronze re-lands whole files, so MERGE keeps silver current without
# dropping history or rewriting the table. Delta needs BOTH aliases and a
# de-duplicated source, or the merge aborts with MULTIPLE_MATCHING_ROWS_ON_MERGE.
# df_silver was already de-duplicated in the transform cell above.

try:
    (DeltaTable.forName(spark, target_table)
     .alias("tgt")
     .merge(df_silver.alias("src"), "tgt.`customer_id` = src.`customer_id`")
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

