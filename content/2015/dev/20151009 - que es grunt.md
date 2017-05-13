Title: Cómo usar Grunt    
Date: 2015-10-09 8:38:14 p.m.
Category: desarrollo
Tags: tools, frontend

Como inicio la completamente nueva versión 2.0 del Cuadro de Mando Integral, totalmente renovada y reescrita desde el origen, orientado a la norma ISO 9001:2015, aprovecho para utilizar por primera vez algunas tecnologías que nunca había usado. Como **Grunt**.

### Qué es Grunt

**Grunt** es un _administrador_ de tareas. Y sirve para automatizar las tareas repetitivas que realizamos cuando estamos desarrollando para la web, como compilar, minificar, ejecutar baterías de pruebas, limpiar el código, etc. Una vez que configuramos nuestro `Gruntfile`, el gestor de tareas hará todo ese trabajo mundano prácticamente sin ningún esfuerzo de nuestra parte.

### Por qué usar Grunt

El Ecosistema de _Grunt_ es enorme y crece cada día. Existen, literalmente, cientos de _plugins_ que permiten que _Grunt_ automatice cualquier tarea, con un mínimo de esfuerzo. Y dicen que si no existe, crearlo es muy fácil. Ya lo veremos.

### Cómo empezar a usar Grunt

__Grunt__ y sus plugins se instalan usando `npm`, el gestor de paquetes de **Node.js**. Las versiones de la rama 0.4.x de Grunt necesitan una versión de Node.js `>= 0.8.0`. Las versiones nones se consideran inestables.

> Pues yo estoy instalando la versión 4.1.2, que es la estable el día de hoy, creo. La instalé usando el comando `nvm install -s v4.1`.  
>   
> Es además la versión por default, porque use esto:
> 
>     toledano@toledano src (tema) $ nvm alias default 4.1.2
>     default -> 4.1.2 (-> v4.1.2)

Luego, debemos asegurarnos que tenemos la versión actualizada de `npm`, ejecutando `npm update -g npm`[^1]. No estoy seguro que se haya actualizado, pero este es el resultado:

```bash
toledano@toledano src (tema) $ npm update -g npm
/Users/toledano/.nvm/v4.1.2/bin/npm -> /Users/toledano/.nvm/v4.1.2/lib/node_modules/npm/bin/npm-cli.js
npm@3.3.6 /Users/toledano/.nvm/v4.1.2/lib/node_modules/npm
```

> Hubiera verificado la versión que estaba instalada, para compararla con la que se actualizó, ¿verdad? 

### Instalar el comando grunt-cli

Para poder usar Grunt, debemos instalar la interface de linea de comandos (CLI por sus siglas en inglés) de forma global. De nuevo, tal vez necesites usar `sudo` o ejecutar tu consola con permisos de administrador si usas Windows.

```bash
toledano@toledano src (tema) $ npm install -g grunt-cli
/Users/toledano/.nvm/v4.1.2/bin/grunt -> /Users/toledano/.nvm/v4.1.2/lib/node_modules/grunt-cli/bin/grunt
/Users/toledano/.nvm/v4.1.2/lib
└─┬ grunt-cli@0.1.13 
  ├─┬ findup-sync@0.1.3 
  │ ├─┬ glob@3.2.11 
  │ │ ├── inherits@2.0.1 
  │ │ └─┬ minimatch@0.3.0 
  │ │   ├── lru-cache@2.7.0 
  │ │   └── sigmund@1.0.1 
  │ └── lodash@2.4.2 
  ├─┬ nopt@1.0.10 
  │ └── abbrev@1.0.7 
  └── resolve@0.3.1 
```

Con esto, vamos a tener el comando `grunt` en la ruta, lo que nos permitirá ejecutarlo en cualquier directorio.

Es importante hacer notar que cuando instalamos `grunt-cli` no instalamos el ejecutor[^2] de tareas.

### Cómo funciona 
Cada vez que se ejecuta `grunt`, este busca la versión de Grunt que está indicada en `require()`. Gracias a esto, puedes ejecutar `grunt` en cualquier subcarpeta de tu proyecto.

Si hay una instalación de Grunt local, la CLI carga esta versión de la librería de Grunt, aplica la configuración indicada en el `Gruntfile`, y ejecuta cualquier tarea solicitada.

### Preparar un nuevo proyecto con Grunt

Una configuración involucra generalmente dos archivos: `package.json` y el `Gruntfile`.

