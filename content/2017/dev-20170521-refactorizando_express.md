Title: Refactorizando una aplicación Express    
Date: 2017-05-22 18:57:47
Category: desarrollo
Tags: express, es6, 
Summary: Convertir una aplicación a la versión ECMAScript 6, es un ejercicio simple pero que nos ayuda a mejorar la comprensión de este lenguaje.

Ya sabemos que **Express.js** tiene una CLI que genera un proyecto, pero ahora vamos a convertir, en la medida de mis limitadas capacidades, en la sintaxis de ECMAScript 2016. Veamos si el resultado es exitoso.

## Instalación de la CLI de Express

Primero, vamos a instalar el generador, instalando `express` como paquete global.

```terminal256
yarn global add express
```

Con esto, estamos en posibilidad de usar la CLI. Estas son las opciones de generación.

```terminal256
$ express -h                                                                                                                           

  Usage: express [options] [dir]

  Options:

    -h, --help           output usage information
        --version        output the version number
    -e, --ejs            add ejs engine support
        --pug            add pug engine support
        --hbs            add handlebars engine support
    -H, --hogan          add hogan.js engine support
    -v, --view <engine>  add view <engine> support (dust|ejs|hbs|hjs|jade|pug|twig|vash) (defaults to jade)
    -c, --css <engine>   add stylesheet <engine> support (less|stylus|compass|sass) (defaults to plain css)
        --git            add .gitignore
    -f, --force          force on non-empty directory
```

## Generación del proyecto

Bien, vamos usar como motor de plantillas Handlebars, con la opción  `--view hbs`, el preprocesador de estilos será Sass, ` --css saas` y queremos que genere un archivo `.gitignore`. Así que esta es la línea que usaremos,

```terminal256
$ express --view hbs --css sass --git nspaces 
```

Y este es el resultado:

```terminal256
   create : nspaces
   create : nspaces/package.json
   create : nspaces/app.js
   create : nspaces/.gitignore
   create : nspaces/public
   create : nspaces/routes
   create : nspaces/routes/index.js
   create : nspaces/routes/users.js
   create : nspaces/views
   create : nspaces/views/index.hbs
   create : nspaces/views/layout.hbs
   create : nspaces/views/error.hbs
   create : nspaces/bin
   create : nspaces/bin/www
   create : nspaces/public/javascripts
   create : nspaces/public/images
   create : nspaces/public/stylesheets
   create : nspaces/public/stylesheets/style.sass

   install dependencies:
     $ cd nspaces && npm install

   run the app:
     $ DEBUG=nspaces:* npm start
```

Como podemos ver, creo cuatro directorios:

* `bin` — que contiene solo un archivo, llamado `www` y es el que ejecuta el proyecto.
* `public` — contiene los archivos de plantillas, los scripts del _front-end_ y los estilos. 
*  `routes` — Contiene dos archivos, uno llamado `índex.js` y otro llamado `users.js`.
* `views` — Contiene plantillas de _Handlebars_, la base, una para errores y el índice.

Hay también un archivo `app.js`, uno `.gitignore` y un `package.json`.


### Archivo `.gitignore`

Ignora los archivos comunes del desarrollo con **Node.js**. No hay ninguna sorpresa, así que lo dejamos como esta.

### Archivo `packages.json`
Este es el contenido:

```json
{
  "name": "nspaces",
  "version": "0.0.0",
  "private": true,
  "scripts": {
    "start": "node ./bin/www"
  },
  "dependencies": {
    "body-parser": "~1.17.1",
    "cookie-parser": "~1.4.3",
    "debug": "~2.6.3",
    "express": "~4.15.2",
    "hbs": "~4.0.1",
    "morgan": "~1.8.1",
    "node-sass-middleware": "0.9.8",
    "serve-favicon": "~2.4.2"
  }
}
```

La principal modificación que vamos a hacer es que vamos a agregar las dependencias de **Babel** y modificaremos el _script_ de arranque.

```16m
yarn add --dev babel-cli babel-preset-es2015
```

Esto agrega una nueva sección a nuestro archivo, que junto con la configuración de Babel, se ve así:

