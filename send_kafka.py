import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import when, col, concat, lit
import argparse
import os

config = os.getenv("APP_SETTINGS_MODULE")
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.mongodb.spark:mongo-spark-connector:10.0.2 pyspark-shell'
mongo_conn = "mongodb://host.docker.internal:27017/findep"
mongo_db = "findep"
parser = argparse.ArgumentParser()
parser.add_argument('tratamiento', type=str, help='Tratamiento')
parser.add_argument('topic', type=str, help='Tratamiento')
arg = parser.parse_args()
trata_ajustar = arg.tratamiento
topic = arg.topic
myspark = SparkSession.builder\
	.config("spark.mongodb.read.connection.uri", "mongodb://host.docker.internal:27017/findep.segmentados_core") \
    .config("spark.jars.packages","org.mongodb.spark:mongo-spark-connector:10.0.2") \
	.getOrCreate()
df = myspark.read.format("mongodb").load()
df_result = df.filter(df['tratamiento']==trata_ajustar)
df_result = df_result.withColumn("value", concat(lit('{ "id_contrato":'),col('id_contrato')\
            ,lit(', "tratamiento": "'),col('tratamiento'),lit('"}')))
query = df_result \
    .selectExpr("CAST(id_contrato AS STRING) as key","CAST(value AS STRING)") \
    .write \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "host.docker.internal:9092") \
    .option("topic", topic) \
    .option("checkpointLocation", "/opt/spark") \
    .partitionBy("id_contrato") \
    .mode("append") \
    .save()

myspark.sparkContext._gateway.close()
myspark.stop()
