from pyspark.sql import SparkSession

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
                            .config("spark.mongodb.read.collection", "orion_contrato") \
                            .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:10.2.2") \
                            .config("spark.mongodb.write.connection.uri", mongo_conn) \
                            .config("spark.mongodb.write.database", mongo_db) \
                            .config("spark.mongodb.write.collection", "core_cliente") \
                            .getOrCreate()

df_contratos = spark.read.jdbc(url = "jdbc:postgresql://host.docker.internal:5434/orion",
                               table = "orion_contrato",
                               properties = properties_local)

df_clientes = spark.read.jdbc(url = "jdbc:postgresql://host.docker.internal:5434/orion",
                              table = "orion_cliente",
                              properties = properties_local)

df_joined = df_contratos.join(df_clientes, df_contratos.id_contrato == df_clientes.cc_deudor, how='left')

df_final = df_joined.select(df_contratos.cc_contrato,
                            df_contratos.id_contrato,
                            df_clientes.cc_deudor,
                            df_clientes.cg_nombre,
                            df_clientes.cg_ap_paterno,
                            df_clientes.cg_ap_materno,
                            df_clientes.cg_rfc,
                            df_clientes.df_nacimiento,
                            df_clientes.telefono,
                            df_clientes.cg_calle,
                            df_clientes.cg_colonia,
                            df_clientes.cg_ciudad,
                            df_clientes.cg_entidad,
                            df_clientes.cg_municipio,
                            df_clientes.cg_entre_calles,
                            df_contratos.monto_pago,
                            df_contratos.total_contrato,
                            df_contratos.num_pago_vencido,
                            df_contratos.dias_vencido,
                            df_contratos.nivel_riesgo,
                            df_contratos.ilocalizables,
                            df_contratos.ilocalizable_sistema,
                            df_contratos.band_rpc,
                            df_contratos.calificacion_cliente,
                            df_contratos.maximo_retraso,
                            df_contratos.sucursal,
                            df_contratos.producto,
                            df_contratos.frecuencia_pago,
                            df_contratos.tipo_analisis).fillna('', subset=[
                                'cc_deudor',
                                'cg_nombre',
                                'cg_ap_paterno',
                                'cg_ap_materno',
                                'cg_rfc',
                                'df_nacimiento',
                                'telefono',
                                'cg_calle',
                                'cg_colonia',
                                'cg_ciudad',
                                'cg_entidad',
                                'cg_municipio',
                                'cg_entre_calles'
                            ])

df_final.write.format("mongodb").mode("overwrite").save()
spark.stop()

print('Proceso completado...')