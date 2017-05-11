Title: Anatomía de un Gruntfile    
Date: 2015-10-10 10:05:07 a.m.
Category: desarrollo

El objetivo de usar __Grunt__ en el Cuadro de Mando Integral es crear y _mantener_ el tema del Cuadro de Mando Integral de la forma más eficiente posible.

Este es el segundo archivo de la serie. En el primero, donde vemos como instalar Grunt y es [__Cómo usar Grunt__](http://yo.toledano.org/como-usar-grunt/).

Lo que quiero es escribir mi personalización en un archivo `.less` separado del código fuente de Bootstrap, de modo que solo tengo que controlar este archivo personal y las actualizaciones de Bootstrap serán controladas por _bower_.

> Utilizo [Twitter Bootsrap](https://getbootstrap.com) para el tema de la versión 2.0 porque realmente nunca llegué a dominar [MaterializeCSS](http://gruntjs.com/plugins). Es bastante bueno este _framework_, pero realmente soy mas productivo con Bootstrap.

## Los plugins de Grunt

Grunt tiene un sitio para [buscar plugins](http://gruntjs.com/plugins), porque actualmente hay unos 5,200 plugins, lo que hace que encontrar el plugin requiera de un buen motor de búsqueda.

La búsqueda del término `bootstrap` arroja 16 resultados. De estos, 3 _plugins_ parecen prometedores: [grunt-include-bootstrap](https://www.npmjs.com/package/grunt-include-bootstrap), [grunt-customize-bootstrap](https://www.npmjs.com/package/grunt-customize-bootstrap), [grunt-twbs](https://www.npmjs.com/package/grunt-twbs). Después de revisar el código fuente, descarto `grunt-include-bootstrap` porque se ve más complicado y sobre todo porque incluye los archivo `.less` de la versión 2 de Bootstrap. O sea, no.

Al final, elijo `grunt-twbs` porque me parece el más simple de los dos que quedan. Solo requiere el archivo `.less` en el que van las variables y el código que reemplaza[^1] al de Bootstrap.

Ahora vamos a crear el `Gruntfile` que se utilizará en el proyecto, así como los archivos `package.json` y `bower.json` que acompañan al gestor de tareas.

## Creando un `Gruntfile`

Vamos a empezar con el archivo con el que empezamos en el [artículo anterior](http://yo.toledano.org/como-usar-grunt/) e iremos agregando los gruntplugins que necesitemos y su configuración respectiva.

```javascript
module.exports = function(grunt) {

  // Configuración del proyecto.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    uglify: {
      options: {
        banner: '/*! <%= pkg.name %> <%= grunt.template.today("dd/mmm/yyyy") %> */\n'
      },
      build: {
        src: 'sources/<%= pkg.name %>.js',
        dest: 'assets/<%= pkg.name %>.min.js'
      }
    }
  });

  // Carga el plugin que nos proporciona la tarea "uglify".
  grunt.loadNpmTasks('grunt-contrib-uglify');

  // La(s) tarea(s) por default.
  grunt.registerTask('default', ['uglify']);

};
```

Al finalizar agregaremos a este archivo los siguientes _plugins_:

- [grunt-contrib-concat](https://github.com/gruntjs/grunt-contrib-uglify) - Para unir archivos en uno solo.
- [grunt-contrib-uglify](https://github.com/gruntjs/grunt-contrib-uglify) - Para minificar los archivos.
- [grunt-contrib-qunit](https://github.com/gruntjs/grunt-contrib-qunit) - Nuestra batería de pruebas.
- [grunt-contrib-jshint](https://github.com/gruntjs/grunt-contrib-jshint) - La guía de estilo de JavaScript, similar al PEP-8.
- [grunt-contrib-watch](https://github.com/gruntjs/grunt-contrib-watch) - Para vigilar los cambios en los archivos.
- [grunt-twbs](https://github.com/misterdai/grunt-twbs) - Para construir el tema con Bootstrap, en el siguiente artículo.

La primera parte es nuestra _envoltura_, que encapsula la configuración de nuestro `Gruntfile`:

    module.exports = function(grunt) {
    }

Dentro, de la envoltura, vamos a inicializar la configuración, que es un objeto `grunt`:

    grunt.initConfig({
    });

Lo siguiente es leer los datos del proyecto, desde nuestro archivo `package.json` y colocarlos en la variable `pkg`, con lo que podemos acceder a los campos de `package.json` usando la notación de punto.

    pkg: grunt.file.readJSON('package.json')


Y así vamos hasta el momento:

```javascript
module.exports = function(grunt) {
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json')
  });
};
```

 The configuration object for a task lives as a property on the configuration object, that's named the same as the task. So the "concat" task goes in our config object under the "concat" key. Below is my configuration object for the "concat" task.

### Tarea `concat`

Ahora podemos definir las tareas que queremos que ejecute Grunt. La configuración es un objeto de JavaScript que forma parte de la configuración y se accede a cada tarea como una propiedad del mismo nombre. Por ejemplo, la taera `"concat"` va en nuestro objeto de configuración bajo la clave `"concat"`. 

La tarea `concat` consiste en unir los archivos indicados en uno solo. Podemos definir una lista de archivos o usar comodines en la clave `dist.src` y definimos la salida en la clave `dist.dest`.

Pero primero debemos instalarlo y guardarlo en el archivo `Gruntfile`:

```bash
toledano@toledano src (tema) $ npm install grunt-contrib-concat --save-dev
cmi@2.0.0 /Users/toledano/proyectos/cmi_core/src
└─┬ grunt-contrib-concat@0.5.1 
  ├─┬ chalk@0.5.1 
  │ ├── ansi-styles@1.1.0 
  │ ├─┬ has-ansi@0.1.0 
  │ │ └── ansi-regex@0.2.1 
  │ ├── strip-ansi@0.3.0 
  │ └── supports-color@0.2.0 
  └── source-map@0.3.0 
```

Esto agrega la línea correspondiente en el archivo `packages.json` y nos permite usar la tarea. 

Veamos su configuración.

```javascript
concat: {
  options: {
    // define una cadena de texto que se coloca entre cada archivo unido
    separator: ';'
  },
  dist: {
    // los archivos a unir
    src: ['sources/js/*.js'],
    // la ubicacion de la salida concatenada
    dest: 'sources/tmp/js/<%= pkg.name %>.js'
  }
},
```

Observa que estamos usando la propiedad `name` que tomamos del `package.json`. Accedemos a ella usando la notación de punto `pkg.name`, porque cargamos las claves en la configuración del `Gruntfile`. Grunt tiene un motor de plantillas que usa las claves del objeto de configuración para formar la salida esperada. En nuestro ejemplo, vamos a concatenar todos los archivos que se encuentren en `sources/js/` y terminen con `.js`.

La salida, la vamos a colocar en el subdirectorio `js` de nuestros  `assets` y se va a llamar como lo indica la clave `name` del archivo `package.json`, o sea `cmi`.

Al final, en la sección de carga del `Gruntfile`, debemos indicar el módulo correspondiente `grunt.loadNpmTasks('grunt-contrib-concat');`, para tener lista la tarea.

### Tarea `uglify`

La tarea `uglify` reduce el tamaño de los archivos al eliminar todo el contenido que no sea necesario. En el caso de los archivos JavaScript, esto incluye espacios, tabulaciones y comentarios. Al hacerlo, el archivo resultante puede quedar ilegible y _feo_, de ahí su nombre. A cambio, se reduce el tamaño, lo que ahorra tiempo y ancho de banda.

Lo primero, como siempre, es instalar el _gruntplugin_ usando `npm install grunt-contrib-uglify --save-dev`. A continuación configuramos la tarea en el `Gruntfile`:

```javascript
    uglify: {
      options: {
        banner: '/*! <%= pkg.name %> <%= grunt.template.today("dd/mmm/yyyy") %> */\n'
      },
      build: {
        src: 'sources/tmp/js/<%= pkg.name %>.js',
        dest: 'assets/js/<%= pkg.name %>.min.js'
      }
    }
```

Tal como vimos en el [artículo anterior](http://yo.toledano.org/como-usar-grunt/) se toma una archivo específicado en `build.src` y se _minifica_ en donde se indica con `build.dest`. En nuestro ejemplo, tomamos la salida de la tarea `concat` y la minificamos en los `assets`.

Ahora bien, esta configuración crea archivos temporales, y usa las claves `buid.src` y `build.dest` para identificar el origen y el destino. Pero podemos ser más eficientes usando el campo `files` que se forma con un dupla `destino: [origen, ]`, por lo que podemos aprovechar que el origen ya lo tenemos en la clave `concat.dist.dest`. La tarea queda así:

```javascript
    uglify: {
      options: {
        banner: '/*! <%= pkg.name %> <%= grunt.template.today("dd/mmm/yyyy") %> */\n'
      },
      build: {
        files: {
          'assets/js/<%= pkg.name %>.min.js': ['<%= concat.dist.dest %>']
        }
      }
    }
```

### La tarea `qunit`

Como es una buena práctica de desarrollo incorporar una batería de pruebas al código para asegurar que funciona correctamente y poder hacer despliegues automáticos con confianza, vamos a ahora a incorporar la tarea `qunit` a nuestro `Gruntfile`.

Aunque he de confesar que esto es nuevo para mí. Por lo que para empezar, voy a incorporar las pruebas que vienen de ejemplo en el paquete `grunt-contrib-qunit` y luego veremos que pasa.

Antes de instalar el _gruntplugin_ debemos instalar el paquete `qunitjs` que no se instala automáticamente:

```bash
toledano@toledano src (feature/gruntfile) $ npm install qunitjs --save-dev
cmi@2.0.0 /Users/toledano/proyectos/cmi_core/src
└── qunitjs@1.19.0 
```

Necesitamos, por supuesto, instalar el módulo con `npm install grunt-contrib-qunit --save-dev` y cargarlo en la sección de _plugins_ del `Gruntfile`: `grunt.loadNpmTasks('grunt-contrib-qunit');`.

La configuración de la tarea es realmente muy simple. 

```javascript
    // :task: qunit
    // :package: grunt-contrib-qunit
    qunit: {
        files: ['test/**/*.html']
    }
```

Una batería de pruebas se compone de un archivo `.html` y el código JavaScript que ejecuta la prueba. Para administrar mejor ambos recursos, yo los separé. Esta es la página de pruebas:

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Batería de pruebas básica</title>
    <!-- Llamamos a QUnit localmente. -->
    <link rel="stylesheet" href="../../node_modules/qunitjs/qunit/qunit.css" media="screen">
    <script src="../../node_modules/qunitjs/qunit/qunit.js"></script>
    <!-- Cargamos las librerias locales y las pruebas. -->
    <script src="qunit_test.js"></script>
  </head>
  <body>
      <div id="qunit"></div>
      <div id="qunit-fixture">esto es algo mejor.</div>
  </body>
</html>
```

Y las pruebas están en el archivo `qunit_test.js`:

```javascript
QUnit.test('prueba básica', function() {
  expect(1);
  ok(true, 'esto es algo mejor.');
});


QUnit.test('acceso al DOM', function() {
  expect(1);
  var fixture = document.getElementById('qunit-fixture');
  equal(fixture.innerText, 'esto es algo mejor.', 'debo ser capaz de acceder al DOM.');
});
```

Solo tiene dos pruebas. Verifica el contenido de la página, buscando la cadena `esto es algo mejor.` y verifica el acceso al __DOM__.

Al ejecutar `grunt qunit`, vemos que pasa las pruebas:

```bash
toledano@toledano src (feature/gruntfile) $ grunt qunit
Running "qunit:files" (qunit) task
Testing sources/test/qunit1.html ..OK
>> 2 assertions passed (22ms)

Done, without errors.
```

Supongo que conforme crezca el proyecto, se agregarán más pruebas. Por ahora es todo.

### Tarea JSHint

**JSHint** es una especie de PEP8. Analiza el código JavaScript para detectar errores y problemas potenciales. Antes de instalar el _gruntplugin_, supongo que debería instalar el módulo con `npm install jshint --save-dev`. 

Luego, para instalar el plugin, hacemos lo mismo, `npm install grunt-contrib-jshint --save-dev` y lo agregamos en la sección correspondiente del `Gruntfile`, `grunt.loadNpmTasks('grunt-contrib-jshint');`.

Por otro lado, su configuración es realmente muy simple:

```js
    // :task: jshint
    // :package: grunt-contrib-jshint
    jshint: {
      // se define que archivos se van a limpiar
      files: ['gruntfile.js', 'sources/**/*.js'],
      // se configura JSHint (tal como se indica en http://www.jshint.com/docs/)
      options: {
          // aqui van las opciones, si los valores por
          // omisión no son suficientes
        globals: {
          jQuery: true,
          console: true,
          module: true
        }
      }
    }
```

Al ejecutar la tarea, JSHint analiza los archivos indicados y nos dice los problemas potenciales:

```bash
toledano@toledano src (feature/gruntfile) $ grunt jshint
Running "jshint:files" (jshint) task

   sources/js/01-uno.js
      1 |test = new Date()
                          ^ Missing semicolon.
      2 |month = test.getMonth()
                                ^ Missing semicolon.
      3 |month = (month * 1) + 1
                                ^ Missing semicolon.
      4 |day = test.getDate()
                             ^ Missing semicolon.
      5 |year = test.getFullYear()
                                  ^ Missing semicolon.
      6 |console.log(" ",month,"/",day,"/",year," ")
                                                    ^ Missing semicolon.
   sources/js/02-dos.js
      1 |console.log("Este archivo está de mas")
                                                ^ Missing semicolon.
   sources/tmp/js/cmi.js
      1 |test = new Date()
                          ^ Missing semicolon.
      2 |month = test.getMonth()
                                ^ Missing semicolon.
      3 |month = (month * 1) + 1
                                ^ Missing semicolon.
      4 |day = test.getDate()
                             ^ Missing semicolon.
      5 |year = test.getFullYear()
                                  ^ Missing semicolon.
      7 |;console.log("Este archivo está de mas")
                                                 ^ Missing semicolon.

>> 13 errors in 5 files
Warning: Task "jshint:files" failed. Use --force to continue.

Aborted due to warnings.
```

Como solo me faltan, punto y comas (`;`), voy a agregarlos a los archivos y ejecutaré de nuevo el analizador.

> Después de agregar los punto y comas que me faltaban, quedó un error provocado por la tarea `concat`. Eliminé el separador.

Una vez corregidas todas las advertencias y los errores, esta es la salida de `jshint`:

```bash
toledano@toledano src (feature/gruntfile) $ grunt jshint
Running "jshint:files" (jshint) task
>> 5 files lint free.

Done, without errors.
```

### La tarea `watch`

Para terminar con nuestro `Gruntfile`, digo, antes de dedicarnos al plugin que nos interesa que es el de Bootstrap, vamos a crear un servidor que monitorea todos los cambios de nuestros archivos y ejecuta las tareas indicadas cuando detecta alguna modificación.

Instalamos el módulo con `npm install grunt-contrib-watch --save-dev` y lo activamos en el `Gruntfile` con `grunt.loadNpmTasks('grunt-contrib-watch');`.

Su configuración también es bien sencilla. Le decimos que archivos vigilar (los mismos que `jshint`) y que tareas ejecutar si hay cambios (`jshint` y `qunit`).

```bash
toledano@toledano src (feature/gruntfile) $ grunt watch
Running "watch" task
Waiting...
>> File "sources/js/01-uno.js" changed.
Running "jshint:files" (jshint) task
>> 5 files lint free.

Running "qunit:files" (qunit) task
Testing sources/test/qunit1.html ..OK
>> 2 assertions passed (21ms)

Done, without errors.
Completed in 5.961s at Sat Oct 10 2015 16:33:25 GMT-0500 (CDT) - Waiting...
```

## Conclusión

Nuestro `Gruntfile` está listo para empezar a trabajar en el tema del cuadro de mando. 

Para terminar, así queda ya listo:

```js
module.exports = function(grunt) {

  // Configuración del proyecto.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

    // :task: concat
    // :package: grunt-contrib-concat
    concat: {
      options: {
        // define una cadena de texto que se coloca entre cada archivo unido
        separator: ' '
      },
      dist: {
        // los archivos a unir
        src: ['sources/js/*.js'],
        // la ubicacion de la salida concatenada
        dest: 'sources/tmp/js/<%= pkg.name %>.js'
      }
    },

    // :task: uglify
    // :package: grunt-contrib-uglify
    uglify: {
      options: {
        banner: '/*! <%= pkg.name %> <%= grunt.template.today("dd/mmm/yyyy") %> */\n'
      },
      build: {
        files: {
          'assets/js/<%= pkg.name %>.min.js': ['<%= concat.dist.dest %>']
        }
      }
    },

    // :task: qunit
    // :package: grunt-contrib-qunit
    qunit: {
        files: ['sources/test/**/*.html']
    },

    // :task: jshint
    // :package: grunt-contrib-jshint
    jshint: {
      // se define que archivos se van a limpiar
      files: ['gruntfile.js', 'sources/**/*.js'],
      // se configura JSHint (tal como se indica en http://www.jshint.com/docs/)
      options: {
          // aqui van las opciones, si los valores por
          // omisión no son suficientes
        globals: {
          jQuery: true,
          console: true,
          module: true
        }
      }
    },

    // :task: watch
    // :package: grunt-contrib-watch
    watch: {
        files: ['<%= jshint.files %>'],
        tasks: ['jshint', 'qunit']
    }

  });

  // Carga los plugins que nos proporcionan las tareas.
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-qunit');
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-watch');

  // La(s) tarea(s) por default.
  grunt.registerTask('default', ['concat', 'uglify', 'jshint', 'qunit']);

};
```


[^1]: En realidad no lo reemplaza el código CSS, solo las variables. Como CSS es acumulativo, este código va al final del archivo generado y por lo tanto es que usa el navegador. El código original de Bootstrap sigue ahí.
