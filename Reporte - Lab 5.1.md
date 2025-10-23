# **Reporte de Laboratorio 5.1: Working with Amazon DynamoDB**

- ### Introducción

Este laboratorio marcó un avance significativo en el desarrollo de la presencia digital de la cafetería, enfocándose en la implementación de una solución de base de datos NoSQL con Amazon DynamoDB. El objetivo principal era migrar la información estática del menú a una base de datos dinámica para que el sitio web pudiera mostrar y actualizar los productos en tiempo real, una funcionalidad clave solicitada por los clientes.

Mi trabajo consistió en dominar las operaciones fundamentales de DynamoDB: creación de tablas, inserción de datos, manipulación de elementos con expresiones condicionales, y la consulta eficiente de datos, utilizando tanto la AWS CLI como el AWS SDK para Python (Boto3).

- ### Tareas Detalladas y Exploración de Funcionalidades

- **Tarea 1 y 2: Preparación del Entorno y Creación de la Tabla**
Comencé configurando mi entorno en el IDE de VS Code, actualizando la CLI de AWS y confirmando la instalación de Boto3. El primer paso con DynamoDB fue la creación de la tabla FoodProducts utilizando un script de Python (create_table.py).

> Esquema de Clave Primaria: Definí product_name como la clave primaria HASH (partición) de la tabla. Esta elección es crucial porque garantiza que cada producto sea único, ya que los nombres de los productos no deben duplicarse, y además permite la consulta directa por nombre de producto.

> Provisioned Throughput: Asigné unidades mínimas de lectura y escritura (1 URC y 1 UCE), adecuadas para una tabla inicial.

El script utilizó el método create_table del recurso de Boto3 (DDB = boto3.resource(...)) y esperó a que la tabla alcanzara el estado Active antes de finalizar, asegurando que el recurso estuviera listo para la siguiente fase.

- **Tarea 3: Inserción de Datos y Comprensión de Expresiones Condicionales**
Esta fase se centró en la escritura de datos y en comprender el comportamiento por defecto de DynamoDB.

> Comportamiento por Defecto de PutItem: Al insertar un elemento mediante el comando aws dynamodb put-item de la CLI, observé que si la clave primaria (product_name) ya existe, la operación por defecto es sobrescribir completamente el registro existente, eliminando cualquier atributo previo.

> Importancia de las Expresiones Condicionales: Este comportamiento de sobrescritura es indeseable para añadir nuevos productos, ya que podría borrar accidentalmente datos de productos existentes al intentar una actualización. Para evitar esto, introduje la expresión condicional attribute_not_exists(product_name). Al reintentar la inserción de un elemento duplicado con esta condición, el comando falló con un error ConditionalCheckFailedException. Este es el comportamiento deseado, ya que garantiza que solo se inserten productos nuevos y evita actualizaciones accidentales.

- **Tarea 4: Inserción Condicional con Boto3 y Esquema Flexible**
Continué aplicando la lógica condicional, esta vez usando el método put_item del cliente de Boto3 (DDB = boto3.client(...)) a través del script conditional_put.py.

Tipado de Datos de Boto3: Noté la diferencia en la sintaxis de Boto3, donde los datos deben definirse con su tipo explícito (ej., 'S': 'apple pie' para cadenas, 'N': '595' para números, y 'L': [...] para listas).

> Flexibilidad de Esquema (Schema-less): El nuevo registro de 'apple pie' insertado tenía cinco atributos, a diferencia de los dos atributos iniciales (product_name y product_id). Esto confirmó la naturaleza sin esquema fijo de DynamoDB, permitiendo agregar nuevos atributos a los elementos en tiempo de ejecución sin modificar la definición de la tabla.

Al probar la inserción de un producto nuevo (cherry pie) con la expresión ConditionExpression='attribute_not_exists(product_name)', se agregó un nuevo registro sin problemas, demostrando que la lógica de inserción segura funciona tanto en la CLI como en el SDK.

- **Tarea 5: Procesamiento por Lotes (BatchWriteItem) para Escalabilidad**
Para manejar la carga masiva de datos, exploré el procesamiento por lotes, que es mucho más eficiente que las inserciones elemento por elemento.

> Manejo de Duplicados en Lotes: Al usar inicialmente el método batch_writer de Boto3 con el parámetro overwrite_by_pkeys=['product_name'], observé que los elementos duplicados de 'apple pie' en el archivo test.json resultaron en una sobrescritura, donde solo el último valor del lote (el más reciente) se mantenía.

> Garantizando la Integridad: Dado que no queremos valores incorrectos en la base de datos, modifiqué el script (test_batch_put.py) para eliminar el parámetro overwrite_by_pkeys. Al ejecutar el script modificado con datos duplicados, la operación falló con un ClientError: ValidationException, y ningún elemento fue escrito en la tabla. Este resultado es ideal, ya que obliga a la corrección de errores en la fuente de datos (el JSON) antes de la carga, asegurando la integridad.

### Conclusión

Este laboratorio ha sido fundamental para dominar las operaciones de Amazon DynamoDB, un servicio clave para cualquier aplicación moderna sin servidor. He aprendido a crear y gestionar una tabla NoSQL, aprovechando su flexibilidad de esquema para almacenar atributos complejos como listas y números. Lo más importante, he adquirido un conocimiento profundo sobre cómo garantizar la integridad de los datos durante las operaciones de escritura:

Inserciones de Elementos Únicos: Usando expresiones condicionales (attribute_not_exists) para prevenir la sobrescritura accidental.

Cargas Masivas (Batch): Eliminando el parámetro overwrite_by_pkeys para asegurar que todo el lote falle si se encuentran duplicados, lo cual obliga a la validación de la fuente de datos.

Con los datos del menú ahora almacenados de manera segura y eficiente en DynamoDB, estoy preparada para la siguiente fase del desarrollo: crear las llamadas a la API que permitirán al sitio web de la cafetería consultar y mostrar estos datos dinámicamente, pasando de un sitio estático a una experiencia interactiva para el cliente.



Carga de Producción: Finalmente, utilicé el script final (batch_put.py) para cargar los 26 productos reales del sitio web (all_products.json) sin el parámetro de sobrescritura, asegurando una carga de datos masiva exitosa y con integridad.
