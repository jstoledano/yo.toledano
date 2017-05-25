Title: Cómo funciona Express.js
Date: 2017-05-24 12:22:01
Category: desarrollo
Tags: express, es6, node, middleware
Summary: En este artículo conoceremos los principales componentes de Express.js: aplicación, petición, respuesta y los middlewares.

En términos reales, __Express.js__ solo tiene tres componentes en su núcleo, por lo que es relativamente fácil aprenderlo. Estos componentes son: `app`, `req` y `res`. Pero un concepto básico son los *middlewares* y también los revisaremos.

!!! notice "Contenido"
    [TOC]

## El objeto aplicación
El objeto **aplicación**, comúnmente llamado `app` es una instancia de **Express.js**. Es el objeto principal de nuestra aplicación y la gran mayoría de las funcionalidad del framework están construidas en él.

Una instancia de **Express.js** se crea de la siguiente manera:

    :::javascript
    import express from 'express'
    let app = new express()

Esta es una lista de las propiedades y métodos disponibles en el objeto `aplicación`:

| Propiedad/Método | Descripción |
|:--|:--|
|`app.set(nombre, valor)`|Establece propiedades específicas de la aplicación|
|`app.get(nombre)`|Recupera un valor establecido por `app.set()`|
|`app.enable(nombre)`|Activa una configuración en la app|
|`app.disable(nombre)`|Desactiva una configuración en la app|
|`app.enabled(nombre)`|Verifica si una configuración está activa|
|`app.disabled(nombre)`|Verifica si una configuración está inactiva|
|`app.configure([env], callback)`|Condiciona la activación de una configuración a una variable de entorno|
|`app.use([ruta], función)`|Carga un _middleware_ en la app|
|`app.engine(ext, callback)`|Registra un motor de plantillas|
|`app.param([name], callback)`|Agrega parámetros a la rutas|
|`app.VERBO(ruta, [callback...], callback)`|Define rutas y gestores para los verbos HTTP|
|`app.all(ruta, [callback...], callback)`|Define rutas y gestores para cualquier ruta|
|`app.locals`|Almacena variables accesibles desde cualquier vista|
|`app.render(view, [opciones], callback)`|Renderiza la vista|
|`app.routes`|Contiene una lista de las rutas definidas|
|`app.listen()`|Crea el enlace que escucha las peticiones|

La documentación de **Express.js** es excelente y una explicación más amplía de todos estos métodos y propiedades se pueden consultar en la [Referencia de API][1].

## El objeto petición
El objeto _"petición"_ de HTTP se crea cuando un cliente hace una petición a la app de **Express.js**. Este objeto, se representa por costumbre con la variable `req`, que contiene propiedades y métodos relacionados con la petición actual.

Estos son los métodos y propiedades relacionados con el objeto `req`, así como una breve descripción de los mismos.

| Propiedad/Método | Descripción |
|:--|:--|
|`req.params`|Contiene los valores de los parámetros pasados a la URI|
|`req.params(nombre)`|Regresa el valor del parámetro, ya sea GET o POST|
|`req.query`|Contiene los valores enviados por un formulario vía GET|
|`req.body`|Contiene los valores enviados por un formulario vía POST|
|`req.files`|Contiene los archivos subidos por un formulario|
|`req.route`|Proporciona detalles sobre la ruta actual|
|`req.cookies`|Contiene los valores de las *cookies*|
|`req.signedCookies`|Contiene los valores de las *cookies* firmadas|
|`req.get(encabezado)`|Contiene los encabezados de la petición HTTP|
|`req.accepts(tipos)`|Verifica si el cliente los tipos de medios indicados|
|`req.is(tipo)`|Verifica si la petición entrante es de un tipo de medio en particular|
|`req.ip`|La IP del cliente|
|`req.ips`|La IP del cliente junto con todos los proxies a través de los cuales se conecta|
|`req.path`|La ruta solicitada|
|`req.host`|_Hostname_ desde el encabezado HTTP|
|`req.fresh`|Verifica si la solicitud todavía esta _fresca_|
|`req.stale`|Verifica si la petición está congelada|
|`req.xhr`|Verifica se la petición se hizo vía una solicitud AJAX|
|`req.protocol`|El protocolo usado para hacer la petición|
|`req.secure`|Verifica si la conexión es segura|
|`req.subdomains`|Subdominios en el _hosts_|
|`req.url`|La ruta de la petición, junto con los parámetros de consulta|
|`req.originaUrl`|Se usa como respaldo de `req.url`|
|`req.acceptedLanguages`|Una lista de los lenguajes aceptados por el cliente|
|`req.acceptsLanguage(lenguaje)`|Verifica si el cliente acepta `lenguaje`|
|`req.acceptedCharsets`|Una lista de los conjuntos de caracteres aceptados por el cliente|
|`req.acceptsCharsets(charset)`|Verifica si el cliente acepta el conjunto de caracteres `charset`|

