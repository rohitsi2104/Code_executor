from pyspark.sql import SparkSession
spark = SparkSession.builder.appName('Test').getOrCreate()
spark.range(3).show()