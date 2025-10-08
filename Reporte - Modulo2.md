# **Reporte del Módulo 2: Introduction to Developing on AWS**

- ### Introducción

En este módulo trabajé con los conceptos y herramientas necesarias para comenzar a desarrollar en AWS. No solo repasé teoría (como el ciclo de vida del desarrollo de sistemas y las metodologías de trabajo), sino que también realicé actividades prácticas en AWS CloudShell y en un IDE de VS Code alojado en una instancia de Amazon EC2. A lo largo del módulo confirmé la importancia de equilibrar dos objetivos que a veces parecen opuestos: estabilidad operativa y desarrollo rápido de funciones. Mi objetivo fue entender cómo AWS ayuda a cerrar esa brecha y cómo usar su ecosistema (CLI, SDKs, IDEs y servicios) para construir, probar, desplegar y mantener aplicaciones de forma segura y escalable.

- ### Lo que entendí del SDLC y las metodologías
Aprendí que el Systems Development Life Cycle (SDLC) es el marco que organiza todo el proceso de creación de software en etapas: planificar, definir, diseñar, desarrollar, desplegar y mantener. Me quedó claro que, aunque el curso se centra en la etapa de desarrollo, las decisiones que tomamos ahí impactan directamente el despliegue y el mantenimiento. Por ejemplo, si adopto buenas prácticas de pruebas y control de versiones en “desarrollar”, reduzco el riesgo al “desplegar” y facilito la operación diaria en “mantener”.

También comparé dos enfoques: Waterfall y Agile. Waterfall me pareció útil cuando los requisitos están congelados, ya que progresa por fases secuenciales y hasta que no termina una, no pasa a la siguiente. Su desventaja es que el cliente ve resultados hasta muy tarde. Agile, en cambio, trabaja con iteraciones cortas (sprints de 1 a 4 semanas), lo que permite incorporar cambios y retroalimentación continua. Entendí por qué en la nube este enfoque es tan natural: la infraestructura y los servicios de AWS permiten iterar rápido, automatizar despliegues y medir el impacto casi en tiempo real.

En la práctica, desglosé la fase de desarrollo en codificar, compilar/build y probar. En “codificar” escribimos el código y lo versionamos (Git/AWS CodeCommit). En “build” generamos artefactos y pasamos chequeos de calidad (estilo, métricas). En “probar” distinguí varios niveles: unitarias (validan la lógica), integración (conexiones con BD o servicios), carga (simulan tráfico de usuarios para ver desempeño), UI (usabilidad y funcionamiento desde la vista del usuario) y penetración (seguridad frente a ataques). Me pareció clave que, aunque todo suene “técnico”, el objetivo es simple: entregar valor sin romper lo que ya funciona.

- ### Primeros pasos seguros en AWS: cuenta, IAM y entorno

Para poder trabajar, revisé el flujo recomendado: crear la cuenta de AWS, evitar usar el usuario root (solo para tareas estrictamente necesarias) y, en su lugar, crear usuarios IAM con permisos mínimos. Comprendí la diferencia entre usuarios, grupos y roles. Un usuario puede pertenecer a un grupo (por ejemplo, “Developers”) y heredar las políticas del grupo; además, puede asumir un rol con permisos específicos para una tarea. Esta separación me pareció muy práctica porque reduce errores de configuración y estandariza permisos.

Después, instalé y configuré el entorno de desarrollo: AWS CLI y el SDK del lenguaje que utilicé (Boto3 para Python). Me quedo con la idea de que en AWS se puede interactuar por cuatro vías equivalentes en el fondo: Consola, CLI, SDKs o APIs. Todas terminan llamando a un endpoint y devolviendo un código HTTP que debo manejar (por ejemplo, 4xx para errores del cliente y 5xx para errores del servicio, que normalmente se resuelven con reintentos y exponential backoff).

- ### Práctica 1: Exploración de AWS CloudShell

Abrí AWS CloudShell desde la consola. Me gustó que ya viene autenticado y con AWS CLI 2.x instalado. Verifiqué la versión con aws --version y listé buckets con aws s3 ls. Luego subí y ejecuté un script de Python, list-buckets.py, que usa Boto3 para listar los buckets desde código. Me pareció interesante comparar los dos enfoques: con un comando (aws s3 ls) y con un script (SDK). Ambos lograron lo mismo, pero el script me da la base para integrar esa lógica en una aplicación real.

Como ejercicio de I/O, copié el archivo desde CloudShell a un bucket de S3 con aws s3 cp list-buckets.py s3://<mi-bucket>. Con esto confirmé que CloudShell no solo sirve para “probar cosas rápidas”, sino que también puede integrarse en un flujo de trabajo real (por ejemplo, lanzar scripts de mantenimiento o automatización). Además, entendí la limitación de 1 GB de almacenamiento persistente por región en $HOME, suficiente para utilidades, pero no para datos grandes (ahí conviene S3).

