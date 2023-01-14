import pyspark

textFile = spark.read.text("README.md")
print(textFile)