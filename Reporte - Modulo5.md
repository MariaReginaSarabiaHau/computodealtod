# **Reporte del Módulo 5 – Developing Flexible NoSQL Solutions (DynamoDB)**

- ## ¿Qué entendí del módulo?

Este módulo me ayudó a pasar de la teoría a la práctica con DynamoDB para diseñar soluciones NoSQL flexibles. Comprendí que DynamoDB es una base de datos clave-valor/documento totalmente administrada, pensada para escalar horizontalmente y mantener baja latencia. El enfoque no es normalizar tablas como en relacional, sino modelar según los patrones de acceso: qué voy a leer, cómo lo voy a filtrar y con qué frecuencia. Eso guía la elección de claves, índices y capacidad.

- ## Conceptos esenciales que interioricé

Aprendí cómo se estructura una tabla: contiene ítems y cada ítem tiene atributos. La clave primaria puede ser solo partition key o partition + sort key, y determina unicidad y distribución. DynamoDB reparte los datos por particiones usando el hash de la partition key, así que elegir una clave con alta cardinalidad y acceso uniforme evita “hot partitions”. También entendí el tema de capacidad: se puede trabajar bajo demanda o aprovisionada (RCU/WCU); la forma en que leo/escribo afecta rendimiento y costo. Para consultar por atributos que no son clave primaria, se agregan índices secundarios globales (GSI), que tienen su propia clave e incluso pueden ser dispersos si el atributo no existe en todos los ítems, lo que los vuelve eficientes para subconjuntos. Vi además Streams para reaccionar a cambios, Global Tables para replicación multi-región activa-activa, Transacciones para operaciones “todo o nada” y PITR para restauraciones puntuales hasta 35 días. Finalmente, confirmé que desde los SDK/CLI puedo no solo operar datos sino también crear y administrar tablas e índices.

- ## Lo que hice en el laboratorio y lo que aprendí

> Primero creé la tabla FoodProducts con product_name como clave primaria. Me quedó claro que esta decisión es crítica porque no se puede cambiar después; si me equivoco debo crear otra tabla y migrar. Luego empecé a insertar datos con AWS CLI y comprobé el comportamiento por defecto: si hago put-item con una clave que ya existe, DynamoDB sobrescribe el registro. Para evitar errores, utilicé expresiones condicionales como attribute_not_exists(product_name), que bloquean inserciones cuando ya existe la clave y devuelven una ConditionalCheckFailedException; esto es perfecto para patrones “insert-only”.

> Después repliqué ese control en código con Boto3 (Python) en conditional_put.py. Inserté apple pie con atributos adicionales (precio, descripción, tags) y confirmé que cambiar solo el product_id ya no sobrescribe gracias a la condición. En cambio, si cambio el product_name a cherry pie, se agrega un ítem nuevo; así garantizo que únicamente se crean productos nuevos y no se pisan registros existentes por accidente.

> Para cargas mayores, usé el proceso por lotes con batch_writer. Probé dos enfoques: con overwrite_by_pkeys=['product_name'], donde “gana” la última escritura y por eso el precio final de apple pie terminó siendo el del último registro del lote; y sin ese parámetro, donde el lote falla completo si detecta claves duplicadas, lo cual me parece mejor para datos sensibles porque me obliga a corregir el JSON antes de cargar y evita estados intermedios inconsistentes. Con ese aprendizaje, cargué el dataset real all_products.json y dejé la tabla con más de 26 ítems listos para consulta.

> Con los datos poblados, implementé dos formas de lectura. Por un lado, scan() con paginación usando LastEvaluatedKey para traer todo el catálogo (útil para páginas generales, aunque costoso en tablas grandes). Por otro lado, usé get_item cuando ya conozco la clave primaria para recuperar un solo producto de forma eficiente. Observé que los números llegan como Decimal en Python, un detalle que más adelante se normaliza en la capa Lambda antes de responder como JSON al sitio.

> Finalmente añadí un GSI llamado special_GSI con special como HASH. Esperé a que el índice quedara Active y luego ejecuté un scan sobre el índice (no sobre la tabla) con un FilterExpression que excluye elementos con tags que contengan “out of stock”. Esto me permitió obtener justo el subconjunto que la cafetería quiere mostrar por defecto: los especiales disponibles. Me gustó este patrón porque equilibra eficiencia (consulto el índice disperso) con experiencia de usuario (no muestro agotados).

- ## Conexión con la necesidad del negocio

El objetivo era que el sitio muestre un menú dinámico y rápido. Con la tabla y los scripts, el personal puede cargar y mantener el inventario sin sobrescribir por accidente; el sistema puede listar todo para vistas completas, consultar puntual por product_name, y traer solo los destacados disponibles desde el GSI para la portada. Este backend está listo para exponerse como API con Lambda + API Gateway en el siguiente paso, de modo que el frontend ya no dependa de información “quemada” sino de datos vivos.

- ## Puntos del knowledge check que reforcé

> Confirmé que DynamoDB es clave-valor/documento, que escala horizontalmente, y que las particiones dependen del hash de la partition key. Practiqué que los atributos forman el ítem y la clave primaria define la unicidad, que los GSI habilitan consultas por otros campos, que las transacciones resuelven operaciones complejas en bloque, que Streams sirven para reaccionar a cambios, que Global Tables simplifica la réplica multi-región y que con PITR puedo restaurar hasta 35 días atrás. También verifiqué que desde el API se pueden crear y administrar tablas e índices. En mi intento del quiz rondé el 90% y me sirvió para fijar estos conceptos.

- ## Errores comunes que anoté para no repetir

> Si no especifico la región, “desaparece” la tabla. Si uso put-item sin condiciones, puedo pisar datos. Con batch_writer, permitir sobrescrituras cuando no debo puede generar precios incorrectos. Consultar un GSI antes de que esté Active provoca confusiones. Y abusar de scan() puede salir caro; cuando conozco claves, debo preferir get_item o query.

- ## Conclusión 

El módulo me cambió la forma de diseñar: en DynamoDB primero defino cómo voy a acceder a los datos y después moldeo la estructura. Pude crear la tabla correcta, proteger inserciones con condiciones, dominar cargas por lote con control de duplicados, leer de forma eficiente y usar un GSI para mostrar solo lo que importa en la portada. Con esto, el backend de menú quedó sólido y listo para exponerse como API en el siguiente laboratorio.