Title: Configurando un proyecto en Node    
Date: 2017-05-06 18:33:46
Category: desarrollo
Tags: node.js, es6, babel 
Summary: 
Series: Programación Funcional


Ahora que estamos iniciando con **Node.js** es importante definir algunas cosas que afectaran el desarrollo del proyecto, por ejemplo, el uso de funciones de flecha (que se llaman _Fat Arrow_) de __ES6__ como base para el estilo de programación funcional.

### Configuración inicial
La configuración inicial es muy fácil porque el programa `npm` nos lleva de la mano.

Lo primero que tenemos que hacer es crear el directorio en el que reside nuestro proyecto. Como se me acabaron las ideas y estoy usando otras combinaciones para el _Cuadro de Mando Integral_, en esta ocasión, el proyecto se llama `cerebro`.

```bash
$ md cerebro && cd cerebro
```

En este directorio vamos a crear el archivo de configuración, solo tenemos que ejecutar la siguiente orden:

```bash
$ npm init
```

…y contestar el sencillo cuestionario que genera al final un archivo `package.json`. Para este proyecto, se ve así:

```json
{
  "name": "cerebro",
  "version": "0.1.0",
  "description": "El nuevo servidor del SGC",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1",
  },
  "repository": {
    "type": "git",
    "url": "git+https://github.com/SGC-Tlaxcala/cerebro.git"
  },
  "keywords": [
    "node",
    "javascript",
    "express",
    "mongodb"
  ],
  "author": "Javier Sanchez Toledano <js.toledano@me.com>",
  "license": "MIT",
  "bugs": {
    "url": "https://github.com/SGC-Tlaxcala/cerebro/issues"
  },
  "homepage": "https://github.com/SGC-Tlaxcala/cerebro#readme"
}
```

Es un archivo `json`, que tiene una sintaxis muy estricta y es como un diccionario. Las claves son bastante explícitas y describen el proyecto con claridad.

### Cómo agregar módulos o librerías
Node.js cuenta con un gestor de paquetes, llamado `npm`, que funciona de forma muy parecida a `apt` o `pip`[^1] que instala los módulos y librerías que necesita un proyecto _junto con todas sus dependencias_. También hay un programa que le hace competencia llamado [__Yarn__](https://yarnpkg.com) que es muy rápido y es el que vamos a usar en este proyecto.

Para instalar `yarn` usaremos _Homebrew_ en mac OSX; `apt` en Ubuntu o Debian o el gestor de paquetes de tu sistema operativo.

```bash
$ brew install yarn
```

Ahora bien, hay dos tipos de dependencias en un proyecto. Las dependencias del proyecto en si y las que se usan solo en desarrollo. Las dependencias que vamos a agregar a continuación son de este segundo tipo, solo para desarrollo, por lo tanto, al instalarlas vamos a indicar su tipo con la marca `--dev`:

```bash
$ yarn add --dev babel-cli babel-preset-es2015
```

El comando anterior descarga [__Babel__](https://babeljs.io), que es un compilador de JavaScript. Traduce el código ECMAScript  6 que vamos a usar este proyecto a la versión ECMAScript 2015 que es la más común. De esta manera usaremos la versión más moderna del lenguaje y nos aseguramos que funcionará correctamente en cualquier parte.

Este comando __modifica__ nuestro archivo `packages.json` de modo que cuando llevemos el código fuente a otra máquina solo escribiremos `yarn` y tendremos el mismo entorno en todos lados. Nuestro archivo se ve así.

```json
{
  ...
  ,
  "devDependencies": {
    "babel-cli": "^6.24.1",
    "babel-preset-es2015": "^6.24.1"
  }
}
```

### Configuración rápida de Babel

_Babel_ es un compilador compuestísimo y complejo. Lo mejor es consultar su documentación. Pero para este proyecto queremos que de forma predeterminada produzca código compatible con ES2015, por lo que vamos a crear un archivo llamado `.babelrc` que usará Babel para su configuración automática.

```json
{
  "presets": ["es2015"]
}
```

Para asegurar el funcionamiento de Babel, vamos a crear un pequeño guión en nuestro archivo `packages.json` que haga la _compilación_ del código.

Vamos a agregar en la clave `"scripts"` una entrada llamada `start`, que compile nuestro archivo principal.

```json
{
  ...
   "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1",
    "start": "babel-node src/index.js"
  },
  ...
}
```

Ahora, vamos a probar el funcionamiento del compilador.

Primero, vamos a crear un directorio llamado `src/lib` donde crearemos un archivo `utilidades.js` en el que iremos colocando algunas funciones de ayuda. Por el momento, solo una:

```js
export const consola = (mensaje) => console.log(mensaje)
```

Esta función que usa la sintaxis de flecha, solo es un sinónimo de `console.log()`. 

Ahora crearemos en el directorio `src` el archivo `index.js`, en el que importamos nuestra función y mostramos un mensaje.

```js
import { consola } from './lib/utilidades.js'

consola('Hola mundo')
```

Si ejecutamos este archivo con `node` vamos a obtener un error:

```sh
$ node src/index.js                                                                      
/Volumes/datos/Proyectos/cerebro/src/index.js:1
(function (exports, require, module, __filename, __dirname) { import { consola } from 'lib/utilidades'
                                                              ^^^^^^
SyntaxError: Unexpected token import
```

Pero si ejecutamos el script `run` que tenemos en `packages.json` nuestra salida es la correcta.

```sh
$ npm run start

> cerebro@0.1.0 start /Volumes/datos/Proyectos/cerebro
> babel-node src/index.js

Hola mundo
```

[^1]: La verdad, funciona mejor que `pip`.

Una vez que hemos verificado el funcionamiento correcto de nuestro entorno, podemos seguir adelante.