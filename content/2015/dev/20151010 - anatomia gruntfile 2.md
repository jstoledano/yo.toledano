Title: Anatomía de un Gruntfile, parte 2    
Date: 2015-10-10 6:25:54 p.m.
Category: desarrollo
Tags:  javascript, angularjs 
Cover: http://media.toledano.org/images/2015/gruntjs1.jpg

Esta es la continuación de [Anatomía de un Gruntfile](https://yo.toledano.org/anatomia-de-un-gruntfile/) y es el tercero de una serie en la que narro mis experiencias desarrollando un [cuadro de mando integral](https://es.wikipedia.org/wiki/Cuadro_de_mando_integral) adaptado a la norma ISO 9001:2015.

## Bootsrap

Hablaba en el [artículo anterior](https://yo.toledano.org/anatomia-de-un-gruntfile/) que estoy decidido a usar [**Bootstrap de Twitter**](https://getbootstrap.com) porque me parece que tiene un mejor soporte por parte de su comunidad y porque soy más productivo.

La idea es crear un archivo `.less` que contenga las modificaciones del tema y usar [**Grunt**](http://gruntjs.com/) para construir el tema usando el gestor de tareas y uno de los plugins especializados en Bootstrap.

De las opciones existentes, seleccioné [**grunt-twbs**](https://www.npmjs.com/package/grunt-twbs) porque me parece el más simple y porque fue actualizado a mediados del mes pasado, mientras que otros no se han actualizado en años.

## La tarea `twbs`

Ya tengo un `Gruntfile` funcionando, con algunas tareas básicas: concatenar, minimizar, analizar, verificar y monitorear. Ahora voy a instalar el _gruntplugin_ `grunt-twbs` y me voy a asegurar que funcione.

Este plugin permite crear un tema sin alterar el código fuente de Bootstrap, lo que permite asegurar, por ejemplo, que la actualización no tendrá problemas, porque las personalizaciones están aisladas de este _framework_.

### Bower

Para empezar, necesitamos instalar [__Bower__](http://bower.io), que es un gestor de paquetes especializado en _frontend_, creado por los propios autores de Bootstrap.

Debemos instalarlo de forma globlal usando `npm install -g bower`. Recuerda que tal vez necesites permisos de administrador para ejecutar este comando.

```
toledano@toledano src (feature/bower) $ npm install -g bower
/Users/toledano/.nvm/v4.1.2/bin/bower -> /Users/toledano/.nvm/v4.1.2/lib/node_modules/bower/bin/bower
/Users/toledano/.nvm/v4.1.2/lib
... 
un enorme árbol de dependencias
...
```

Su funcionamiento es muy similar al de `npm`, de hecho, vamos a crear un archivo `bower.json` que asegure que se instalan todas las dependencias necesarias para nuestro cuadro de mando, con el comando interactivo `init`, que nos hace una serie de preguntas y genera el archivo de forma automática:

```
toledano@toledano src (feature/bower) $ bower init
? name: cmi
? version: 2.0.0
? description: Núcleo del Cuadro de Mando Integral 2.0
? main file: 
? what types of modules does this package expose? globals
? keywords: django, angularjs, postgresql, npm, bootstrap
? authors: Javier Sanchez Toledano <js.toledano@me.com>
? license: MIT
? homepage: https://github.com/SGC-Tlaxcala/cmi_core
? set currently installed components as dependencies? Yes
? add commonly ignored files to ignore list? Yes
? would you like to mark this package as private which prevents it from being accidentally published to the registry? No/N)
```

Después nos muestra la propuesta y al confirmarla tenemos el archivo generado:

```js
{
  "name": "cmi",
  "version": "2.0.0",
  "homepage": "https://github.com/SGC-Tlaxcala/cmi_core",
  "authors": [
    "Javier Sanchez Toledano <js.toledano@me.com>"
  ],
  "description": "Núcleo del Cuadro de Mando Integral 2.0",
  "main": "",
  "moduleType": [
    "globals"
  ],
  "keywords": [
    "django",
    "angularjs",
    "postgresql",
    "npm",
    "bootstrap"
  ],
  "license": "MIT",
  "ignore": [
    "**/.*",
    "node_modules",
    "bower_components",
    "test",
    "tests"
  ]
}
```

### Bootstrap

[__Bootstrap__](https://getbootstrap.com) es un framework de JS, CSS y HTML muy popular. Tal vez el más popular. Fue creado por Twitter y facilita enormemente el desarrollo de aplicaciones web al incorporar funcionalidades responsivas, con prioridad en dispositivos móviles.

Para instalarlo, solo debemos ejecutar `bower install bootstrap --save-dev`. Como ya sabemos, la marca `--save-dev` guarda este paquete en `bower.json` para que quede fijo como dependencia.

```
toledano@toledano src (feature/bower) $ bower install bootstrap --save-dev
bower cached        git://github.com/twbs/bootstrap.git#3.3.5
bower validate      3.3.5 against git://github.com/twbs/bootstrap.git#*
bower cached        git://github.com/jquery/jquery.git#2.1.4
bower validate      2.1.4 against git://github.com/jquery/jquery.git#>= 1.9.1
bower install       bootstrap#3.3.5
bower install       jquery#2.1.4

bootstrap#3.3.5 bower_components/bootstrap
└── jquery#2.1.4

jquery#2.1.4 bower_components/jquery
```

Este paquete se instala en el directorio `bower_components`, junto con jQuery, el framework de JS, necesario para Bootstrap. En ambos casos, se instala el código fuente y en nuestro proyecto solo debemos incluir las dependencias y las instrucciones para reconstruirlos, lo que significa un importante ahorro de recursos.

### El plugin grunt-twbs

Para instalar este _gruntplugin_ hacemos lo mismo que hicimos con los otros. Instalamos el paquete con `npm install grunt-twbs --save-dev` y lo agregamos a la sección de _plugins_ del `Gruntfile` usando `grunt.loadNpmTasks('grunt-contrib-twbs');`.

```
toledano@toledano bower_components (feature/bower) $ npm install grunt-twbs --save-dev
cmi@2.0.0 /Users/toledano/proyectos/cmi_core/src
├─┬ grunt-contrib-uglify@0.9.2
│ └─┬ maxmin@1.1.0
│   └─┬ pretty-bytes@1.0.4
│     └─┬ meow@3.4.2
│       └─┬ read-pkg-up@1.0.1
│         └─┬ read-pkg@1.1.0
│           ├─┬ load-json-file@1.0.1
│           │ └── graceful-fs@4.1.2 
│           └─┬ path-type@1.0.0
│             └── graceful-fs@4.1.2 
├─┬ grunt-lib-phantomjs@0.7.1
│ └─┬ phantomjs@1.9.18
│   └─┬ fs-extra@0.23.1
│     └── graceful-fs@4.1.2 
└─┬ grunt-twbs@0.0.5 
  └─┬ fs-extra@0.24.0 
    └── graceful-fs@4.1.2 
```

### Opciones

Hay varias opciones documentadas en el [código fuente](https://github.com/misterdai/grunt-twbs), pero nos vamos a enfocar en dos:

- `less` - que indica la ruta del archivo `.less` que contiene nuestras opciones personales, y
- `dest` -  que indica la ruta de destino. 

Agregamos la tarea a nuestro `Gruntfile` que se ve así:

```js
    // :task: twbs
    // :package: grunt-twbs
    twbs: {
        target:{
            options: {
                less: './sources/less/',
                dest: 'assets/css/<%= pkg.name %>.min.css'
            }
        }
      }
```


Lo que hace esta tarea es que toma los archivos `.less` en en directorio especificado en `target.options.less` y los copia en la ubicación de Bootstrap, que por defecto es `bower_components/bootstrap`, aunque podemos especificar otra ruta en la clave `target.options.bootstrap`.

```bash
toledano@toledano src (feature/bower) $ grunt twbs
Running "twbs:target" (twbs) task
Running Bootstrap CSS task (dist)
Bootstrap (dist) built

Done, without errors.
```

Ya que los copió, o sea, que reemplazó los originales, con los personalizados, genera el archivo `.css` de Bootstrap, con el comando `grunt dist-css` del `Gruntfile` de Bootstrap, de nuevo, hay varias [tareas disponibles](http://getbootstrap.com/getting-started/#grunt), y podemos especificarlas en la clave `target.options.cmd`. 

> Es importante tener en cuenta que este _gruntplugin_ solo maneja los archivos `.less` y solo genera un `.min.css`, __pero no hace nada con los JavaScript__. Habría que crear una tarea que copie estos archivos a mi directorio de estáticos.

## El Archivo `Gruntfile`

Así va el archivo `Gruntfile`hasta el momento:

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
    },

    // :task: twbs
    // :package: grunt-twbs
    twbs: {
        target:{
            options: {
                less: './sources/less/',
                dest: 'assets/css/<%= pkg.name %>.min.css',
                cmd: 'dist'
            }
        }
      }

  });

  // Carga los plugins que nos proporcionan las tareas.
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-qunit');
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-twbs');

  // La(s) tarea(s) por default.
  grunt.registerTask('default', ['concat', 'uglify', 'jshint', 'qunit']);

};
```

## Conclusión

Siguiendo este esquema de desarrollo, aseguramos la consistencia del tema, en cualquier ambiente de desarrollo y solo tenemos que controlar un mínimo de archivos `.less`. En mi caso copié dos, `bootstrap.less` y `variables.less` aunque solo modifiqué este último archivo.

En el próximo archivo, vamos a crear una tarea completamente nueve que colecte los demás archivos estáticos de Bootstrap o cualquier otro indicado y los copie en el directorio correcto.