```json
  "devDependencies": {
    "babel-cli": "^6.24.1",
    "babel-preset-es2015": "^6.24.1"
  },
  "babel": {
    "presets": ["es2015"]
  }
```

Vamos a cambiar el comando del script `start`, de `node` a `babel-node` y estamos listos para instalar el resto de las dependencias y probar si funciona Babel tal como está el proyecto actualmente.

```16m
$ yarn start
yarn start v0.24.5
$ babel-node ./bin/www
GET / 200 186.270 ms - 204
```

No hay nada que indique que el servidor ya arrancó o el puerto en el que está funcionando, pero si visitamos la página `http://localhost:3000` podemos ver el resultado esperado. Ya podemos empezar a refactorizar.

## Refactorizabdo `app.js`
Empezaremos con este archivo, cambiando las líneas como esta

```js
var express = require('express');
```

a esto

```js
import express from 'express'
```

Nuestros `import` se ven así:

```js
import express from 'express'
import path from 'path'
import favicon from 'serve-favicon'
import logger from 'morgan'
import cookieParser from 'cookie-parser'
import bodyParser from 'body-parser'
import sassMiddleware from 'node-sass-middleware'
```

y no hemos roto nada.  Pero ahora siguen las rutas, donde se importan archivos locales, veamos si podemos usar la misma estructura.

Los cambiamos por esto:

```js
import index from './routes/index'
import users from './routes/users'
```

y todo sigue funcionando.

La línea 

```js
var app = express();
```

cambia a 
```js
let app = express()
```

La configuración del motor de plantillas no requiere nada (solo quité el punto y coma) y se ve igual

```js
// configuracion del motor de plantillas
app.set('views', path.join(__dirname, 'views'))
app.set('view engine', 'hbs')
```

La configuración del _favicon_, la bitácora, el analizador de contenido `bodyParser` y de _cookies_, `cookieParser` tampoco cambia.

### Cambiando a SCSS
Aquí damos un pequeño brinco, porque pasamos de Sass a SCSS. El cambio es solo cuestión de gustos. La plantilla cambia a esto:

```scss
body {
  padding: 50px;
  font: 14px "Noto Sans", Helvetica, Arial, sans-serif;
}

a {
  color: indianred;
}
```

Dado el cambio en el procesador, de regreso en `app.js` hacemos los ajustes necesarios.

```js
app.use(sassMiddleware({
  src: path.join(__dirname, 'public'),
  dest: path.join(__dirname, 'public'),
  indentedSyntax: false, // true = .sass and false = .scss
  sourceMap: true
}));
```

Las rutas no cambian…

```js
app.use('/', index)
app.use('/users', users)
```

Ni el generador de errores 404…

```js
// catch 404 and forward to error handler
app.use(function(req, res, next) {
  var err = new Error('Not Found')
  err.status = 404
  next(err)
})
```

El siguiente manejado de errores, tampoco lo tocamos…

```js
// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message
  res.locals.error = req.app.get('env') === 'development' ? err : {}

  // render the error page
  res.status(err.status || 500)
  res.render('error')
})
```

Por último, exportamos la app. Sin cambios.

```js
module.exports = app
```

## Refactorizando `bin`, primera parte
No me atrevo con este archivo, pero haremos el primer intento.

Primero cambiamos la línea que importa `app`, para dejarla así:

```js
import app from '../app'    // var app = require('../app');
```

La siguiente línea es esta:

```js
var debug = require('debug')('nspaces:server');
```

Y la cambiaré en dos líneas, creo…

```js
import Debug from 'debug'
let debug = Debug('nspaces:server')
```

Ufff,  que suerte. Funcionó.

Hay una función llamada `normalizarPuerto`, que al cambiarla a `let` debe colocarse **antes** de su primer uso, quedando así:

```js
/**
 * Normalizamos un puerto a número, cadena o false
 */
let normalizarPuerto = (val) => {
  let port = parseInt(val, 10)
  if (isNaN(port)) return val
  if (port >= 0) return port
  return false
}

/**
 * El puerto lo obtenemos del entorno...
 */
let port = normalizarPuerto(process.env.PORT || '3000')
app.set('port', port)
```

