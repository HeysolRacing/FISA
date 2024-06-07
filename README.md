# Demo Orion
En esta documentación, aprenderás cómo ejecutar un Docker Compose para configurar el entorno de Spark y cómo ejecutar distintos comandos de Spark en ese entorno para simular el proceso de Orion, desde la ingesta de datos hasta el envío de datos a los diferentes tópicos de Kafka.

## Pre-requisitos 📋
Antes de comenzar, asegúrate de tener instalados los siguientes requisitos:
- Docker: [Guía de instalación de Docker](https://docs.docker.com/get-docker/)
- Docker Compose: [Guía de instalación de Docker Compose](https://docs.docker.com/compose/install/)

### Paso 1: Ejecutar Docker Compose
1. Abre una terminal y navega hasta el directorio donde se encuentra tu archivo docker-compose.yml.
2. Ejecuta el siguiente comando para iniciar los contenedores de Docker:

```bash
docker-compose up -d
```

Esto iniciará los contenedores necesarios para ejecutar Spark, Kafka, PostgreSQL y MongoDB.

3. Verifica que los contenedores estén en ejecución utilizando el siguiente comando:

```bash
docker-compose ps
```

Deberías ver una lista de los contenedores y su estado.

### Paso 2: Conectar a la base de datos PostgreSQL y carga de csv
Una vez que los contenedores estén en ejecución, puedes conectar a la base de datos PostgreSQL utilizando los siguientes datos de conexión:
- Host: localhost
- Port: 5434
- Database: orion
- Nombre de usuario: orion
- Contraseña: orion
  
Puedes utilizar estos datos de conexión en tu aplicación de Spark o en cualquier otra herramienta de gestión de bases de datos PostgreSQL para acceder a la base de datos ***orion***.

Para cargar un archivo CSV en la base de datos PostgreSQL, sigue los siguientes pasos:

1. Primero deberas crear las tablas en la base de datos, para eso puedes abrir el gestor de base de datos que prefieras y ejecutar el script ***schema.sql*** que se encuentra en el directorio.

2. Luego, puedes cargar el archivo CSV que se encuentra en el directorio como ***clientes_millon.csv*** donde se encuentran los datos de los clientes.

3. Verifica que los datos se hayan cargado correctamente ejecutando la siguiente consulta:

```sql
select * from orion_contrato order by id_contrato asc;
select count(*) as "Total Contratos" from orion_contrato; 
select * from orion_cliente order by cc_deudor asc;
select count(*) as "Total clientes" from orion_cliente;  
```

### Paso 3: Conectar a la base de datos MongoDB
Después de conectarte a la base de datos PostgreSQL, puedes conectar a la base de datos MongoDB utilizando los siguientes datos de conexión:

- Host: localhost
- Port: 27017
- Database: findep

Puedes utilizar estos datos de conexión en tu aplicación de Spark o en cualquier otra herramienta de gestión de bases de datos MongoDB para acceder a la base de datos findep.

### Paso 4: Configurar kafka
Para configurar kafka, deberas ejecutar los siguientes comandos:
1. Abre una terminal y verifica que el contenedor de kafka esté en ejecución utilizando el siguiente comando:

```bash
docker-compose ps
```

2. Ejecuta el siguiente comando para conectarte al contenedor de kafka:
   
```bash
docker exec -it <CONTAINER ID> bash
```
El ***CONTAINER ID*** sera el id del contenedor de kafka que se encuentra en ejecución.
Ejemplo: ***docker exec -it 0f0b7b0b0b0b bash***

3. Una vez conectado al contenedor de kafka, navega hasta el directorio ***/opt/bitnami/kafka/bin*** utilizando el siguiente comando:

```bash
cd /opt/bitnami/kafka/bin
```

4. Ejecuta los siguientes comandos para crear los topicos ***pre*** y ***coa***:

```bash
kafka-topics.sh --create --bootstrap-server host.docker.internal:9092 --topic pre
kafka-topics.sh --create --bootstrap-server host.docker.internal:9092 --topic coa
```

5. Verifica que los topicos se hayan creado correctamente ejecutando el siguiente comando:

```bash
kafka-topics.sh --list --bootstrap-server host.docker.internal:9092
```

6. Activa el consumidor de kafka para el topico ***coa*** ejecutando el siguiente comando:

```bash
kafka-console-consumer.sh --topic coa --bootstrap-server host.docker.internal:9092
```

### Paso 5: Ejecutar los procesos de Spark
Para ejecutar los procesos de Spark, deberas ejecutar los siguientes comandos:

1. Abre una terminal y verifica que el contenedor de Spark esté en ejecución utilizando el siguiente comando:

```bash
docker-compose ps
```

2. Ejecuta el siguiente comando para conectarte al contenedor de Spark:
   
```bash
docker exec -it <CONTAINER ID> bash
```
El ***CONTAINER ID*** sera el id del contenedor de kafka que se encuentra en ejecución.
Ejemplo: ***docker exec -it 0f0b7b0b0b0b bash***

3. Una vez conectado al contenedor de Spark, navega hasta el directorio ***/opt/bitnami/spark/bin*** utilizando el siguiente comando:

```bash
cd /opt/bitnami/spark/bin
```

4. Ejecuta el proceso de carga del universo de ***contratos*** en la base de datos PostgreSQL:

```bash - 53 seg
./spark-submit --jars /opt/spark/postgresql-42.2.5.jar --master spark://host.docker.internal:7077 /opt/spark/testContratos.py 
```

5. Ejecutar proceso que realiza el merge entre los contratos con su respectiva informacion de cliente, para luego escribirlos en la base de datos de MongoDB:

```bash - 2:10 min
./spark-submit --jars /opt/spark/postgresql-42.2.5.jar --packages org.mongodb.spark:mongo-spark-connector:10.0.2 --master spark://host.docker.internal:7077 /opt/spark/testClientes.py
```

6. Ejecutar el proceso que realiza la segmentacion de todos los contratos que se encuentran en la base de datos de MongoDB cargados previamente en la coleccion ***core_clientes***:

```bash 1.30 m
./spark-submit --packages org.mongodb.spark:mongo-spark-connector:10.0.2 --master spark://host.docker.internal:7077 /opt/spark/testMap.py
```

### Paso 6: Enviar contratos segmentados hacia el topico de kafka ***coa***

Para enviar los contratos con el tratamiento ***COA+PRE*** hacia el topico de kafka ***coa***, deberas ejecutar los siguientes comandos:

1. En el mismo contenedor de spark ejecuta el siguiente comando para realizar el envio de los contratos hacia el topico de kafka:

```bash
./spark-submit --packages org.mongodb.spark:mongo-spark-connector:10.0.2,org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.1 --master spark://host.docker.internal:7077 /opt/spark/send_kafka_up.py COA+PRE coa
```
2. Verifica que los contratos se hayan enviado correctamente ubicate en el contenedor de kafka.
3. Desde el contenedor de kafka, termina el proceso de consumo del topico ***coa*** con la combinacion de teclas ***Ctrl+C***.:

### Paso 7: Enviar contratos segmentados hacia el topico de kafka ***pre***

1. Desde el contenedor de kafka, activa el consumidor de kafka para el topico ***pre*** ejecutando el siguiente comando:

```bash
kafka-console-consumer.sh --topic pre --bootstrap-server host.docker.internal:9092
```
2. Muevete al contenedor de spark y ejecuta el siguiente comando para realizar el envio de los contratos hacia el topico ***pre*** de kafka:

```bash
./spark-submit --packages org.mongodb.spark:mongo-spark-connector:10.0.2,org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.1 --master spark://host.docker.internal:7077 /opt/spark/send_kafka.py PRE pre
```
3. Verifica que los contratos se hayan enviado correctamente ubicate en el contenedor de kafka.

4. Desde el contenedor de kafka, termina el proceso de consumo del topico ***pre*** con la combinacion de teclas ***Ctrl+C***.:

### Paso 8: Detener los contenedores
Después de finalizar tus tareas con Spark, PostgreSQL, MongoDB y Kafka, es importante detener los contenedores de Docker para liberar recursos del sistema.

1. En la terminal donde ejecutaste el comando docker-compose up -d, ejecuta el siguiente comando para detener los contenedores:

```bash
docker-compose down
```
Esto detendrá y eliminará los contenedores y las redes creadas por Docker Compose.
¡Ahora estás listo para ejecutar la configuración de Kafka y los comandos de Spark en tu entorno Docker Compose!

### Nota :
- Podras ir monitoreando el estado de los procesos de spark en la siguiente url: http://localhost:8080/
- Al ejecutar los procesos de spark, una vez finalizados se debera terminar el proceso de spark con la combinacion de teclas ***Ctrl+C*** para volver a ejecutar otro proceso de spark.