- **`package.json`**: Este archivo es usado por `npm` para almacenar metadatos del proyecto como son los módulos npm. Debemos enlistar `grunt` y sus plugins como `devDependencies` necesarias en este archivo.
- __`Gruntfile`__: Este archivo se llama `Gruntfile.js` o `Gruntfile.coffee` y se usa para configurar las tareas y cargar los plugins de Grunt.  

> Cuando hablemos del `Gruntfile`, recuerda que puede ser `Grutnfile.js` o `Gruntfile.coffee`.

## El archivo `package.json`

El archivo `package.json` debe ubicarse en el directorio raiz de tu proyecto, junto al `Gruntfile` y debe incluirse en el código fuente del proyecto. Al ejecutar `npm install` en el mismo directorio que un `package.json` instalará las versiones correctas de las dependencias listadas en él.

Hay varias formas de crear un `package.json` para un proyecto:

- Con `grunt-init` se pueden crear automáticamente `package.json` con plantillas preexistentes.
- El comando `npm-init` crea un archivo `package.json` básico.
- Puedes usar uno de los ejemplo siguiente y modifícalo de acuerdo a tus necesidades siguiendo las [especificaciones](https://docs.npmjs.com/files/package.json).  
```json
{
  "name": "cmi",
  "version": "2.0.0",
  "license": "MIT",
  
  "author": {
    "name": "Javier Sanchez Toledano",
    "email": "js.toledano@me.com",
    "url": "http://yo.toledano.org"
  },

  "repository": "npm/npm",
  "devDependencies": {
  }
}
```

## Cómo instalar Grunt y los gruntplugins

La manera más fácil de agregar GRunt y gruntplugins a un `package,json` existente es con el comando `npm install <módulo> --save-dev`. Esto no solo instala el `<módulo>` localmente, sino que también lo agregará automáticamente a la sección `devDependencies`.

Por ejemplo, esto instalará la versión más reciente de Grunt en la carpeta de tu proyecto, y lo agregará a la sección `devDependencies`.

    npm install grunt --save-dev

> Pero antes debe existir el archivo package.json y debe tener la estructura básica indicada arriba, que no produce ningún error o advertencia y funciona correctamente.
>    
    toledano@toledano cmi_core (tema) $ npm install grunt --save-dev
    cmi@2.0.0 /Users/toledano/proyectos/cmi_core
    └─┬ grunt@0.4.5 
      ├── async@0.1.22 
      ├── coffee-script@1.3.3 
      ├── colors@0.6.2 
      ├── dateformat@1.0.2-1.2.3 
      ├── eventemitter2@0.4.14 
      ├── exit@0.1.2 
      ├─┬ findup-sync@0.1.3 
      │ ├─┬ glob@3.2.11 
      │ │ ├── inherits@2.0.1 
      │ │ └── minimatch@0.3.0 
      │ └── lodash@2.4.2 
      ├── getobject@0.1.0 
      ├─┬ glob@3.1.21 
      │ ├── graceful-fs@1.2.3 
      │ └── inherits@1.0.2 
      ├─┬ grunt-legacy-log@0.1.2 
      │ ├─┬ grunt-legacy-log-utils@0.1.1 
      │ │ ├── lodash@2.4.2 
      │ │ └── underscore.string@2.3.3 
      │ ├── lodash@2.4.2 
      │ └── underscore.string@2.3.3 
      ├── grunt-legacy-util@0.2.0 
      ├── hooker@0.2.3 
      ├── iconv-lite@0.2.11 
      ├─┬ js-yaml@2.0.5 
      │ ├─┬ argparse@0.1.16 
      │ │ ├── underscore@1.7.0 
      │ │ └── underscore.string@2.4.0 
      │ └── esprima@1.0.4 
      ├── lodash@0.9.2 
      ├─┬ minimatch@0.2.14 
      │ ├── lru-cache@2.7.0 
      │ └── sigmund@1.0.1 
      ├─┬ nopt@1.0.10 
      │ └── abbrev@1.0.7 
      ├── rimraf@2.2.8 
      ├── underscore.string@2.2.1 
      └── which@1.0.9 
> 
Y se modifica la sección `devDependencies`, agregando la línea correspondiente a Grunt.  
>  
      "devDependencies": {
        "grunt": "^0.4.5"
      }

Lo mismo puede hacerse para los _gruntplugins_ y otros módulos de node. En el siguiente ejemplo, vamos a instalar el módulo `JSHint`.

    npm install grunt-contrib-jshint --save-dev

Hay un montón de _plugins_ que puedes instalar y puedes consultarlos en la página de [plugins de Grunt](http://gruntjs.com/plugins).

Recuerda guardar los cambios de tu archivo `package.json` en tu control de versiones[^3]. 

## El archivo `Gruntfile`

Un archivo `Gruntfile.js` o `Gruntfile.coffee` es un archivo de JavaScript o CoffeeScript válido que se encuentra en la raíz de tu proyecto, junto al archivo `package.json`, y debe adjuntarse a las fuentes de tu proyecto. 

Un archivo `Gruntfile` se compone de las siguientes partes:

- Una función `wrapper`, que envuelve el contenido
- La configuración del proyecto y de la tarea
- La carga de plugins y tareas de Grunt
- Tareas personalizadas

### Un archivo `Gruntfile` de ejemplo

En el siguiente archivo `Gruntfile`, los metadatos del proyecto se importan a la configuración de Grunt desde el `package.json` del proyecto y la tarea `uglify` del plugin `grunt-contrib-uglify` se configura para _minificar_ un archivo fuente y genera un comentario de forma dinámica usando los metadatos. Cuando se ejectuta `grunt` en la línea de comandos, la tarea `uglify` será la que se ejecute por default.

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
        src: 'src/<%= pkg.name %>.js',
        dest: 'build/<%= pkg.name %>.min.js'
      }
    }
  });

  // Carga el plugin que nos proporciona la tarea "uglify".
  grunt.loadNpmTasks('grunt-contrib-uglify');

  // La(s) tarea(s) por default.
  grunt.registerTask('default', ['uglify']);

};
```

Ahora que ya tenemos el archivo `Gruntfile` completo, vamos a analizar sus componentes.

#### La función _wrapper_

Cada archivo `Gruntfile` (y cada gruntplugin) usa este formato básico. Todo el código Grunt debe colocarse dentro de esta función:

```javascript
module.exports = function(grunt) {
  // Aquí van las cosas que queremos que haga Grunt
};
```

#### Configuración del proyecto

Muchas tareas de Grunt delegan la configuración de los datos al objeto que se pasa como argumento en el método `grunt.initConfig`.

En nuestro ejemplo, lo que hace `grunt.file.readJSON('package.json')` es importar los metadatos en formato `json` almacenados en el `package.json`[^4]. Como la plantilla `<% %>` puede referirse a cualquier propiedad de la configuración, ahí es donde colocamos los datos que se leen del `package.json` y evitamos la repetición.

> No me quedaba claro al principio, pero `pkg` es el contenido del archivo `package.json`  y `name` es el campo en dicho archivo, entonces `pkg.name` nos devuelve el contenido, que en este caso es `cmi`.

Podemos almacenar cualquier dato de forma arbitraria dentro del objeto de configuración, mientras que no entren en conflicto con las propiedades requeridas por las tareas, ya que en caso contrario, serían ignoradas. Así mismo, como este archivo es JavaScript no se limita al formato JSON; por lo que podemos usar cualquier código JS válido. Esto quiere decir que podríamos generar este archivo programáticamente, si fuera necesario.

Como muchas tareas, la tarea `uglify`[^5] del plugin `grunt-contrib-uglify` necesita que su configuración esté especificada en una propiedad con el mismo nombre. En nuestro ejemplo, también agregamos la opción `banner`, junto con un objetivo `build` que minifica el archivo indicado en `src` y lo colocan en la ruta indicada en `dest`.

```javascript
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
```

> Recordemos que en este ejemplo el valor de `pkg.name` es `cmi`, por lo que el valor del campo `src`, una vez hecha la sustitución es `src: 'sources/cmi.js'` y la salida es `dest: 'assets/cmi.min.js'`. El banner queda de la siguiente manera: `/*! cmi 10/Oct/2015 */`.

#### Cargar las tareas y los plugins
Muchas tareas comunes, como la concatenación, minificación y limpieza[^6] están disponibles como plugins de grunt. Siempre y cuando un plugin esté especificado en `package.json` como dependencia y haya sido instalado con `npm install`, un plugin de Grunt puede usarse simplemente escribiendo esto en el `Gruntfile`:

```javascript
// Carga el plugin que nos proporciona la tarea "uglify".
grunt.loadNpmTasks('grunt-contrib-uglify');
```

> Observa los dos requisitos anteriores: 1. Debe estar especificado en `package.json` y __debe haberse instalado__ con `npm install`. Cuando intentaba usar `grunt` sin estos requisitos, obtenía este error:  
>   
    toledano@toledano src (tema) $ grunt 
    >> Local Npm module "grunt-contrib-uglify" not found. Is it installed?
    Warning: Task "uglify" not found. Use --force to continue.  
>        
    Aborted due to warnings.
> La solución es instalar este plugin con `npm install grunt-contrib-uglify --save`.

#### Tareas personalizadas

Se puede configurar Grunt para que ejecute una o más tareas de forma automática, definiendo una tarea `default`. En nuestro ejemplo, al ejecutar `grunt` en la línea de comandos sin especificar ninguna tarea, se ejecutará la tarea `uglify`. Se puede especificar cualquier número de tareas (con o sin argumentos) en un _array_.

```javascript
// La(s) tarea(s) por default.
grunt.registerTask('default', ['uglify']);
```

Si tu proyecto requiere tareas que no proporciona algún plugin de Grunt, puedes definirlas dentro del `Gruntfile`. Por ejemplo, para definir una tarea `default` que no utiliza ninguna configuración[^7]:

```javascript
module.exports = function(grunt) {

  // Una tarea muy básica.
  grunt.registerTask('default', 'Registrar algo.', function() {
    grunt.log.write('Estoy registrando algo...').ok();
  });

};
```

### Resultados

Para probar que nuestro ejemplo funciona, hemos instalado con `npm` los paquetes `grunt`, `grunt-contrib-jshint` y `grunt-contrib-uglify`, por lo que la sección `devDependencies` del archivo `packages.json` se ve ahora así:

```javascript
  "devDependencies": {
    "grunt": "^0.4.5",
    "grunt-contrib-jshint": "^0.11.3",
    "grunt-contrib-uglify": "^0.9.2"
  }