Y lo mismo va a pasar con la función `siHayError`…

```js
/**
 * Event listener for HTTP server "error" event.
 */
let siHayError = (error) => {
  if (error.syscall !== 'listen') throw error
  let bind = typeof port == 'string' ? `Pipe ${port}` : `Puerto ${port}`
  // manejamos los errores con mensajes amigables
  switch (error.code) {
    case 'EACCES':
      console.error(`${bind} requiere de mayores privilefios`)
      process.exit(1)
      break
    case 'EADDRINUSE':
      console.error(`El ${bind} ya está en uso`)
      process.exit(1)
      break;
    default:
      throw error
  }
}
```

… y con `alEscuchar`…

```js
/**
 * alEscuchar es un evento de "escucha" del servidor HTTP.
 */
let alEscuchar = () => {
  let direccion = server.address()
  let bind = typeof direccion === 'string' ? `el pipe ${direccion}` : `el puerto ${direccion.puerto}`
  debug(`Escuchando en ${bind}`)
}
```

Al final el archivo se ve de esta manera:

```js
/**
 * Module dependencies.
 */
import app from '../app'
import http from 'http'
import Debug from 'debug'

let debug = Debug('nspaces:server')

/**
 * Normalizamos un puerto a número, cadena o false
 */
let normalizarPuerto = (val) => {
  let puerto = parseInt(val, 10)
  if (isNaN(puerto)) return val
  if (puerto >= 0) return puerto
  return false
}

/**
 * Event listener for HTTP server "error" event.
 */
let siHayError = (error) => {
  if (error.syscall !== 'listen') throw error
  let bind = typeof port == 'string' ? `Pipe ${port}` : `Puerto ${port}`
  // manejamos los errores con mensajes amigables
  switch (error.code) {
    case 'EACCES':
      console.error(`${bind} requiere de mayores privilefios`)
      process.exit(1)
      break
    case 'EADDRINUSE':
      console.error(`El ${bind} ya está en uso`)
      process.exit(1)
      break;
    default:
      throw error
  }
}

/**
 * alEscuchar es un evento de "escucha" del servidor HTTP.
 */
let alEscuchar = () => {
  let direccion = server.address()
  let bind = typeof direccion === 'string' ? `el pipe ${direccion}` : `el puerto ${direccion.port}`
  debug(`Escuchando en ${bind}`)
}

/**
 * El puerto lo obtenemos del entorno...
 */
const puerto = normalizarPuerto(process.env.PORT || '3000')
app.set('port', puerto)

/**
 * Creamos el servidor HTTP...
 */
const server = http.createServer(app);

/**
 * Escuchamos el puerto determinado y todas las interfaces de red...
 */
server.listen(puerto)
server.on('error', siHayError)
server.on('listening', alEscuchar)
```

## Refactorizando las rutas
Estos archivos son pequeños, así que es fácil refactorizarlos.

Este el archivo `routes/index.js` refactorizado:

```js
import express from 'express'
let _rutaIndex = express.Router()

/* GET de la portada */
_rutaIndex.get('/', (req, res, next) => res.render('index', { title: 'nSpaces' }))

module.exports = _rutaIndex
```

Y este es el archivo `routes/users.js`

```js
import express from 'express'
let _rutaUsers = express.Router()

/* De usuarios, creo. */
_rutaUsers.get('/', (req, res, next) => res.send(`respondiendo con un recurso`))

module.exports = _rutaUsers
```

## Refactorizando las plantillas
Realmente la única que requiere cambios es `index.hbs` y solo implica cambiar el `Welcome to` a `Bienvenido a`… 

```jinja
<h1>{{title}}</h1>
<p>Bienvenido a {{title}}</p>
```

## Liberando la versión refactorizada
Como ya está listo el proyecto con la sintaxis de **ES6**, vamos a liberar una versión para que podamos usarla en futuros desarrollos.

Esta es la página del proyecto [nSpaces en GitHub](https://github.com/jstoledano/nspaces/releases/tag/v0.1.0) versión **v0.1.0** firmada con GnuPG para mayor seguridad.