import findspark
findspark.init()
from pyspark.sql import SparkSession
spark=SparkSession.builder.master("local").getOrCreate()
data = [("Alice", "F", 34), ("Bob", "M", 45), ("Catherine", "F", 23), ("David", "M", 40)]
columns = ["Name", "Gender", "Age"]
df = spark.createDataFrame(data, columns)
df.show()