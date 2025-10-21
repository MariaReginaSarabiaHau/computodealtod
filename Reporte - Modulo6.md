# **Reporte del Módulo 6 – Developing REST APIs (Amazon API Gateway)**

- ### Introducción

Este módulo me llevó de “tener datos en DynamoDB a “exponerlos correctamente mediante una API. Entendí que una REST API es una interfaz que sigue el estilo Representational State Transfer, donde los recursos se modelan con rutas predecibles y métodos HTTP (GET, POST, etc.). En AWS, API Gateway es el servicio que me permite definir endpoints, integrarlos con backends (Mock, Lambda, HTTP, otros servicios), protegerlos, monitorizarlos y desplegarlos por etapas (stages) como prod. También comprendí cuándo NO usar REST: por ejemplo, para comunicación bidireccional en tiempo real (chat o dashboards en vivo) conviene WebSocket APIs; y para casos simples, de baja latencia y costo, a veces basta con HTTP APIs de API Gateway como proxy delante de Lambda.

- ### Puntos clave 

Primero, la base URI de una API en API Gateway incluye, entre otros, la región y el stage (por ejemplo, ...execute-api.us-east-1.amazonaws.com/prod). El despliegue por stages me permite tener ambientes separados y hasta variables de stage para apuntar a backends distintos sin reescribir código. Segundo, la integración define a dónde va la petición: en el laboratorio usé integración MOCK para devolver respuestas simuladas; más adelante esa integración cambiará a Lambda que consultará DynamoDB. Tercero, las plantillas de mapeo (Mapping Templates) me permiten transformar requests/responses entre el cliente y el backend; por ejemplo, si el cliente envía givenName/surname/phone y mi base solo acepta name/mobile, con la plantilla ajusto el payload y evito tocar el backend. Cuarto, CORS es fundamental cuando el sitio (S3) llama a mi API desde otro origen: debo habilitar cabeceras y métodos para que el navegador no bloquee las solicitudes. Quinto, en seguridad aprendí que puedo proteger la API con IAM, Amazon Cognito (authorizers), API Keys/Usage Plans y también AWS WAF para mitigar ataques web comunes (SQLi, XSS). Sexto, monitorización y rendimiento: con CloudWatch observo métricas como IntegrationLatency (responsividad del backend), latencia total, 4XX/5XX, y puedo optimizar con caché, throttling, compresión y buen diseño de rutas.

- ### Lo que construí en el laboratorio y por qué importa

Arranqué preparando el IDE de VS Code en EC2, verifiqué AWS CLI v2 y Boto3, y confirmé que el sitio estático de la cafetería vive en S3. Al inicio el sitio leía JSON “quemados” en el bucket (all_products.json y all_products_on_offer.json). La meta del laboratorio fue reemplazar esas fuentes por endpoints de API Gateway (por ahora simulados), para luego cambiarlos por Lambda + DynamoDB en el siguiente módulo.

> Primer endpoint [GET] /products
Con Boto3 ejecuté create_products_api.py para crear la REST API ProductsApi, el recurso /products y un método GET con integración MOCK. La respuesta simulada se definió en un response template que devuelve una lista de 3 productos con la misma forma que tendrá el JSON real (nombres con sufijos como _str, _int, etc.). En la consola de API Gateway validé el flujo: Method Request → Integration (MOCK) → Integration Response → Method Response y probé con la pestaña TEST.
Aprendizaje: Comenzar con MOCK reduce variables: pruebo rutas, mapeos y CORS sin depender todavía del backend.

> Segundo endpoint [GET] /products/on_offer
Con create_on_offer_api.py agregué el recurso anidado /on_offer bajo /products y un GET que devuelve un solo producto simulado (suficiente para que la UI reaccione).
Aprendizaje: El árbol de recursos puede ser jerárquico; mantener rutas semánticas simplifica el frontend.

> Tercer endpoint [POST] /create_report
Con create_report_api.py definí /create_report (al mismo nivel que /products) y un POST con respuesta simulada: {"msg_str":"report requested, check your phone shortly"}. A propósito, no habilité CORS aquí, porque luego esta ruta se protegerá (usuarios autenticados) y se integrará con un proceso asíncrono.
Aprendizaje: Diferentes recursos pueden tener políticas y CORS distintos según el caso de uso (público vs autenticado).

> Despliegue y stage prod
Desde la consola, Implementé la API creando el stage prod y obtuve la Invoke URL.
Aprendizaje: Nada está “en vivo” hasta desplegar; cada cambio en recursos/métodos necesita un deployment hacia un stage.

> Actualizar el sitio para usar la API
Reemplacé la API_GW_BASE_URL_STR en resources/website/config.js con la Invoke URL (terminando en /prod, sin “/” final) y ejecuté update_config.py para subir el config.js al bucket S3. Al recargar el sitio y abrir la consola del navegador, vi que ahora main.js detecta API Gateway y hace las llamadas AJAX a:

> GET /products/on_offer → la portada ahora mostró 1 producto (el simulado del segundo endpoint).

> GET /products (al pulsar view all) → aparecieron 3 productos (los del primer endpoint).
También apareció un aviso por CORS hacia /bean_products que se ignora por ahora; se resuelve en módulos siguientes.
Aprendizaje: La UI ya consume endpoints reales (aunque MOCK). Cambiar la integración a Lambda después será transparente para el frontend.

- ### Control de acceso, monitoreo y optimización

Para controlar acceso, puedo elegir IAM (para clientes de AWS), Cognito User Pools (para usuarios finales con login) o Lambda authorizers (lógica propia), y además API keys/usage plans para planes y cuotas. Para protegerme de ataques, lo más directo es AWS WAF delante de API Gateway. Para observar salud y rendimiento, 4XX/5XX, Latency, IntegrationLatency y logs de ejecución en CloudWatch. Si la API es intensiva en lectura con respuestas repetidas, puedo habilitar caché a nivel de stage o método, y combinar con throttling para estabilidad. Si necesito baja latencia y menor costo para un proxy simple a Lambda, evaluar HTTP APIs. Si necesito canales bidireccionales en tiempo real, optar por WebSocket APIs.

- ### Errores típicos que evité/anoté

No olvidar desplegar al stage tras cambios (si no, la URL sigue sirviendo la versión previa). Cuidar CORS (cabeceras, métodos y orígenes) o el navegador bloqueará. Mantener la URL de invocación exacta en config.js (con /prod y sin “/” extra). Verificar región correcta. Y recordar que IntegrationLatency mide la respuesta del backend y ayuda a separar si el retraso está en API Gateway o en la integración.

- ### Conclusión

Este módulo me enseñó a estructurar y publicar una REST API de forma profesional: definí recursos claros, usé MOCK para validar rápido, desplegué a un stage y conecté el frontend en S3. Ahora el sitio ya no depende de JSON estáticos, sino que consulta endpoints que pronto apuntarán a Lambda + DynamoDB. Me quedo con la foto completa: diseñar rutas limpias, mapear y transformar datos cuando conviene, habilitar CORS correctamente, proteger con Cognito/WAF según el público, y medir con CloudWatch para optimizar. Con esto, estoy lista para el siguiente paso: reemplazar MOCK por Lambda y cerrar el circuito dinámico end-to-end.