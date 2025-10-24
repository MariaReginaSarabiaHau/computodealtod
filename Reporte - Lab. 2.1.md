# **Reporte de Laboratorio 2.1: Explorando AWS CloudShell y el IDE**

- ### Introducción
Este laboratorio práctico me permitió, como estudiante y desarrolladora con experiencia en Python, evaluar dos entornos clave en AWS para el desarrollo de soluciones en la nube: AWS CloudShell y el IDE de VS Code (ejecutándose en una instancia de Amazon EC2). La meta era entender sus capacidades para escribir, ejecutar y gestionar código y recursos de AWS, específicamente para el futuro desarrollo de la presencia en línea de la cafetería de mis padres. Logré conectarme a ambos, ejecutar comandos de la CLI de AWS, código Python con Boto3 y gestionar archivos con Amazon S3. Ambos entornos son viables, pero el IDE de VS Code ofrece la interfaz gráfica y las características completas que busco para el desarrollo a largo plazo, mientras que CloudShell es ideal para tareas rápidas y automatización.

- ### Detalle de la Exploración

  - **Tarea 1: Exploración de AWS CloudShell**

AWS CloudShell es una terminal preautenticada basada en navegador que se inicia directamente desde la Consola de administración de AWS. Es un entorno muy conveniente y rápido de usar.

> Conexión y Verificación: Abrí CloudShell y verifiqué la versión de la AWS CLI con el comando **aws --version**. Confirmé que usa la versión 2.x, lo que asegura acceso a las últimas características.

> Comandos de la AWS CLI: Ejecuté aws s3 ls para listar los buckets de S3 en la cuenta. Esto demostró la integración inmediata con la CLI, mostrando el bucket de ejemplo creado automáticamente por el laboratorio.

> Funcionalidad Multitarea: Probé la opción de "Dividir en columnas" para tener dos paneles de terminal simultáneos, lo que es útil para monitoreo o ejecución paralela de scripts.

>vEjecución de Código con SDK (Boto3):

     1. Descargué un script de Python (list-buckets.py) y lo subí a CloudShell usando la opción Files > Upload file.

      2. Revisé el contenido del script (cat list-buckets.py), que utiliza el SDK de Python Boto3 para listar los buckets de S3.

      3. Ejecuté el script con python3 list-buckets.py y confirmé que devolvía el nombre del bucket, demostrando que Boto3 está preinstalado y funcional.

> Gestión de Archivos con S3: Copié el archivo Python de mi directorio local de CloudShell al bucket de S3 usando aws s3 cp list-buckets.py s3://<bucket-name>. Esto valida su utilidad para transferir código o datos hacia y desde S3.

> Conclusión de CloudShell: Es una herramienta poderosa para la administración rápida de recursos, ejecución de scripts de automatización y comandos de la CLI, especialmente útil ya que ofrece 1 GB de almacenamiento persistente en el directorio $HOME sin costo adicional. Sin embargo, carece de un IDE gráfico completo para el desarrollo de código complejo.

      - **Tarea 2: Exploración del IDE de VS Code**
Siguiendo la recomendación de mi amiga Faythe, exploré el IDE de VS Code (accesible mediante una URL y una contraseña, ejecutándose en una instancia de EC2). Este entorno está diseñado para ofrecer una experiencia de desarrollo completa.

> Conexión y Diseño del IDE: Me conecté al IDE e ingresé la LabIDEPassword. El entorno presenta la interfaz familiar de VS Code, incluyendo un panel de navegación de archivos, un editor de texto principal y un Terminal Bash integrado en la parte inferior.

> Copia de Archivos desde S3: Utilicé el terminal Bash para ejecutar comandos de la AWS CLI, de forma similar a CloudShell. Descargué el archivo Python previamente subido a S3: aws s3 cp s3://<bucket-name>/list-buckets.py .. El archivo apareció inmediatamente en el panel de navegación, confirmando la transferencia.

> Instalación del SDK para Python (Boto3):

       - Al intentar ejecutar python3 list-buckets.py, recibí un error ModuleNotFoundError: No module named 'boto3'.

      - Esto me enseñó que, aunque Python 3 está preinstalado en la instancia de EC2, las librerías del SDK (Boto3) no lo están por defecto.

      - Instalé el SDK resolviendo el error con: sudo pip3 install boto3.

      - Tras la instalación, la ejecución del script fue exitosa.

> Creación y Carga de Archivo Web: Utilicé la interfaz gráfica (File > New Text File) para crear un simple archivo HTML con el contenido <body> Hello World. </body>. Lo guardé como index.html.

> Finalmente, subí la página web al bucket de S3 usando la AWS CLI desde el terminal integrado: aws s3 cp index.html s3://<bucket-name>/index.html.

- Conclusión del IDE de VS Code:
Este es el entorno de desarrollo que necesito. Proporciona una experiencia de programación completa con un editor de código gráfico, explorador de archivos, depuración (aunque no explorada en este lab) y un terminal funcional para la AWS CLI y la ejecución de código. Requiere la inicialización de una instancia de EC2, lo que lo hace menos instantáneo que CloudShell, pero sus características son esenciales para un proyecto como el sitio web de la cafetería.




### Conclusión del laboratirio: 
El Lab 2.1 fue una exploración comparativa de **AWS CloudShell** y el **IDE de Visual Studio Code (VS Code)**, dos entornos de desarrollo clave en AWS. Logré validar que ambos permiten la ejecución de comandos de la AWS CLI y código Python con Boto3, lo que es esencial para interactuar con servicios como Amazon S3. **CloudShell** destacó por su **acceso instantáneo y preautenticado**, siendo ideal para la administración rápida y la ejecución de scripts de automatización. Por otro lado, el **IDE de VS Code** ofreció una **experiencia de desarrollo completa y gráfica**, con un editor de código, explorador de archivos y la capacidad de instalar dependencias (como se demostró con Boto3), lo que lo hace la opción superior para la escritura, edición y gestión de proyectos complejos, como el futuro sitio web de la cafetería. En conclusión, utilizaré el IDE de VS Code para el desarrollo principal, apoyándome en CloudShell para tareas rápidas y de administración de recursos.



Conclusiones Generales
Ambos entornos de AWS son valiosos y complementarios:

AWS CloudShell: Es excelente para la administración de la infraestructura, tareas rápidas, automatización y scripts puntuales gracias a su acceso inmediato y preautenticado desde la consola.

IDE de VS Code: Es ideal para el desarrollo de software completo (escritura, edición, depuración y gestión de proyectos) al proporcionar una interfaz gráfica rica en funciones y la capacidad de instalar librerías y dependencias específicas del proyecto.

He validado que puedo utilizar la AWS CLI y el SDK de Python (Boto3) para interactuar con Amazon S3 desde ambos entornos. Para el desarrollo del sitio web de la cafetería, el IDE de VS Code será mi elección principal debido a sus características de desarrollo completas, mientras que CloudShell será mi herramienta de apoyo para la administración de recursos.

