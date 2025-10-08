# **Reporte del Módulo 3: Developing Storage Solutions (Amazon S3)**

- ### Introducción

En este módulo me enfoqué en Amazon Simple Storage Service (Amazon S3) como base para desarrollar soluciones de almacenamiento en la nube. Revisé conceptos de objetos, buckets, seguridad, control de acceso, cifrado y buenas prácticas de publicación, y lo llevé a la práctica creando un sitio web estático para la cafetería del caso, controlando quién puede verlo a través de una política de bucket. Complementé la parte teórica con la AWS CLI, el SDK de Python (Boto3) y el IDE de VS Code sobre una instancia EC2, lo que me permitió moverme entre consola, línea de comandos y código como lo haría en un entorno profesional.

- ### AWS CLI: instalación, configuración y perfiles

Antes de trabajar con S3 repasé cómo instalar y verificar la AWS CLI v2 en Windows y macOS. El flujo es muy directo: descargar el instalador, aceptar licencia y luego confirmar con aws --version. Lo más importante vino después: configurar credenciales y región con aws configure. Aquí pegué el Access key ID y Secret access key de un usuario IAM creado con acceso programático y permisos mínimos (en mi caso, AmazonS3ReadOnlyAccess para validar), definí la región por defecto (us-east-1) y el formato de salida (JSON).
Aprendí a usar perfiles para alternar entre cuentas: con aws configure --profile <nombre> guardo otro par de credenciales, y luego añado --profile <nombre> a mis comandos. Esto es útil cuando debo probar permisos distintos (por ejemplo, uno con S3 y otro con EC2). Confirmé la configuración listando buckets con aws s3 ls y exploré la ayuda integrada (aws s3 ls help) para entender variaciones como listar objetos de un bucket específico usando la URI S3.

- ### Conceptos de Amazon S3 que me quedaron claros

Entendí que S3 es almacenamiento de objetos (no de bloques ni de archivos) con un diseño para 11 nueves de durabilidad. La unidad principal es el objeto, que combina datos y metadatos, y vive dentro de un bucket. El identificador clave de un objeto es su key, y tanto buckets como objetos se pueden referir por URL (endpoint regional + nombre del bucket + key).
Vi cinco casos de uso que conectan con escenarios reales: (1) distribución de contenido estático (documentos, imágenes, videos) de forma segura; (2) backup y archivo por su durabilidad; (3) data lake por su elasticidad y costo; (4) disaster recovery sin mantener un segundo sitio físico; y (5) hosting de sitios estáticos, que fue lo que implementé. También internalicé que los buckets son regionales (elijo región por latencia, costo y cumplimiento) y que la organización “tipo carpetas” se logra por prefijos en las keys, lo cual es clave para búsquedas y automatización (por ejemplo, filtrar por 2021/ventas/).

- ### Crear buckets: reglas y buenas prácticas

Cuando creé mi bucket por CLI confirmé las reglas de nomenclatura global (único a nivel mundial, 3–63 caracteres, minúsculas, números y guiones). Elegí la región desde el inicio porque luego no se puede cambiar. Prácticamente me quedo con tres ideas: (1) planear el nombre desde el principio; (2) seleccionar la región por cercanía a los usuarios/consumidores de datos y por requisitos regulatorios; (3) usar prefijos desde el día uno para evitar “cajones desordenados”.

- ### Seguridad en S3: cifrado, acceso y compartición controlada

En seguridad distinguí entre datos en tránsito y datos en reposo. En tránsito, lo normal es TLS 1.2+. En reposo, S3 soporta cifrado del lado del servidor: SSE-S3 (llaves manejadas por S3), SSE-KMS (llaves en AWS KMS, con auditoría y permisos más granulares) y SSE-C (llaves proporcionadas por el cliente). Entendí cuándo conviene cada opción: SSE-S3 para simplicidad, SSE-KMS para controles finos y registros, y SSE-C si por políticas debo gestionar llaves propias.
Para control de acceso revisé dos familias de políticas: basadas en identidad (adjuntas a usuarios, grupos y roles IAM) y basadas en recurso (adjuntas a buckets/objetos). Aquí entran las ACLs (muy puntuales para objetos “no propietarios” o escenarios legados) y la bucket policy, que usé para controlar desde qué dirección IP se podía ver el sitio. También aprendí a usar pre-signed URLs para compartir un objeto específico por tiempo limitado sin abrir el bucket, y CORS cuando un sitio en un dominio requiere cargar recursos alojados en S3 (especificando orígenes permitidos, métodos HTTP, etc.).

