from pyspark.sql.functions import col, explode, sequence
from pyspark.sql.types import DateType



def snapshot(df, col_names, start_date, end_date, value_col):
    col_names += [value_col]
    df = df.select(*col_names)
    col_names.pop()
    
    # Assuming the Spark session is already created and available as df.sparkSession
    spark = df.sparkSession
    date_range = spark.createDataFrame([(start_date, end_date)], ["start_date", "end_date"])
    date_range = date_range.withColumn("start_date", col("start_date").cast(DateType()))
    date_range = date_range.withColumn("end_date", col("end_date").cast(DateType()))
    date_range_df = date_range.select(explode(sequence(col("start_date"), col("end_date"))).alias("date_range"))

    # print('cross join of Date range....')
    date_range_df = date_range_df.join(df)
    date_range_df = date_range_df.fillna(0)

    # print("filtering data ....")
    date_range_df = date_range_df.filter(col("date_range") >= col(col_names[0]))

    # print("Grouping data........")
    drop_col = col_names.pop(0)
    col_names.insert(0, "date_range")
    date_range_df = date_range_df.groupBy(*col_names).sum(value_col)

    date_range_df = date_range_df.orderBy("date_range")
    date_range_df = date_range_df.withColumnRenamed("date_range", drop_col)
    date_range_df = date_range_df.withColumnRenamed(f"sum({value_col})", value_col)

    return date_range_df
