# **Lab 12.1 – Implementando autenticación en el sitio web de la cafetería con Amazon Cognito**

En este laboratorio trabajé nuevamente desde la perspectiva de Sofía, la desarrolladora encargada del sitio web de la cafetería. Frank le pidió que el sitio no solo mostrara el inventario o permitiera solicitar reportes, sino que también fuera capaz de autenticar a un usuario antes de permitirle generar un informe. Esto era necesario porque, en el estado anterior, cualquier persona dentro de la red de la cafetería o con acceso al endpoint podía ejecutar la API de creación de reportes. Por lo tanto, el objetivo de este laboratorio fue integrar Amazon Cognito como servicio de autenticación, conectar su flujo de login al sitio web y asegurar el endpoint create_report de API Gateway para que únicamente usuarios autenticados puedan enviar solicitudes. Este laboratorio se apoya directamente en la arquitectura que construí en el Lab 11.1, donde Step Functions generaba los reportes a partir de datos reales en RDS.

- ### **Tarea 1: Preparación del entorno**

La primera parte del laboratorio consistió en preparar el entorno de trabajo y asegurarse de que todos los recursos creados previamente estaban listos para continuar. Lo primero que hice fue revisar en CloudFormation que las pilas asociadas al laboratorio estuvieran en estado CREATE_COMPLETE, ya que estas plantillas son las que levantan los buckets, la base de datos, API Gateway, Elastic Beanstalk y parte de las configuraciones de seguridad. Después accedí nuevamente al IDE de VS Code desde la URL que aparece en la sección Start Lab y me autentiqué usando la contraseña temporal proporcionada.

Dentro del IDE descargué un archivo code.zip específico para este laboratorio y lo descomprimí para obtener los archivos de trabajo. Después ejecuté el script setup.sh, que recrea la configuración realizada en los laboratorios anteriores, solicita mi dirección IPv4 pública y también un correo electrónico para confirmar la suscripción a SNS. Gracias a esto, el sitio web quedó limitado únicamente a mi IP, reforzando la seguridad del bucket estático. Verifiqué que la CLI de AWS fuera la versión 2 y que boto3 estuviera instalado correctamente. Finalmente confirmé que el sitio web de la cafetería podía cargarse desde CloudFront y observé que el botón LOGIN aún no tenía funcionalidad, lo cual es normal en este punto.

- ### **Tarea 2: Creación del User Pool y Cliente de Aplicación en Amazon Cognito**

En esta fase configuré el componente central de autenticación: un grupo de usuarios de Amazon Cognito. Abrí la consola de Cognito y comencé creando un User Pool nuevo utilizando la configuración para aplicaciones web tradicionales. Le asigné como cliente el nombre the_cafe_app_client, seleccioné “nombre de usuario” como tipo de inicio de sesión y definí que el atributo obligatorio para la autenticación sería el correo electrónico. Además agregué la URL de retorno correspondiente, que era la página callback.html servida por CloudFront.

Una vez creado, renombré el User Pool a the_cafe para mantener la coherencia con el nombre de la aplicación. Luego configuré dentro del cliente the_cafe_app_client la URL de cierre de sesión, los tipos de autorización activos y los scopes de OpenID Connect, dejando habilitados únicamente el email y openid. También ajusté la configuración del flujo de autenticación, deshabilitando SRP y habilitando el flujo basado en usuario y contraseña. Todo esto permitirá que Cognito gestione sesiones, tokens y un login completamente funcional para nuestro sitio web.

Finalmente, Cognito generó automáticamente una interfaz de login alojada, y pude verla desde la opción “Ver página de inicio de sesión”. Aunque aún no existían usuarios registrados, guardé esta URL porque sería clave para integrarla al sitio web.

- ### **Tarea 3: Preparar Cognito para interactuar con la API create_report**

La siguiente parte consistió en conectar Cognito con API Gateway para que ambos pudieran trabajar juntos. Para esto definí un servidor de recursos dentro del User Pool, el cual permite a Cognito identificar a qué endpoint debe enviar los tokens de autenticación. Tomé el endpoint de create_report desde la consola de API Gateway y lo registré como el Resource Server. Con esto, Cognito reconocerá que ese endpoint forma parte del backend que la aplicación necesitará proteger.

También confirmé que la interfaz de login de Cognito estuviera funcionando, aunque todavía no se podía iniciar sesión sin usuarios definidos. Con esta configuración lista, quedaba integrar la autenticación directamente dentro del sitio web.

- ### **Tarea 4: Integrar Cognito al sitio web de la cafetería**

Volví al IDE de VS Code para modificar el archivo config.js, que controla las variables globales del sitio web. Este archivo tenía el valor de COGNITO_LOGIN_BASE_URL_STR como null, y lo actualicé colocándole la URL completa de login generada por Cognito. Esta URL incluye el client_id, el tipo de respuesta (token) y el redirect_uri, donde Cognito enviará el token después de iniciar sesión.

Después subí la versión actualizada de config.js al bucket S3 que hospeda el sitio. Una vez hecho esto, regresé al sitio web en CloudFront y recargué la página. Al presionar LOGIN, ya no aparecía el mensaje de error anterior sino que se abría directamente la interfaz de autenticación de Amazon Cognito. Esto confirmó que el sitio ya estaba correctamente conectado al nuevo sistema de login.