- ### Laboratorio 3.1 — Publicación del sitio estático y restricción por IP

Pasando a la práctica, me conecté al IDE de VS Code (sobre EC2), verifiqué AWS CLI v2, instalé Boto3 (sudo pip3 install boto3) y descargué los recursos del laboratorio.
Creación del bucket por CLI. Construí el nombre con mis iniciales, fecha y sufijo s3site y ejecuté:

> aws s3api create-bucket --bucket <mi-bucket> --region us-east-1


Luego en la consola confirmé la creación y revisé la sección Permisos. El laboratorio me pidió activar bloqueos de acceso público adecuados (dejando listo el bucket para que el acceso se gestione con bucket policy y no con ACLs abiertas).
Política de bucket con condición por IP. Creé el archivo website_security_policy.json para: (a) permitir GetObject solo desde mi IPv4 pública y (b) denegar el acceso a report.html salvo que sea mediante URL prefirmada (condición s3:authtype = REST-QUERY-STRING, que usaré en un laboratorio posterior). Apliqué la política con un script de Python/Boto3 (permissions.py) y validé que apareciera en la consola del bucket.
Carga del sitio. Subí el contenido del sitio (HTML, CSS, JS y JSON) con:


> aws s3 cp ../resources/website s3://<mi-bucket>/ --recursive --cache-control "max-age=0"


El --cache-control "max-age=0" fue útil para no pelearme con caché durante el desarrollo.
Pruebas de acceso. Copié la URL de objeto de index.html con el formato:

> https://<mi-bucket>.s3.amazonaws.com/index.html


Desde mi red autorizada, la página cargó correctamente (se ve la interfaz con menú, productos, etc.). Intenté abrir la misma URL desde otra conexión (por ejemplo, usando datos móviles o curl desde el IDE) y obtuve AccessDenied, tal como esperaba por la condición de IP. Esta validación me dejó claro que la política está efectivamente filtrando por origen.
Funcionalidad del sitio. Al presionar Login, apareció el mensaje “No API to call”. Esto es normal: más adelante integraré API Gateway y Cognito, pero por ahora el sitio solo consume archivos estáticos desde S3.

- ### Revisión del código del sitio (HTML, JS y datos)

Abrí index.html y ubiqué las referencias a CSS en el <head> y a scripts JS al final del <body>. Dos archivos clave son config.js y pastries.js.
En config.js hay un objeto window.COFFEE_CONFIG con claves como API_GW_BASE_URL_STR y COGNITO_LOGIN_BASE_URL_STR en null. Ese diseño me pareció acertado: cuando conecte API Gateway y Cognito, solo debo sobrescribir este archivo en S3 con valores reales, sin modificar el resto del código del sitio.
En pastries.js revisé la función loadAllItems. Si API_GW_BASE_URL_STR es null, la página lee all_products.json y muestra los productos de manera estática. Más abajo, printItems se encarga de renderizar el HTML. Este patrón me gustó porque separa capa de datos (hoy en JSON estático, mañana en un backend) de la capa de presentación, facilitando la migración futura a base de datos sin reescribir la UI.

- ### Reflexiones de seguridad y operación

De esta práctica me llevo varias lecciones. Primero, principio de mínimo privilegio: configuré credenciales IAM solo con lo necesario y me apoyé en bucket policy con condición de IP, sin abrir ACLs públicas indiscriminadamente. Segundo, estático no significa inseguro: un sitio en S3 puede y debe endurecerse (bloqueos de acceso público, políticas explícitas, CORS solo si es necesario y SSE-KMS si hay datos sensibles). Tercero, operación sencilla con CLI/SDK: aws s3 cp --recursive y unos cuantos comandos de Boto3 me permitieron montar, probar y ajustar permisos rápidamente. Finalmente, versionar y automatizar es el siguiente paso natural: integrar CodeCommit/CodePipeline para publicar cambios del sitio con pipelines reproducibles.

- ### Conclusión

Al finalizar el módulo tengo una visión completa de cómo usar S3 como plataforma de contenido estático con controles finos de acceso. Comprendí la diferencia entre objetos, keys y prefijos; reforcé la instalación y uso de AWS CLI y Boto3; y publiqué un sitio que solo mi red autorizada puede ver, cumpliendo el objetivo del caso de la cafetería: compartir un avance privado con los dueños sin exponerlo públicamente. Este módulo me preparó para el siguiente paso: convertir el sitio en una aplicación dinámica conectándolo a APIs y autenticación gestionada, manteniendo las buenas prácticas de seguridad aprendidas aquí.