```

También hice un pequeño archivo JavaScript, `sources/cmi.js` que imprime la fecha actual en la consola:

```javascript
test = new Date()
month = test.getMonth()
month = (month * 1) + 1
day = test.getDate()
year = test.getFullYear()
console.log(" ",month,"/",day,"/",year," ")
```

Al ejecutar `grunt` en el directorio, 

```bash
toledano@toledano src (tema) $ grunt
Running "uglify:build" (uglify) task
>> 1 file created.

Done, without errors.
```

Obtenemos el archivo `assets/cmi.min.js`, que se ve así:

```javascript
/*! cmi 10/Oct/2015 */
test=new Date,month=test.getMonth(),month=1*month+1,day=test.getDate(),year=test.getFullYear(),console.log(" ",month,"/",day,"/",year," ");
```

## Conclusión

El uso de Grunt, facilita muchas tareas de desarrollo. Para el Cuadro de Mando Integral, el uso de Grunt será toral, tanto para la generación del tema, como la instalación de los componentes en un contenedor de Docker. Pero eso será tema de otro artículo.

En el próximo, veremos como usar Grunt para generar el tema del Cuadro de Mando usando los colores institucionales, creando un archivo `less` con las opciones mínimas.

[^1]: Yo no lo necesito, pero tu tal vez debas usar `sudo`.
[^2]: Eso me recuerda _El Fin de la Eternidad_... Gestor de Tareas, tal vez sea mejor. Lo que hace Grunt CLI es realmente ejecutar la versión de Grunt que se haya instalado junto con su `Gruntfile`. Esto permite que existan en la misma máquina mútiples versiones de Grunt simultáneamente.
[^3]: Porque decir _haz commit_ no me parece correcto.
[^4]: _Yeison_ dijo una vez un representante de cierto partido político, cuando estabamos haciendo aquello de la distritación.
[^5]: _uglify_ es algo así como _afear_ (porque _uglifycar_ es una aberración), pero en este proceso se reduce el tamaño y se efectuan, supongo yo, ciertas optimizaciones.
[^6]: _Concatenar_ es unir archivos, _minificar_ es eliminar espacios y comentarios innecesarios en el archivo de producción, _limpiar_ es asegurar que el archivo es correcto, o algo así.
[^7]: Decíamos que mientras fuera código JavaScript válido, podíamos crear tareas generadas programáticamente.

