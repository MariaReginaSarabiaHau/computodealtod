# **Reporte de Laboratorio 3.1: Working with Amazon S3**

- ### Introducción

Este laboratorio, el Lab 3.1, tuvo como objetivo principal utilizar Amazon Simple Storage Service (S3) no solo como almacenamiento, sino como una plataforma para alojar un sitio web estático. Mi meta era configurar el sitio de prueba de concepto, pero con un enfoque riguroso en la seguridad y las mejores prácticas de arquitectura. Esto implicó aprender a restringir el acceso al sitio web a un conjunto específico de direcciones IP mediante la aplicación de una Política de Bucket, un paso esencial antes de un despliegue público, y utilizar el SDK de Python (Boto3) y la AWS CLI para orquestar todo el proceso.

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

Este laboratorio demostró la flexibilidad y robustez de Amazon S3 no solo como un servicio de almacenamiento, sino como una plataforma de alojamiento web segura. Aprendí a pasar de una configuración de seguridad por defecto a una seguridad personalizada y estricta mediante la aplicación programática de Políticas de Bucket. La capacidad de utilizar la AWS CLI y el SDK de Python (Boto3) de manera integrada para la creación, configuración y despliegue me proporciona las herramientas necesarias para automatizar futuras tareas. El sitio web de prueba está ahora protegido y solo accesible para el equipo de trabajo, completando con éxito la fase inicial de desarrollo y arquitectura segura.

Al finalizar el módulo tengo una visión completa de cómo usar S3 como plataforma de contenido estático con controles finos de acceso. Comprendí la diferencia entre objetos, keys y prefijos; reforcé la instalación y uso de AWS CLI y Boto3; y publiqué un sitio que solo mi red autorizada puede ver, cumpliendo el objetivo del caso de la cafetería: compartir un avance privado con los dueños sin exponerlo públicamente. Este módulo me preparó para el siguiente paso: convertir el sitio en una aplicación dinámica conectándolo a APIs y autenticación gestionada, manteniendo las buenas prácticas de seguridad aprendidas aquí.
