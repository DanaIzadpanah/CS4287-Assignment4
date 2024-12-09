from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when

# Path to the MongoDB data (or demonstration CSV for the demo)
SPARK_INPUT_PATH = "../data/mongo_data/mongo_entries.json"
SPARK_OUTPUT_PATH = "../data/spark_output/error_counts_per_producer.csv"

def main():
    # Initialize Spark session
    spark = SparkSession.builder \
        .appName("ErrorCountPerProducer") \
        .getOrCreate()

    # Read data from the demonstration input file
    print(f"Reading data from {SPARK_INPUT_PATH}...")
    df = spark.read.json(SPARK_INPUT_PATH)

    # Add a column to indicate whether an error occurred
    df = df.withColumn("is_wrong", when(col("GroundTruth") != col("Inferred"), 1).otherwise(0))

    # Group by ProducerID and sum up the errors
    error_count_df = df.groupBy("ProducerID").sum("is_wrong").withColumnRenamed("sum(is_wrong)", "total_errors")

    # Show the results
    print("Error counts per producer:")
    error_count_df.show()

    # Write the output to a CSV file
    print(f"Writing results to {SPARK_OUTPUT_PATH}...")
    error_count_df.coalesce(1).write.csv(SPARK_OUTPUT_PATH, header=True)

if __name__ == "__main__":
    main()