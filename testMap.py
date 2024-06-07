from pyspark.sql import SparkSession
from pyspark.sql.functions import when
from decisiones import validar_gestion_map

mongo_conn = "mongodb://host.docker.internal:27017/findep"
mongo_db = "findep"

properties_local = {
    'user': 'orion',
    'password': 'orion',
    "driver": 'org.postgresql.Driver'
}

spark = SparkSession.builder.config("spark.driver.extraClassPath", "/opt/spark/postgresql-42.2.5.jar")\
    .config("spark.mongodb.read.connection.uri", mongo_conn) \
    .config("spark.mongodb.read.database", mongo_db) \
    .config("spark.mongodb.read.collection", "core_cliente") \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector:10.0.2") \
    .config("spark.mongodb.write.connection.uri", mongo_conn) \
    .config("spark.mongodb.write.database", mongo_db) \
    .config("spark.mongodb.write.collection", "core_map") \
    .getOrCreate()

spark.sparkContext.addPyFile('/opt/spark/decisiones.py')
df = spark.read.format("mongodb").load()

processed_rdd = df.rdd.map(lambda row: validar_gestion_map(row))
processed_df = processed_rdd.toDF()
processed_df.show(5)

dfR = processed_df.withColumn("tratamiento", when(processed_df["gestion"].isin(["C002", "C005", "C006", "C021", "C023", "C024", "C025", "C027", "C028", "C012", "C072", "C071", "C070", "C031", "C030", "C045", "C044", "C051"]), "COA+PRE").
                                             when(processed_df["gestion"].isin(["C032", "C037", "C036"]), "PRE+AGE").
                                             when(processed_df["gestion"].isin(["C062"]), "COA+AGE").
                                             when(processed_df["gestion"].isin(["C001", "C004", "C022", "C026", "C011", "C015", "C016", "C017", "C074", "C073", "C050"]), "PRE").
                                             when(processed_df["gestion"].isin(["C014", "C018", "C060", "C060", "C052", "C041", "C040", "C042"]), "COA").
                                             when(processed_df["gestion"].isin(["C048", "C061", "C038"]), "AGE").
                                             when(processed_df["gestion"].isin(["C089", "C095"]), "SIN CANAL").
                                             when(processed_df["gestion"].isin(["C035", "C034", "C033"]), "ASIG ASESOR PYME").
                                             otherwise(""))

dfR.select("id_contrato", "dias_vencido", "gestion", "tratamiento").write.format("mongodb").mode("overwrite").save()
spark.stop()

print('Proceso completado...')