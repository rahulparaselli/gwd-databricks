# Databricks notebook source
# DBTITLE 1,Configuration
from pyspark.sql import functions as F

CATALOG = "gwd_de"
source_table = f"{CATALOG}.bronze.invoices"
target_table = f"{CATALOG}.silver.invoices"

# COMMAND ----------

# DBTITLE 1,Read and Transform
df_bronze = spark.table(source_table)

df_silver = df_bronze.select(
    F.col("invoice_id"),
    F.col("customer_id"),
    F.to_date(F.col("invoice_date"), "yyyy/M/d").alias("invoice_date"),
    F.col("invoice_month"),
    F.upper(F.col("currency")).alias("currency"),
    F.initcap(F.col("region")).alias("region"),
    F.initcap(F.col("invoice_status")).alias("invoice_status")
)

# COMMAND ----------

# DBTITLE 1,Write (upsert)
from delta.tables import DeltaTable

# Bronze re-lands whole files, so MERGE keeps silver current without
# dropping history or rewriting the table. Delta needs BOTH aliases and a
# de-duplicated source, or the merge aborts with MULTIPLE_MATCHING_ROWS_ON_MERGE.
df_silver = df_silver.dropDuplicates(['invoice_id'])


# Self-heal: MERGE only updates duplicate target rows, never removes them.
# Collapse historical duplicates once per run before merging (no-op when
# already clean); skipped on first run where merge creates the table itself.
self_healed = 0
try:
    dup_ids = [
        r["invoice_id"]
        for r in spark.table(target_table)
            .groupBy("invoice_id").count()
            .filter(F.col("count") > 1)
            .collect()
    ]
except Exception as exc:
    if "TABLE_OR_VIEW_NOT_FOUND" not in str(exc).upper():
        raise
    dup_ids = []

if dup_ids:
    spark.sql(
        "DELETE FROM " + target_table + " WHERE invoice_id IN ("
        + ", ".join(repr(i) for i in dup_ids) + ")"
    )
    self_healed = len(dup_ids)

try:
    (DeltaTable.forName(spark, target_table)
     .alias("tgt")
     .merge(df_silver.alias("src"), "tgt.`invoice_id` = src.`invoice_id`")
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
msg = f"{target_table}: {how}, {rows} rows" + (" (self-healed %d duplicate keys)" % self_healed if self_healed else "")
print(msg)
dbutils.notebook.exit(msg)

