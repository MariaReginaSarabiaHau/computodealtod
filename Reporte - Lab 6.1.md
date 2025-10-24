# **Reporte de Lab 6.1: Developing REST APIs with Amazon API Gateway**


- ### Introducción

Este laboratorio representó la creación de la capa de interfaz de nuestra aplicación serverless, utilizando Amazon API Gateway para definir la Application Program Interface (API) REST del sitio web de la cafetería. El objetivo principal fue establecer las rutas (endpoints) de la API y, de manera estratégica, configurarlas con Integraciones Simuladas (MOCK). Esto nos permitió probar la conectividad y la estructura de datos del frontend inmediatamente, desacoplando la dependencia de la lógica de backend (AWS Lambda), que se desarrollará posteriormente.

Mi trabajo se centró en la creación programática de la API (ProductsApi), la definición de tres endpoints clave para manejar las consultas del menú, y el despliegue final para que el sitio web alojado en S3 dejara de leer datos estáticos y comenzara a comunicarse con esta nueva capa de API.

- ### Tareas y Exploración de Funcionalidades

    - Tarea 1: Preparación del Entorno y Verificación Inicial
Comencé configurando el IDE de VS Code y ejecutando un script que instaló las librerías necesarias (Boto3) y desplegó la última versión del sitio web al bucket de S3.

> Verificación del Frontend: Al cargar el sitio web en el navegador, confirmé que la aplicación estaba leyendo los datos estáticos de los archivos JSON locales (all_products.json, all_products_on_offer.json). La vista "on offer" mostraba seis productos y la vista "view all" muchos más. Esta fue la base de referencia que sabríamos que cambiaría al final del laboratorio.

  - Tarea 2 y 3: Creación de Endpoints GET con Integración MOCK
Utilicé el AWS SDK para Python (Boto3) a través de scripts (create_products_api.py, create_on_offer_api.py) para crear la API ProductsApi y definir los primeros dos recursos.

Endpoint [GET] /products:

> Creación y Método: Se creó el recurso /products con un método GET.

> Integración MOCK: Fue configurado como una integración de tipo MOCK. El cuerpo de la respuesta simulada se codificó directamente en la plantilla de respuesta (responseTemplate), devolviendo una lista de tres productos.

> Propósito: Este endpoint simula la futura consulta de toda la tabla de DynamoDB.

Endpoint [GET] /products/on_offer:

> Recurso Anidado: Este recurso fue creado como anidado en /products.

> Integración MOCK: Su integración simulada devolvía un único elemento, simulando el resultado de una consulta filtrada (sobre el GSI) para ítems en oferta.

> Exploración de MOCK: Al probar ambos endpoints en la sección PRUEBAS de la consola de API Gateway, confirmé que ambos devolvían un código de estado 200 OK y el cuerpo JSON simulado que yo había definido. Esto demostró que la interfaz de la API estaba estructuralmente correcta.

  -  Tarea 4: Creación del Endpoint POST para Reportes
Creé el tercer recurso, [POST] /create_report, al mismo nivel que /products.

> Propósito: Este endpoint está destinado a la funcionalidad de solicitud de informes por parte del personal autenticado.

> Integración MOCK: Su integración MOCK simplemente devolvió un mensaje codificado ("report requested, check your phone shortly") para confirmar que el cliente recibiría una respuesta en el futuro.

> Observación: Noté que, a diferencia de los métodos GET, este endpoint no tenía configurados los headers CORS, algo que sería crucial para la comunicación en una solicitud AJAX POST desde un dominio diferente (S3).

  - Tarea 5 y 6: Implementación y Conexión del Frontend
El último paso fue poner la API en producción y conectar el sitio web a esta nueva URL.

> Implementación: Desplegué la API seleccionando el recurso raíz / y creando la Etapa prod. Esta acción generó la URL de invocación pública de la API (ej., https://<id>.execute-api.us-east-1.amazonaws.com/prod).

> Conexión del Frontend: Reemplacé el valor null en el archivo resources/website/config.js con la URL de invocación. Usé un script de Python (update_config.py) para cargar este archivo actualizado al bucket de S3.

> Validación Final: Al refrescar el sitio web con la consola del desarrollador abierta, validé los resultados:

El sitio ya no mostraba 6 o más productos, sino tres productos en la vista "view all" y un producto en la vista "on offer", lo que coincidía exactamente con los datos simulados de mis endpoints.

La consola del desarrollador mostraba mensajes de registro indicando que la aplicación estaba realizando llamadas a API Gateway, confirmando que el frontend había migrado de los datos estáticos a la capa de API.

- ### Conclusión
Este laboratorio ha sido fundamental para establecer la capa de interfaz de comunicación y enrutamiento de nuestra arquitectura serverless. Demostré la habilidad para crear, configurar e implementar una API REST completa utilizando Amazon API Gateway y el SDK de Boto3.

Estrategia MOCK y Desacoplamiento: El uso de Integraciones MOCK fue la técnica central del laboratorio, permitiéndome desacoplar el desarrollo. Pude validar la estructura de la API (rutas, métodos y formato JSON de respuesta) y la conectividad del frontend sin esperar a que el backend (AWS Lambda) estuviera listo. Este enfoque acelera el desarrollo front-end al proporcionar un contrato de datos claro desde el inicio.

Fundamento para el Futuro: Aunque el tráfico es simulado, la configuración ya sentó las bases para los requisitos de comunicación clave, incluida la necesidad de CORS para los métodos GET (que asegura la comunicación entre el dominio de S3 y el de API Gateway).

