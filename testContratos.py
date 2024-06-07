from pyspark.sql import SparkSession

properties_local = {
    'user': 'orion',
    'password': 'orion',
    "driver": 'org.postgresql.Driver'
}

spark = SparkSession.builder.config("spark.dri ver.extraClassPath", "/opt/spark/postgresql-42.2.5.jar").getOrCreate()

try:
    csv_reader = spark.read.options(header='True', inferSchema='True').csv("/opt/spark/contratosActualizados.csv") 
    csv_reader.write.jdbc( url = "jdbc:postgresql://host.docker.internal:5434/orion",
                           table = "orion_contrato",
                           mode = "overwrite",
                           properties = properties_local)
except Exception as e:
    print("Error en procesamiento: ", e)
finally:
    spark.stop()
    print('Proceso completado...')

# Procesamiento en 1.05seg