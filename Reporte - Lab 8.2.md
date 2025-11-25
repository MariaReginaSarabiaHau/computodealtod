# Reporte del Laboratorio 8.2: Implementación de Contenedores en Servicios Administrados

En este laboratorio trabajé en llevar la aplicación de proveedores de café a una arquitectura mucho más administrada, reduciendo la carga operativa y aprovechando servicios de AWS que permiten escalar sin tanta intervención manual. A diferencia del laboratorio anterior, donde yo contenicé manualmente la aplicación y la base de datos, aquí el enfoque fue migrarla hacia servicios gestionados: Aurora Serverless para la base de datos y Elastic Beanstalk para la capa web. Con esto, practiqué un flujo más cercano al que se utiliza en implementaciones reales en la nube.

- ### Tarea 1 

> En la Tarea 1 preparé el entorno de trabajo en el IDE de VS Code, igual que en laboratorios previos, pero esta vez el script de inicialización (setup.sh) reconstruyó el trabajo de laboratorios anteriores de forma automática. Configuró el bucket S3, la tabla en DynamoDB, la API en API Gateway y volvió a enviar la imagen Docker al repositorio de Amazon ECR. También verifiqué que la CLI de AWS estuviera instalada en su versión más reciente y confirmé que boto3 estuviera disponible. Por último, validé que el sitio web de la cafetería funcionara desde S3, lo cual me sirvió de base para la integración que haría más adelante con API Gateway.

- ### Tarea 2

> En la Tarea 2 configuré la parte de red para que tanto Aurora Serverless como Elastic Beanstalk pudieran funcionar correctamente. Revisé la VPC generada por el laboratorio, identifiqué la subred existente y luego creé una segunda subred en otra zona de disponibilidad. Esto fue importante porque tanto RDS como Beanstalk requieren más de una subred para trabajar con mayor disponibilidad. Después habilité la asignación automática de IP pública para esa nueva subred y ajusté su tabla de rutas para asegurar que tuviera salida a Internet mediante el internet gateway. Guardé todos esos IDs porque más adelante los usé en la configuración de Beanstalk.

- ### Tarea 3

> En la Tarea 3 configuré la nueva base de datos Aurora Serverless v2, que sustituye al contenedor MySQL que usé en el laboratorio anterior. Seleccioné el motor compatible con MySQL, definí el clúster como "supplierdb", establecí la contraseña del usuario admin y asigné las subredes creadas en la tarea previa. También habilité la API de datos de RDS, desactivé opciones de monitoreo que no necesitaba y creé la base de datos inicial llamada suppliers. Una vez desplegado, obtuve el endpoint del clúster y el ID del grupo de seguridad para usarlo en pasos posteriores cuando conectara la aplicación desde el contenedor y desde Beanstalk.

- ### Tarea 4

> En la Tarea 4 revisé la imagen Docker que previamente había subido a Amazon ECR. Usando tanto la consola como la CLI confirmé el repositorio, el URI, las etiquetas y los detalles de la imagen. Esta revisión fue importante porque más adelante esa misma imagen sería utilizada por Elastic Beanstalk para iniciar el contenedor que ejecuta la aplicación de proveedores de café.
 
 - ### Tarea 5

> En la Tarea 5 probé la comunicación entre el contenedor y la nueva base de datos Aurora Serverless directamente desde el IDE. Inicié un nuevo contenedor de la aplicación, pero esta vez pasándole el endpoint de Aurora como valor de APP_DB_HOST. Abrí el puerto 8000 en el grupo de seguridad para visualizar la aplicación, y agregué también una regla para permitir que el IDE pudiera comunicarse con el puerto 3306 de Aurora. Aunque la aplicación cargó, al intentar ver la lista de proveedores apareció un error, lo que indicaba que Aurora aún no tenía creados los objetos de base de datos necesarios.

- ### Tarea 6