- ### Práctica 2: IDE de VS Code en EC2 y publicación de “Hello World” en S3

Después ingresé al IDE de VS Code (servido por una instancia EC2). Reconocí la interfaz: panel de archivos a la izquierda, editor al centro y terminal Bash abajo. Lo primero fue traer mi archivo list-buckets.py desde S3 al entorno local con aws s3 cp s3://<bucket>/list-buckets.py .. Al ejecutar python3 list-buckets.py apareció el error ModuleNotFoundError: No module named 'boto3'. Esto me sirvió para comprobar que, aunque Python venía instalado, el SDK no. La solución fue instalarlo con sudo pip3 install boto3. Reejecuté el script y funcionó, mostrando el nombre del bucket.
Este fallo-controlado me ayudó a afianzar dos hábitos: leer el error con calma y documentar el paso que lo corrige (en este caso, dependencia faltante).

Luego creé un index.html sencillo con el mensaje Hello World. y lo subí a S3 usando aws s3 cp index.html s3://<mi-bucket>/index.html. Con esto comprobé un caso básico de hosting estático en S3 (para verlo públicamente, sé que debo revisar propiedad del objeto, bloqueos de acceso público y ACLs/políticas). El apéndice traía un script s3-permissions.py que automatiza tres cosas: propiedad del bucket (BucketOwnerPreferred), desbloqueo de accesos públicos y ACL pública de solo lectura para el objeto index.html. Aunque no siempre se recomienda abrir contenido de forma pública, en un entorno de laboratorio es útil para validar que el archivo realmente se puede consumir desde la web.

Comparando con CloudShell, VS Code me ofreció una experiencia más completa para editar y depurar, mientras que CloudShell me dio acceso rápido y autenticado a la CLI sin levantar infraestructura adicional. Concluí que ambos se complementan: CloudShell para scripts y operaciones rápidas; VS Code/EC2 para desarrollo con editor gráfico, extensiones y control más fino del entorno.

- ### AWS Cloud9 y Amazon CodeWhisperer: productividad y colaboración

Aunque en el laboratorio usé VS Code, también revisé AWS Cloud9, un IDE totalmente en el navegador que se integra con servicios como Lambda y CodeCommit. Su ventaja principal es que evita instalaciones locales y facilita la colaboración en tiempo real.
También conocí Amazon CodeWhisperer, que es un asistente de IA dentro del IDE para generar sugerencias de código con base en comentarios y contexto. Me pareció útil para acelerar tareas repetitivas, proponer unit tests, y, sobre todo, por su scanner de seguridad que analiza vulnerabilidades comunes. Aprendí que existe una capa Individual (gratis con AWS Builder ID) y una Professional (con administración y políticas a nivel organización). En resumen, estas herramientas apuntan a que el tiempo de desarrollo se enfoque en la lógica crítica del negocio y no en “plomería” del código.

- ### Manejo de regiones, endpoints y errores con los SDKs

Otro aprendizaje técnico importante fue cómo los SDKs resuelven la región (por ejemplo, variables de entorno, archivos de configuración o metadatos si corro en EC2). Entendí el modelo de request–response: mi aplicación hace una solicitud a un endpoint y recibe una respuesta con datos o con un error estandarizado (códigos HTTP 2xx, 4xx, 5xx). Practiqué mentalmente cómo reaccionar ante 4xx (corregir mi solicitud, credenciales, permisos IAM, parámetros) y 5xx (reintentar con exponential backoff). Esta parte me dejó más preparada para diagnosticar problemas reales.

- ### Conclusiones y aprendizajes personales

Al terminar el módulo siento que avancé en tres frentes: proceso, herramientas y buenas prácticas. En proceso, el SDLC me dio un mapa claro para no perder de vista el objetivo: construir software útil sin sacrificar estabilidad. En herramientas, ya sé moverme entre Consola, CLI, SDKs y IDEs de AWS, eligiendo el camino adecuado según la tarea. Y en buenas prácticas, reforcé la importancia de IAM (usuarios, grupos, roles y políticas de mínimo privilegio), del versionamiento y de las pruebas en múltiples niveles.

En lo práctico, pude listar buckets desde CLI y desde Python, diagnostiqué y corregí un error de dependencias en VS Code, y publiqué un “Hello World” en S3 entendiendo los permisos implicados. Me quedo con la idea de que la nube facilita experimentar y repetir rápido, pero que esa velocidad solo aporta si la acompaño con disciplina: configurar bien permisos, registrar pasos, automatizar lo repetitivo y medir el impacto de los cambios. Este módulo me deja lista para avanzar al siguiente, ya con un entorno funcional y un flujo de trabajo más profesional.