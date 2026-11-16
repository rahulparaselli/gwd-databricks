# Databricks notebook source
# DBTITLE 0,Configuration
from pyspark.sql import functions as F

CATALOG = "gwd_de"
source_table = f"{CATALOG}.bronze.exchange_rates"
target_table = f"{CATALOG}.silver.exchange_rates"

# COMMAND ----------

# DBTITLE 0,Read and Transform
df_bronze = spark.table(source_table)

df_silver = df_bronze.select(
    F.to_date(F.col("date"), "yyyy/M/d").alias("date"),
    F.upper(F.col("currency")).alias("currency"),
    F.col("rate_to_usd")
)

# COMMAND ----------

# DBTITLE 1,Write (upsert)
from delta.tables import DeltaTable

# Bronze re-lands whole files, so MERGE keeps silver current without
# dropping history or rewriting the table. Delta needs BOTH aliases and a
# de-duplicated source, or the merge aborts with MULTIPLE_MATCHING_ROWS_ON_MERGE.
df_silver = df_silver.dropDuplicates(['date', 'currency'])

try:
    (DeltaTable.forName(spark, target_table)
     .alias("tgt")
     .merge(df_silver.alias("src"), "tgt.`date` = src.`date` AND tgt.`currency` = src.`currency`")
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

