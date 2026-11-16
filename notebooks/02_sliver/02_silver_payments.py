# Databricks notebook source
# DBTITLE 1,Configuration
from pyspark.sql import functions as F
from pyspark.sql.types import DecimalType

CATALOG = "gwd_de"
source_table = f"{CATALOG}.bronze.payments"
target_table = f"{CATALOG}.silver.payments"

# COMMAND ----------

# DBTITLE 1,Read and Transform
df_bronze = spark.table(source_table)

df_silver = df_bronze.select(
    F.col("payment_id"),
    F.col("invoice_id"),
    F.to_date(F.col("payment_date"), "yyyy/M/d").alias("payment_date"),
    F.col("payment_amount").cast(DecimalType(10, 2)).alias("payment_amount"),
    F.initcap(F.col("payment_method")).alias("payment_method")
)

# COMMAND ----------

# DBTITLE 1,Write (upsert)
from delta.tables import DeltaTable

# Bronze re-lands whole files, so MERGE keeps silver current without
# dropping history or rewriting the table. Delta needs BOTH aliases and a
# de-duplicated source, or the merge aborts with MULTIPLE_MATCHING_ROWS_ON_MERGE.
df_silver = df_silver.dropDuplicates(['payment_id'])

try:
    (DeltaTable.forName(spark, target_table)
     .alias("tgt")
     .merge(df_silver.alias("src"), "tgt.`payment_id` = src.`payment_id`")
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

