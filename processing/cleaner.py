import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, regexp_replace, lower, lit, when, to_date, upper, initcap
from pyspark.sql.types import StringType

SOURCE_DIR = './sftp-downloads'
OUTPUT_DIR = './processed-data'

def clean_and_save():
    spark = SparkSession.builder.appName("CredableCleaner").getOrCreate()

    expected_schemas = {
        "FINDEXCountry-Series.csv": {"CountryCode", "SeriesCode", "DESCRIPTION"},
        "FINDEXData.csv": {"Country Name", "Country Code", "Indicator Name", "Indicator Code", "2011", "2014", "2017"},
        "FINDEXSeries.csv": {"Series Code", "Topic", "Indicator Name"},
        "FINDEXFootNote.csv": {"CountryCode", "SeriesCode", "Year", "DESCRIPTION"},
        "FINDEXCountry.csv": {"Country Code", "Short Name", "Region", "Income Group"},
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for filename in os.listdir(SOURCE_DIR):
        if filename.endswith('.csv'):
            filepath = os.path.join(SOURCE_DIR, filename)
            print(f"🧼 Processing {filename}")
            try:
                df = spark.read.csv(filepath, header=True, inferSchema=True)

                # Drop unnamed or empty columns
                df = df.select([c for c in df.columns if not c.lower().startswith("unnamed")])

                # Normalize column names to snake_case
                for old_name in df.columns:
                    new_name = old_name.strip().lower().replace(' ', '_').replace('-', '_')
                    df = df.withColumnRenamed(old_name, new_name)

                # Validate schema if defined
                required_cols = expected_schemas.get(filename)
                normalized_columns = {col.strip().lower().replace(' ', '_').replace('-', '_') for col in df.columns}
                normalized_required = {col.strip().lower().replace(' ', '_').replace('-', '_') for col in required_cols}
                if required_cols and not normalized_required.issubset(normalized_columns):
                    print(f"⚠️ Skipping {filename} — missing expected columns")
                    continue

                # File-specific logic
                if filename == "FINDEXCountry-Series.csv":
                    df = df.withColumn("countrycode", upper(col("countrycode")))
                    df = df.withColumn("seriescode", upper(col("seriescode")))
                    df = df.dropna(subset=["countrycode", "seriescode"])
                    df = df.withColumn("description", initcap(col("description")))

                elif filename == "FINDEXData.csv":
                    id_cols = ["country_name", "country_code", "indicator_name", "indicator_code"]
                    year_cols = [c for c in df.columns if c.isdigit()]
                    
                    # Wrap all column names with backticks
                    id_cols_quoted = [f"`{col}`" for col in id_cols]
                    exprs = [f"`{y}` as `{y}`" for y in year_cols]

                    df = df.selectExpr(*id_cols_quoted, *exprs)
                    df = df.na.drop(subset=year_cols)

                    stack_expr = ", ".join([f"'{y}', `{y}`" for y in year_cols])
                    df = df.selectExpr(
                        *id_cols_quoted,
                        f"stack({len(year_cols)}, {stack_expr}) as (year, value)"
                    )

                elif filename == "FINDEXSeries.csv":
                    df = df.fillna("N/A")
                    df = df.dropna(subset=["series_code", "indicator_name"])

                elif filename == "FINDEXFootNote.csv":
                    df = df.dropna(subset=["seriescode"])
                    df = df.withColumn("year", col("year").cast("int"))
                    df = df.withColumn("description", initcap(col("description")))

                elif filename == "FINDEXCountry.csv":
                    df = df.dropna(subset=["country_code", "region"])
                    df = df.fillna("N/A")

                # Fill general nulls
                df = df.fillna("N/A")

                output_path = os.path.join(OUTPUT_DIR, f"cleaned-{filename.replace('.csv', '')}")
                df.coalesce(1).write.option("header", True).mode("overwrite").csv(output_path)
                print(f"✅ Saved to {output_path}")

            except Exception as e:
                print(f"❌ Failed to process {filename}: {e}")

    spark.stop()

if __name__ == "__main__":
    clean_and_save()