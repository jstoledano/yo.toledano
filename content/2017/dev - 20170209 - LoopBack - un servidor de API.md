Title: LoopBack - un servidor de API    
Date: 2017-03-29 13:16:19
Category: desarrollo
Tags: restful, javascript, loopback 
Summary: 

Ahora que empezó el desarrollo del nuevo **Cuadro de Mando Integral**, buscando alternativas para crear el prototipo de las aplicaciones me encontré con [LoopBack](http://loopback.io/), un servidor basado en NodeJS que hace API de manera instantánea. 

Para que tengan una idea, en **Django** primero se tienen que crear los modelos, luego el _serializador_, luego los ViewSet y al final agregarlos a la API… siempre y cuando uses los _endpoints_ de los modelos.  Mientras tanto en  **LoopBack** al definir los modelos se crean al mismo tiempo  la API y su respectivo _endpoint_. 

> Hay una nota muy rara en la página inicial que dice que IBM está comprometido con el desarrollo _open source_ de este framework. Supongo que hay rumores de cerrar el código o algo así.  

Instalarlo es fácil, como cualquier otro paquete de Node:

```
rpm install --general loopback-cli
```

o con el _rapidísimo_ gestor de paquetes `yarn`:

```
yarn global add loopback-cli
```

La interface de consola permite crear el proyecto y los modelos contestando unas simples preguntas. Por ejemplo para crear un proyecto similar al #cmi usamos simplemente `lb`  y respondemos el cuestionario que creará el proyecto.

```
 /Volumes/datos/projects $ lb

     _-----_
    |       |    ╭──────────────────────────╮
    |--(o)--|    │  Let's create a LoopBack │
   `---------´   │       application!       │
    ( _´U`_ )    ╰──────────────────────────╯
    /___A___\   /
     |  ~  |
   __'.___.'__
 ´   `  |° ´ Y `

? What's the name of your application? lb-cmi
? Enter name of the directory to contain the project: lb-cmi
   create lb-cmi/
     info change the working directory to lb-cmi

? Which version of LoopBack would you like to use? 3.x (current)
? What kind of application do you have in mind? api-server (A LoopBack API server with local User auth)
```

Después de un rato (o de un gran rato si tienes una conexión lenta como la mía) estaremos en posibilidad de crear nuestro primer modelo.

## Sitios
Nuestro primer modelo va a ser el más simple de todos: los sitios. Tenemos solo cuatro sitios, la delegación y tres delegaciones. Así que solo necesitamos un campo `nombre` tipo `string`, un campo `lugar`  también tipo `string`  y un campo `teléfonos` tipo `object`  para guardar… pues los teléfonos.

### Cómo crear modelos
Esto es muy simple usando la _cli_, **dentro de nuestro directorio**:
```
$ lb model
```

Y tenemos un cuestionario que nos guía paso a paso para crear el modelo con los campos, que aquí se llaman **propiedades**. Vamos a especificar las propiedades de nuestro modelo y cuando terminemos solo debemos dejar en blanco la pregunta.
```
lb model
? Enter the model name: sitio
? Select the data-source to attach sitio to: db (memory)
? Select model's base class PersistedModel
? Expose sitio via the REST API? Yes
? Custom plural form (used to build REST URL): sitios
? Common model or server only? common
Let's add some sitio properties now.

Enter an empty property name when done.
? Property name: nombre
   invoke   loopback:property
? Property type: string
? Required? Yes
? Default value[leave blank for none]:

Let's add another sitio property.
Enter an empty property name when done.
? Property name: lugar
   invoke   loopback:property
? Property type: string
? Required? Yes
? Default value[leave blank for none]:

Let's add another sitio property.
Enter an empty property name when done.
? Property name: telefonos
   invoke   loopback:property
? Property type: object
? Required? No
? Default value[leave blank for none]:

Let's add another sitio property.
Enter an empty property name when done.
? Property name:
```

Bueno, eso es suficiente. No solo tenemos un modelo, también una API y un montón de _endpoints_. El servidor funciona simplemente escribiendo `node .`  lo que nos da dos URL, el servidor y un explorar de la API.

```
$ node .
Web server listening at: http://0.0.0.0:3000
Browse your REST API at http://0.0.0.0:3000/explorer
```

El explorador nos muestra todos los _endpoint_ de forma muy completa

Tenemos los verbos comunes en una API RESTful, como GET, POST, PUT, PATCH, y cada uno de estos _endpoints_ tiene las funciones necesarias para funcionar de inmediato.

Vamos a escribir un dato, siguiendo el ejemplo proporcionado, a través de esta interface para ver el resultado.

```
{
  "nombre":  "Junta Local",
  "lugar": "Tlaxcala",
  "id": 0,
  "telefonos":  {
    "Ejecutivo": "555 123 456",
    "Secretario": "555 456 789",
    "Registro": "246 123 456"
  }
}
```

El sitio genera una línea de comando para usar con el programa `curl`:

```
curl -X PATCH --header 'Content-Type: application/json' --header 'Accept: application/json' -d '{ \ 
   "nombre":  "Junta Local", \ 
   "lugar": "Tlaxcala", \ 
   "id": 0, \ 
   "telefonos":  { \ 
     "Ejecutivo": "555 123 456", \ 
     "Secretario": "555 456 789", \ 
     "Registro": "246 123 456" \ 
   } \ 
 }' 'http://localhost:3000/api/sitios'
```

Pero tal como escribí los parámetros obtengo un error, porque no debo proporcionar el valor del campo `id`, 
```
Unhandled error for request PATCH /api/sitios: ValidationError: The `sitio` instance is not valid. Details: `id` can't be set (value: 0).
```

así que hagámoslo de nuevo sin este valor.

```
{
  "nombre":  "Junta Local",
  "lugar": "Tlaxcala",
  "telefonos":  {
    "Ejecutivo": "555 123 456",
    "Secretario": "555 456 789",
    "Registro": "246 123 456"
  }
}
```
Ahora si tenemos el código `200`  que significa que la operación fue exitosa. Esta es la respuesta:
```
{
  "nombre": "Junta Local",
  "lugar": "Tlaxcala",
  "telefonos": {
    "Ejecutivo": "555 123 456",
    "Secretario": "555 456 789",
    "Registro": "246 123 456"
  },
  "id": 1
}
```

Podemos usar `http` o `curl`  para usar el verbo `GET`  y ver que devuelve lo siguiente:

```
$ http http://localhost:3000/api/sitios
HTTP/1.1 200 OK
Access-Control-Allow-Credentials: true
Connection: keep-alive
Content-Length: 144
Content-Type: application/json; charset=utf-8
Date: Fri, 10 Feb 2017 03:05:54 GMT
ETag: W/"90-RRBxD86BZQre00tk5+5KiQ"
Vary: Origin, Accept-Encoding
X-Content-Type-Options: nosniff
X-Download-Options: noopen
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block

[
    {
        "id": 1,
        "lugar": "Tlaxcala",
        "nombre": "Junta Local",
        "telefonos": {
            "Ejecutivo": "555 123 456",
            "Registro": "246 123 456",
            "Secretario": "555 456 789"
        }
    }
]
```

¿Qué tal? Una API instantánea, estándar y completa.

Por el momento, eso es todo. En el próximo artículo, veremos que opciones tenemos para guardar nuestros datos en alguna base de datos.
