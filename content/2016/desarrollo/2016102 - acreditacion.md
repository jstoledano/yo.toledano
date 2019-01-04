Title: Acreditación y Autorización    
Date: 2016-10-25 00:46:33
Category: desarrollo
Tags: django, restful, api
Series: Angular para Djangonautas
Summary: 

Antes de entrar de lleno al desarrollo del __Cuadro de Mando Integral *reimaginado*__ usando AngularJS y Django, debemos comprender algunos conceptos _torales_ del paradigma usado.

En la definición del paradigma REST, uno de sus principios fundamentales es que las operaciones deben ser _sin estado_. 

Esto quiere decir que el servidor no debe guardar información del cliente. Sin embargo, este es el funcionamiento normal de Django y está activado [cuando creamos un proyecto](https://es.wikipedia.org/wiki/Representational_State_Transfer) por medio de las __sesiones__. Las sesiones son muy fáciles de usar, porque podemos delegar a Django operaciones como el ingreso (_login_) y la salida (_logout_). El _middleware_ `django.contrib.sessions.middleware.SessionMiddleware` se encarga de almacenar en la base de datos[^1] la información sobre la sesión, de modo que siempre este disponible en el objeto `request`.

[^1]: Generalmente, porque [hay varias formas de almacenar sesiones](https://docs.djangoproject.com/es/1.10/topics/http/sessions/#configuring-the-session-engine), como las _cookies_, caché de memoria y archivos.

## Sin estado
Como decía al principio, un sistema REST[^2] no debe almacenar el estado de las sesiones. Esta es una _restricción_ y en inglés se llama _stateless_.

[^2]: Cuando un sistema cumple con los principios del paradigma REST, se le conoce como __*RESTful*__.

De acuerdo al inventor de este paradigma de desarrollo, [Roy T. Fielding](https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm) la restricción _stateless_ se define de la siguiente manera:

> 5.1.3 sin estado  
>   
> [...] Cada solicitud desde el cliente al servidor debe contener toda la información necesaria para comprender dicha solicitud, y no puede tomar ventaja de cualquier contexto almacenado en el servidor. Por lo tanto, el estado de sesión se mantiene por completo en el cliente. [...]
De modo que, el servidor no tiene que almacenar cualquier estado de la sesión y, en consecuencia, no debe emitir identificadores de sesión.[^3]

[^3]: [https://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm#sec_5_1_3](https://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm#sec_5_1_3)

## Acreditación y Autorización

Si necesitamos acceder a los recursos protegidos de nuestra API que requieran __acreditación__[^4], cada solicitud debe contener los datos necesarios para poder acreditar adecuadamente nuestra autorización para acceder a esos recursos. Y estos datos se envían en cada solicitud en el encabezado `Authorization`[^5] de HTTP.

[^4]: Es muy frecuente que se use _autenticación_ como la traducción de _Authentication_, pero la traducción correcta es _acreditación_.
[^5]: El protocolo HTTP se define en el RFC 7235: [https://tools.ietf.org/html/rfc7235#section-4.2](https://tools.ietf.org/html/rfc7235#section-4.2).

Si tiene acceso a los recursos protegidos que requieren autenticación, cada solicitud debe contener todos los datos necesarios para ser autenticados adecuadamente / autorizado. Y datos de autenticación deben pertenecer al encabezado de autorización HTTP estándar. A partir de la RFC 7235:

Y ya que no podemos _acreditar_ nuestra _autorización_ para consultar los recursos protegidos usando sesiones como lo hacemos normalmente en Django, debemos usar otros métodos. Para efectos didácticos, usaremos __Tokens__, pero de eso hablaremos en el siguiente artículo de esta serie. 
