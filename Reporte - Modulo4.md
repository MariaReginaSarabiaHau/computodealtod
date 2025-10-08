# **Reporte del Módulo 4: Securing Access to Cloud Resources**

- ### Introducción

En este módulo aprendí a manejar la seguridad dentro de la nube de AWS, entendiendo cómo proteger los recursos y controlar quién puede acceder a ellos. Me quedó claro que la seguridad no depende únicamente de AWS, sino que también es mi responsabilidad configurar correctamente los permisos, roles y políticas. Aquí fue donde conocí a fondo el servicio AWS Identity and Access Management (IAM), que sirve para crear usuarios, grupos y roles con permisos específicos, asegurando que cada persona o sistema solo pueda acceder a lo que realmente necesita. Todo el contenido me ayudó a comprender cómo la autenticación, la autorización y las políticas bien definidas son fundamentales para mantener un entorno en la nube seguro y organizado.

- ### Modelo de responsabilidad compartida

Uno de los primeros temas fue el Shared Responsibility Model, que establece una división clara entre las responsabilidades de AWS y las del usuario o cliente. AWS se encarga de la seguridad de la nube, es decir, de toda la infraestructura física: los centros de datos, el hardware, la red y los servidores donde se ejecutan los servicios. En cambio, nosotros, como usuarios, somos responsables de la seguridad en la nube, lo que incluye la configuración de los accesos, la administración de datos, la creación de políticas IAM y la protección de la información sensible.

Por ejemplo, si creo un bucket en Amazon S3, AWS garantiza que los servidores estén protegidos, pero yo debo definir los permisos, activar el cifrado y configurar los accesos correctos. Lo mismo ocurre con una instancia de EC2 o una base de datos en RDS: AWS mantiene el hardware, pero yo debo actualizar el sistema operativo, aplicar parches de seguridad y administrar los grupos de seguridad. En resumen, comprendí que la nube no elimina mi responsabilidad en la seguridad, sino que la transforma: AWS protege la infraestructura, pero yo debo proteger el uso que hago de ella.

- ### Comprendiendo IAM (Identity and Access Management)

Después de entender la parte teórica de la seguridad, me enfoqué en IAM, que es el servicio que permite controlar el acceso dentro de AWS. Lo interesante de IAM es que se basa en dos conceptos principales: autenticación (comprobar quién eres) y autorización (determinar qué puedes hacer). En IAM, los usuarios no tienen acceso a nada hasta que se les asignan permisos de forma explícita.

Aprendí que existen diferentes tipos de entidades:

    - Usuarios IAM: representan a personas o aplicaciones que acceden a la cuenta con credenciales fijas.

    - Grupos IAM: agrupan usuarios que comparten los mismos permisos.

    - Roles IAM: se usan para accesos temporales, muy útiles para servicios o conexiones entre cuentas.

    - Políticas IAM: son documentos JSON donde se especifican los permisos con comandos como “Allow” o “Deny”.

Gracias a esto entendí el principio del mínimo privilegio, que consiste en dar únicamente los permisos necesarios para una tarea, evitando accesos innecesarios que puedan generar riesgos.

- ### Autenticación y seguridad con MFA

Otro tema importante fue la autenticación, donde aprendí los distintos métodos que AWS utiliza para confirmar la identidad de los usuarios. Por ejemplo, cuando entro a la consola, uso mi usuario y contraseña; pero si necesito acceder desde la terminal o desde un programa, uso un par de llaves llamadas Access Key ID y Secret Access Key.

También conocí la autenticación multifactor (MFA), que agrega una capa adicional de seguridad. MFA pide un segundo factor, como un código en una app del teléfono o un dispositivo físico, además de la contraseña. Esto evita que alguien acceda a la cuenta incluso si logra obtener la contraseña.
AWS también cuenta con el Security Token Service (STS), que genera credenciales temporales y seguras. Estas se usan junto con roles IAM para que aplicaciones o usuarios puedan acceder temporalmente a recursos sin tener que almacenar llaves fijas. Esto me pareció muy práctico, sobre todo pensando en la seguridad de proyectos grandes o colaborativos.

- ### Autorización con IAM y acceso cruzado entre cuentas

El módulo también profundizó en la autorización, que es el proceso de determinar qué acciones puede realizar cada identidad. Aquí fue donde trabajé con roles y políticas para dar acceso controlado a recursos específicos.
Uno de los ejemplos más interesantes fue la demostración de acceso cruzado entre cuentas. En ese caso, se configuró una cuenta de producción y una de desarrollo. En la de producción, se creó un bucket S3 y un rol con una política que solo permitía acceso a ese bucket. Luego, en la cuenta de desarrollo, se configuró un usuario con permisos para “asumir” ese rol mediante el servicio STS. Al probarlo, el usuario de la cuenta de desarrollo pudo acceder al bucket autorizado, pero no a otros recursos. Ese laboratorio me enseñó que los roles son una forma muy segura de compartir recursos sin tener que intercambiar credenciales o dar accesos amplios.

- ### Creación de usuarios y grupos IAM

En la siguiente demostración, puse en práctica lo aprendido sobre la creación de usuarios y grupos en IAM. El objetivo fue aplicar la buena práctica de otorgar permisos según el rol que cumple cada persona.
Por ejemplo, se creó un grupo llamado app-developers, al cual se le asignaron permisos limitados, como AmazonEC2ReadOnlyAccess (para ver instancias EC2 sin modificarlas) y AWSCloud9EnvironmentMember (para trabajar en entornos de desarrollo). Luego, se creó un usuario llamado “Nikhil” y se añadió a ese grupo.

Después de iniciar sesión con ese usuario, comprobé que podía ver los recursos EC2, pero no podía crear ni eliminar nada. También noté que no tenía acceso a S3, ya que no se le habían otorgado permisos para ese servicio. Este ejercicio fue muy ilustrativo porque me demostró cómo los grupos simplifican la administración de permisos y cómo el principio del mínimo privilegio se aplica de manera práctica.

- ### Lecciones aprendidas y práctica de seguridad

Además de las configuraciones, en la evaluación del módulo se planteó un escenario donde una empresa almacenaba credenciales dentro de una imagen personalizada de EC2. Aprendí que eso es una mala práctica, ya que las llaves fijas pueden filtrarse fácilmente.
La solución correcta fue asignar un rol IAM a las instancias EC2 para que obtengan credenciales temporales y seguras sin necesidad de guardarlas en archivos o código. Este tipo de ejemplos me ayudaron a afianzar la importancia de los roles y a evitar errores comunes en seguridad.

También reforcé la idea de rotar credenciales, no usar el usuario raíz para tareas diarias, y siempre habilitar MFA en cuentas y servicios sensibles. Al final, me di cuenta de que la seguridad en la nube depende de una buena configuración y del conocimiento de las herramientas que AWS nos ofrece.

- ### Conclusiones

Este módulo me ayudó a comprender que la seguridad en la nube no es algo que se deja en manos de AWS, sino una responsabilidad compartida donde el usuario tiene un papel activo y esencial. Aprendí a crear estructuras seguras de usuarios y grupos, a definir roles con credenciales temporales, a aplicar políticas específicas y a aprovechar los servicios de autenticación y autorización que ofrece IAM.

Además, ahora entiendo cómo proteger los datos en S3, cómo utilizar el versionado y las consultas directas con S3 Select, y cómo asegurar la comunicación entre servicios de manera profesional.
En conclusión, este módulo me dejó una base sólida para administrar accesos en proyectos reales y me hizo más consciente de la importancia de mantener buenas prácticas de seguridad desde el diseño de una aplicación hasta su despliegue en la nube.