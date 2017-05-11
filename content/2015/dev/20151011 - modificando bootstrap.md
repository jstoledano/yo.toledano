Title: Configurar Bootstrap con Grunt y LESS
Date: 2015-10-11 9:21:13 a.m.
Category: desarrollo
Cover: https://media.toledano.org/images/2015/bootstrap.png

Siguiendo con la serie de artículos sobre la experiencia de crear un nuevo Cuadro de Mando Integral con enfoque en la norma ISO 9001:2015, en esta nueva entrega vamos a modificar algunas opciones de framework Bootstrap.

Los artículos anteriores se enlistan a continuación:

1. [Cómo usar Grunt](https://yo.toledano.org/como-usar-grunt/)
2. [Anatomía de un `Gruntfile`, primera parte](http://yo.toledano.org/anatomia-de-un-gruntfile/)
3. [Anatomía de un `Gruntfile`, segunda parte](https://yo.toledano.org/anatomia-de-un-gruntfile-parte-2/)

## Qué es Bootstrap

Bootstrap es un _framework_ para desarrollo web. Es decir, proporciona una estructura básica, pero completamente funcional, que nos permite contruir a partir de ella, estructuras más grandes y complejas. Está específicamente diseñado para el _frontend_, es decir, la parte que se puede ver en un navegador.

Hagan de cuenta que Bootstrap proporciona los planos y las piezas para construir casas prefabricadas, como las casas Geo. Simplemente vamos usando las piezas que necesitamos sobre los planos básicos y tenemos una casa Geo lista para usar. Eso si, idéntica a todas las miles de casas Geo.

Por eso, para que nuestro cuadro de mando no parezca una casa Geo, vamos a personalizarla. Bueno, para empezar vamos a cambiar los colores y la tipografía.

## Creando un tema con Bootstrap

En el artículo anterior, creamos una tarea que toma los archivos `.less` modificados y crea un tema Bootstrap sin tocar los archivos originales. Y funciona, es decir, crea el archivo minificado en el directorio de estáticos. Pero solo el archivo `.css`.

Para nuestro tema, también necesitamos que se copien en el directorio de estáticos (llamado `assets`) las imágenes, tipografía y archivos `.js` que utiliza Bootstrap. Y que no borre los archivos diferentes que ahí encuentre.

Para eso vamos a construir la distribución de Bootstrap con la tarea `twbs` y luego vamos a sincronizar los directorios que necesitamos.

### La distribución de Bootstrap

Bootstrap tiene un `Gruntfile`, con varias tareas programadas, incluída `dist` que contruye todos los archivos que se deben distribuir para un sitio web.

Así que una vez que hemos instalado Bootstrap con `bower install bootstrap --save-dev` nos pasamos al directorio `./bower_components/bootstrap` para instalar las dependencias de `nodejs` que necesita.

![grunt dist](https://media.toledano.org/images/2015/bootstrap-grunt_dist.gif)

Esto crea la distribución completa de Bootstrap en el directorio `dist`:

```
toledano@toledano dist (develop) $ tree
.
├── css
│   ├── bootstrap-theme.css
│   ├── bootstrap-theme.css.map
│   ├── bootstrap-theme.min.css
│   ├── bootstrap.css
│   ├── bootstrap.css.map
│   └── bootstrap.min.css
├── fonts
│   ├── glyphicons-halflings-regular.eot
│   ├── glyphicons-halflings-regular.svg
│   ├── glyphicons-halflings-regular.ttf
│   ├── glyphicons-halflings-regular.woff
│   └── glyphicons-halflings-regular.woff2
└── js
    ├── bootstrap.js
    ├── bootstrap.min.js
    └── npm.js

3 directories, 14 files
```

La tarea `twbs` compila el archivo `.css`, ahora debemos copiar los directorios `fonts` y `js` a los estáticos.

### La tarea `twbs`

Existen varios gruntplugins para copiar o sincronizar archivos, pero yo elegí [`grunt-sync`](https://github.com/tomusdrw/grunt-sync) porque me pareció el más simple. Dice el autor que funciona como `grunt-contrib-copy` pero solo copia los archivos que sufrieron algún cambio.

Para conocer cuáles archivos cambiaron, lee los tiempos de modificación de los archivos de origen `src`, sobreescribe el destino si hay alguna diferencia o no existe el archivo o directorio. También es posible configurar la tarea para que compare los archivos y directorios y borre en el destino cualquiera que no estñe en el origine. Ademas, si queremos algo más seguro, podemos configurar la tarea para que compare las huellas `md5` de los archivos.

Estas son las opciones completas:

- `verbose`: Muestra una salida detallada. Valor por default: `true`
- `pretend`: Hace como que copia, pero no lo hace en realidad. Valor por default: `false`
- `failOnError`: Lanza una excepción cuando encuentra un error y se detiene la tarea. Normal: `false`
- `ignoreInDest`: Una lista de archivos que se ignoran cuando no coinciden con el origen. Valor normal: `none`
- `updateAndDelete`: Borra los archivos en destino que no estén en el origen. Valor por default: `false`
- `compareUsing`: Se especifica, el método de comparación `md5` o `mtime`. Valor por default: `mtime`.

Ahora vamos a instalar el gruntplugin con `npm install grunt-sync  --save-dev`

![npm install grunt-sync  --save-dev](npm install grunt-sync  --save-dev)

La configuración de la tarea es como sigue:

```json
// :task: sync
// :package: grunt-sync
sync: {
    bootstrap: {
        files: [{
            cwd: './bower_components/bootstrap/dist',
            src: [
                'js/*',
                'fonts/*'
            ],
            dest: './assets/'
        }],
        pretend: true,
        verbose: true
    }
}
```

Utilizo la clave `pretend: true` para verificar que esté todo correcto. Yo creo que si lo está, porque esta es mi salida.

```
toledano@toledano src (feature/bootstrap-less) $ grunt sync
Running "sync:bootstrap" (sync) task
Copying bower_components/bootstrap/dist/js/bootstrap.js -> assets/js/bootstrap.js
Copying bower_components/bootstrap/dist/js/bootstrap.min.js -> assets/js/bootstrap.min.js
Copying bower_components/bootstrap/dist/js/npm.js -> assets/js/npm.js
Copying bower_components/bootstrap/dist/fonts/glyphicons-halflings-regular.eot -> assets/fonts/glyphicons-halflings-regular.eot
Copying bower_components/bootstrap/dist/fonts/glyphicons-halflings-regular.svg -> assets/fonts/glyphicons-halflings-regular.svg
Copying bower_components/bootstrap/dist/fonts/glyphicons-halflings-regular.ttf -> assets/fonts/glyphicons-halflings-regular.ttf
Copying bower_components/bootstrap/dist/fonts/glyphicons-halflings-regular.woff -> assets/fonts/glyphicons-halflings-regular.woff
Copying bower_components/bootstrap/dist/fonts/glyphicons-halflings-regular.woff2 -> assets/fonts/glyphicons-halflings-regular.woff2

Done, without errors.
```

Ahora la voy a ejecutar sin `pretend`, y este es mi directorio `assets`:

```
toledano@toledano src (feature/bootstrap-less) $ tree assets/
assets/
├── css
│   └── cmi.min.css
├── fonts
│   ├── glyphicons-halflings-regular.eot
│   ├── glyphicons-halflings-regular.svg
│   ├── glyphicons-halflings-regular.ttf
│   ├── glyphicons-halflings-regular.woff
│   └── glyphicons-halflings-regular.woff2
└── js
    ├── bootstrap.js
    ├── bootstrap.min.js
    └── npm.js

3 directories, 9 files
```

Y ya que verificamos el funcionamiento de nuestra tarea, pasamos a la selección de colores.

### Paleta de Colores

Estoy seguro que hay una teoría de colores, que dice qué colores debemos usar juntos. Pero como yo soy un ignorante de esa teoría, voy a usar el sitio [__Paletton.com__](http://paletton.com) y a elegir unos colores que pueda usar[^1].

![Paletton](https://media.toledano.org/images/2015/paletton.png)

La ventaja de este sitio es que genera las variables de colores listas para usar para usar y compartir. Esta es mi [paleta de colores](http://paletton.com/#uid=14W0u0kjBpv5NLNcZvGoPktvMdQ).

```less
@color-primary-0: #843384;	/* Main Primary color */
@color-primary-1: #D5AED5;
@color-primary-2: #A462A4;
@color-primary-3: #6A186A;
@color-primary-4: #480148;
```

Estos _mixis_ podemos usarlos sin más en nuestro archivo `variables.less` personalizado.

```less
//== Colors
//
//## Gray and brand colors for use across Bootstrap.

// ...

// paletton.com - http://paletton.com/#uid=14W0u0kjBpv5NLNcZvGoPktvMdQ
@color-primary-0: #843384;	/* Main Primary color */
@color-primary-1: #D5AED5;
@color-primary-2: #A462A4;
@color-primary-3: #6A186A;
@color-primary-4: #480148;

@brand-primary:         @color-primary-0;
@brand-success:         @color-primary-1;
@brand-info:            @color-primary-2;
@brand-warning:         @color-primary-3;
@brand-danger:          @color-primary-4;

/* *** Mixins originales de Bootstrap
@brand-primary:         #5F2871; // #337ab7
@brand-success:         #FAECFF;
@brand-info:            #5bc0de;
@brand-warning:         #f0ad4e;
@brand-danger:          #d9534f;
*** */
```

Si decido cambiar la paleta de colores, solo tengo que reemplazar las líneas `@color-primary-[0-4]` y compilar de nuevo con `grunt-twbs`.

### La tipografía

En mi tema, solo voy a cambiar una tipografía. No me decido entre [Noto Sans](https://www.google.com/fonts/specimen/Noto+Sans) o [Lato](https://www.google.com/fonts/specimen/Lato), así que vamos a hacer unas cuantas pruebas, empezando por esta última. Esto queda indicado en la sección de _Tipografía_ de mi archivo `variables.less`.

```less
//== Typography
//
//## Font, line-height, and color for body text, headings, and more.

@font-family-sans-serif:  "Lato", Helvetica, Arial, sans-serif;
@font-family-serif:       Georgia, "Times New Roman", Times, serif;
//** Default monospace fonts for `<code>`, `<kbd>`, and `<pre>`.
@font-family-monospace:   Menlo, Monaco, Consolas, "Courier New", monospace;
@font-family-base:        @font-family-sans-serif;
```

## Conclusión

Crear un tema de Bootstrap se ha vuelto trivial usando **Grunt**. El control del tema involucra un solo archivo, lo que facilita enormemente su manejo.

En el próximo artículo, creo el archivo base del tema y probamos que funcione con la tarea de monitoreo que ya programamos.



[^1]: No necesariamente me tienen que gustar, tenemos pocas opciones para elegir: el gris, el rosita, un moradito, y algunos cafecitos.
