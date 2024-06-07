from pyspark.sql import SparkSession
from concurrent.futures import ThreadPoolExecutor

properties_local = {
    'user': 'orion',
    'password': 'orion',
    'driver': 'org.postgresql.Driver'
}

def process_csv(properties):
    spark = SparkSession.builder.config("spark.driver.extraClassPath", "/opt/spark/postgresql-42.2.5.jar").getOrCreate()
    try:
        csv_reader = spark.read.options(header='True', inferSchema='True').csv("/opt/spark/contratosActualizados.csv") 
        csv_reader.write.jdbc(url = "jdbc:postgresql://host.docker.internal:5434/orion",
                              table = "orion_contrato",
                              mode = "overwrite",
                              properties = properties)
    except Exception as e:
        print("Error en procesamiento: ", e)
    finally:
        spark.stop()
        print('Proceso completado...')


if __name__ == "__main__":

    with ThreadPoolExecutor(max_workers = 2) as executor:
        executor.submit(process_csv, properties_local)


# Procesamiento en 50seg