> En la Tarea 6 me conecté al Editor de Consultas de Amazon RDS con el usuario admin para crear todos los objetos que la aplicación requiere: el usuario nodeapp, la base de datos COFFEE, los permisos necesarios y la tabla suppliers. Probé que la tabla estuviera vacía y luego volví a la aplicación web para confirmar que la conexión ya funcionaba correctamente. Desde ahí pude agregar un proveedor nuevo y verificar en el editor de consultas que el registro sí aparecía en la tabla de Aurora.

- ### Tarea 7
> En la Tarea 7 cargué los datos reales del proveedor utilizando el archivo coffee_db_dump.sql. Me conecté a Aurora con mysql desde el terminal, confirmé que estaba en la base COFFEE y ejecuté el comando source para cargar todo el dump. Revisé las tablas suppliers y beans, verificando que el inventario completo estuviera ahí. Al actualizar la aplicación web vi reflejados todos los proveedores reales, lo que indicaba que la base de datos ya estaba correctamente poblada.
- ### Tarea 8

> En la Tarea 8 revisé la política IAM y el rol que Elastic Beanstalk utilizaría para descargar la imagen desde ECR. Exploré la política aws-elasticbeanstalk-ec2-instance-policy, que concede permisos como ecr:GetAuthorizationToken y ecr:BatchGetImage, y también verifiqué el rol aws-elasticbeanstalk-ec2-role que sería asignado a la instancia EC2 creada por Beanstalk. Este paso era crítico porque sin esos permisos la instancia no habría podido extraer la imagen para lanzar el contenedor.
- ### Tarea 9
> En la Tarea 9 comencé la implementación de Elastic Beanstalk. Primero creé la aplicación MyNodeApp, preparé el archivo options.txt con los IDs de subred, VPC, grupo de seguridad y endpoint de Aurora. Después identifiqué la solución "Amazon Linux 2 running Docker" y con eso creé el entorno MyEnv. Una vez desplegado, probé la aplicación de muestra que Beanstalk genera por defecto. Luego preparé el archivo Dockerrun.aws.json para indicarle a Beanstalk que debía utilizar mi propia imagen de ECR. Subí la nueva versión, esperé a que se desplegara y finalmente pude ver mi aplicación de proveedores corriendo directamente en Elastic Beanstalk, con acceso completo a la base de datos Aurora. Probé /suppliers, /beans y /beans.json, y todo funcionó correctamente.
- ### Tarea 10
> En la Tarea 10 completé la integración final agregando un recurso bean_products en API Gateway. Configuré un método GET que apuntaba directamente al endpoint de Elastic Beanstalk que devolvía los datos de los granos en formato JSON. Habilité CORS, probé el método y lo desplegué en la etapa prod. Finalmente regresé al sitio web de la cafetería en S3 y confirmé que la sección “Buy Coffee” ya mostraba la información del inventario real gracias al nuevo proxy configurado en API Gateway.

Al finalizar el laboratorio, pude ver cómo toda la arquitectura funcionaba de manera integrada: la aplicación en Elastic Beanstalk, la base de datos en Aurora Serverless, la imagen en ECR y la exposición final de datos hacia el sitio web mediante API Gateway. Además, entendí por qué una base de datos en contenedor no es ideal y por qué Aurora ofrece mejores capacidades de escalabilidad y administración. En general, este laboratorio me permitió ver una implementación más realista y administrada de toda la solución.

- ### Conclusión 
En conclusión, este laboratorio me ayudó a dar un paso más allá de la simple ejecución de contenedores para entender cómo se ve una arquitectura más madura en la nube usando servicios administrados. Por un lado, migré la base de datos a Aurora Serverless, lo que elimina mucha carga operativa y permite escalar de forma automática según la demanda. Por otro lado, desplegué la aplicación de proveedores de café en Elastic Beanstalk utilizando una imagen almacenada en ECR, integrando todo con API Gateway y el sitio estático de la cafetería en S3. Al final, pude ver cómo cada servicio encaja como pieza de un mismo sistema: contenedores, base de datos administrada, balanceo de carga, API y front-end, trabajando juntos para ofrecer una solución más flexible, escalable y fácil de mantener para la cafetería.