- ### **Tarea 5: Revisar el comportamiento actual del endpoint create_report**

Antes de continuar con la parte de autorización, revisé cómo se comportaba el endpoint create_report desde API Gateway. Desde la consola ejecuté un test del método POST y recibí correctamente tanto el ARN de la ejecución en Step Functions como el correo con la URL del reporte. Esto era importante para verificar que el backend seguía funcionando correctamente y que la integración con la máquina de estado generadora del reporte continuaba activa.

En este punto, Cognito aún no estaba ligado a API Gateway, por lo que el endpoint seguía siendo accesible sin autenticación, siempre y cuando la solicitud viniera desde la IP configurada en WAF. Esto sentó las bases para aplicar una capa de autorización adicional en las siguientes tareas.

- ### **Tarea 6: Creación del usuario “frank” y prueba del inicio de sesión**

Para continuar con la lógica de autenticación, ingresé nuevamente a Cognito y creé un usuario llamado frank dentro del User Pool the_cafe. Le asigné una contraseña temporal y desactivé el envío de invitaciones por correo para agilizar el proceso. Luego regresé al sitio web, seleccioné LOGIN e ingresé las credenciales recién creadas.

Tal como se esperaba, Cognito me pidió cambiar la contraseña en el primer inicio de sesión. Después de actualizarla, el sitio redirigió automáticamente a callback.html, procesó el token y finalmente me llevó de vuelta a la página principal. Allí pude ver que el botón LOGIN se había reemplazado con un enlace llamado REPORT. Al hacer clic en él, se invocó el endpoint protegido de create_report y recibí el correo con el informe generado. Esta fue la primera validación de que la autenticación ya estaba funcionando.

Para validar las restricciones de IP, intenté ejecutar un comando curl desde el IDE en la nube, y API Gateway lo rechazó con el mensaje “Forbidden”, lo cual tiene sentido dado que solo mi IP local tiene permiso. Luego probé desde mi máquina local y la API sí permitió la invocación, demostrando que WAF seguía funcionando como se esperaba, pero también revelando que aún faltaba restringir el endpoint para que solo aceptara solicitudes autenticadas.

- ### **Tarea 7: Activar un autorizador de Amazon Cognito en API Gateway**

Para aplicar seguridad real al endpoint create_report, configuré un autorizador tipo Cognito dentro de API Gateway. Creé un autorizador llamado cafe_lockdown, seleccioné el User Pool the_cafe y le indiqué que el token estaría en el encabezado Authorization. Después de crearlo, volví a editar el método POST de create_report y lo configuré para que utilizara este autorizador. Añadí también el encabezado Authorization como requerido y volví a desplegar la API en el stage prod.

Con este cambio, cualquier solicitud sin un token válido debería ser rechazada. Para comprobarlo, ejecuté el comando curl desde mi máquina local sin incluir ningún token, y API Gateway respondió esta vez con “Unauthorized” en lugar de “Forbidden”. Esto confirmó que ahora el endpoint exige un JWT válido generado por Cognito.

- ### **Tarea 8: Validación final desde el sitio web**

La última parte del laboratorio consistió en probar de principio a fin la integración completa. Volví al sitio web y me inicié sesión como frank. Una vez autenticada la sesión, seleccioné REPORT y nuevamente recibí el correo con la URL del reporte, lo cual demostró que Cognito estaba transmitiendo correctamente el token y que el JavaScript del sitio estaba incluyendo el encabezado Authorization al hacer la solicitud AJAX hacia API Gateway.

Además de esto, realicé pruebas avanzadas para aprender cómo extraer el token directamente desde el navegador. Con ayuda de las herramientas de desarrollador, inspeccioné la llamada POST a create_report y pude ver el encabezado Authorization con el token Bearer. Copié este token y lo utilicé manualmente en un comando curl, el cual esta vez funcionó perfectamente al incluir el -H "Authorization: Bearer …". Esto sirve como comprobación clara de que el autorizador de Cognito está funcionando correctamente en API Gateway.

Finalmente ejecuté pruebas desde la consola del autorizador de API Gateway, pegando el token directamente, y el sistema devolvió los valores esperados confirmando que dicho token era válido. Con esto se cerró el ciclo completo entre Cognito, API Gateway, Step Functions, Lambda, S3 y SNS.

- ### **Conclusión general**

Este laboratorio permitió extender la arquitectura existente para incorporar un sistema de autenticación profesional utilizando Amazon Cognito. Ahora, el sitio web de la cafetería no solo permite generar reportes bajo demanda, sino que también exige que los usuarios inicien sesión antes de hacerlo. Con esto, Frank tiene un mecanismo seguro, sencillo y directamente integrado en el sitio para solicitar su informe actualizado de inventario cuando lo necesite.

A nivel técnico, aprendí a combinar Cognito con CloudFront, API Gateway, WAF, Step Functions y Lambda, además de integrar la UI hospedada de Cognito en un sitio web estático en S3. También configuré autorización mediante tokens JWT, autorizadores de API Gateway y validación de credenciales en tiempo real, lo cual fortalece considerablemente la seguridad de la aplicación. En conjunto, este laboratorio cierra un ciclo completo donde un sitio web estático evoluciona hacia una aplicación segura y funcional, capaz de entregar contenido dinámico y protegido a través de servicios completamente administrados de AWS.