## Qué son los middlewares o intermediarios
Los *middlewares* o __intermediarios__ son funciones de JavaScript creadas para manejar las solicitudes HTTP de una aplicación Express. Pueden manipular los objetos de solicitud y de respuesta o realizar acciones aisladas o terminar el flujo de la solicitud al enviar la respuesta al cliente o al pasar el control al siguiente intermediario.

Los intermediarios se cargan en una aplicación Express usando el método `app.use()`.

 Vamos a crear un ejemplo para nuestro servidor. Lo único que va a hacer es imprimir la dirección IP del cliente que haga la solicitud. Puede que parezca un intermediario muy simplón, pero nos dará una idea de como funcionan los intermediarios o _middleware_.

```javascript
/**
 * Obtiene la IP del cliente
 * @param req.ip La IP del cliente, tomada de la solicitud.
 */
app.use((req, res, next) => {
  console.log(`Solicitud hecha desde ${req.ip}`)
  next()
})
```

Como podemos ver, un intermediario es solo una función que acepta tres parámetros: `req`, `res` y `next`. El parámetro `req` es el objeto enviado con la solicitud. `res` es el objeto devuelto como respuesta y `next` es una referencia al siguiente intermediario en el flujo. Cualquier intermediario puede terminar una solicitud enviando una respuesta de regreso al cliente usando uno de los métodos de respuesta del objeto `res`. Si un intermediario no llama a un método de respuesta __debe llamar al siguiente intermediario en el flujo__, de lo contrario la aplicación se quedaría colgada.

En la mayoría de los casos, los _middlewares_ o intermedarios son un poco más complejos, pueden estar dentro de un objeto o pueden ser módulos de Node. Veamos un caso en el que el intermediario se define primero antes de pasarse al método `app.use()`.

Así se ve un módulo intermediario si lo definimos primero.

```javascript
const _prohibido = (_diaProhibido) => {
  const _dias = ['domingo', 'lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado']
  return (req, res, next) => {
    // obtenemos el día actual
    let _dia = new Date().getDay()

    // verificamos si hoy es un día prohibido
    if (_dias[_dia] === _diaProhibido) {
      res.send(`No se permiten visitas los días ${_diaProhibido}!`)
    }
    else {
      next()
    }
  }
}
```

Bueno, acepto que un intermediario que rechaze a los visitantes un día a la semana no es una buena idea, pero la intención es conocer como funcionan los _middlewares_.


Para usarlo, debemos importarlo a nuestra `app`

    :::js
    import {prohibido} from './apps/dummy/modulos'

Y para activarlo, lo vamos a colocar antes de las rutas...

    :::js
    app.use(prohibido('jueves'))

---

La mayoría de las funcionalidades de alto nivel de __Express.js__ se implementan a través de sus intermedarios preconstruidos. Un componente indispensable en cualquier aplicación de Express.js es el intermediario `router` que es el encargado de gestionar que las solicitudes de las aplicaciones Express sean atendidas por las funciones apropiadas. A esto se le llama _"ruteo"_.


[1]: https://goo.gl/3UMMkp
