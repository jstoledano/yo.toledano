Title: Cómo usar Sass en WordPress
Date: 2014-08-24 11:33:22
Category: Desarrollo
Tags:  wordpress, sass, css
Author: Javier Sanchez Toledano
Summary: Cómo usar SASS para facilitar la personalización de temas de WordPress usando JetPack

**Sass** es un pre-procesador de lenguaje CSS que permite escribir código de forma sencilla ya que permite el uso de variables, reglas encadenadas, mezclas, importaciones en línea y mucho más, con una sintaxis completamente compatible con CSS. 

<!--more-->

Entre las características de _Sass_ podemos mencionar las siguientes:

+ Es compatible con CSS3
+ Permite extender el lenguaje con variables, uniones y mezclas
+ Tiene muchas funciones útiles para manipular colores y otros valores
+ Tiene características avanzadas, como el control de directivas para librerías
+ Produce una salida bien formada
+ Se puede integrar con _Firebug_

Sass[^1] permite mantener las hojas de estilo bien organizadas y podemos usarlo con WordPress gracias al superplugin **JetPack**.

Esto quiere decir que para usar _Sass_ en WordPress debemos instalar el superplugin JetPack y activar el módulo de __CSS Personalizado__


Y configurarlo para usar la __Sass (SCSS Syntax)__,  que es la versión o el _sabor_ de **Sass** que vamos a utilizar.


En el editor de estilos podemos usar entonces _Sass_ para personalizar nuestro tema. Veamos algunos ejemplos:

### Transparencia

Para las transparencias que aparecen en este blog, uso un _mixin_ o sea una mezcla de código CSS3, variables y funciones en un macro o función que permite que este bloque de código sea utilizado en diferentes partes de nuestra hoja de estilos asegurando resultados consistentes.

```
@mixin transparencia($color, $grado) {
  background-color:rgba($color, $grado/100);
}
```

El _mixin_ o mezcla se llama `transparencia` y establece el color de fondo con una transparencia que puede ir del `0` al `1`, y para usarlo solo tenemos que incluir el mixin con los valores que queremos, de la siguiente manera:

```
.widget {
  @include transparencia(black, 85);
}
```

Al ser procesado por _Sass_ produce el siguiente resultado:

```
.widget {
  background-color: rgba(0, 0, 0, 0.85);
}
```

### Anidamiento de código

Permite asegurar la aplicación de reglas de estilo a los elementos desados anidando las reglas de forma muy sencilla. Observa el siguiente código _Sass_:

```
.sidebar {
  a {
    &:hover {
      color: #d7c603;
    }
  }
  .widget {
    @include transparencia(black, 85);
  }
  .widget-title {
    color: #BBB;
  }
}
```

Como puedes observar, al anidar las reglas ganamos legibilidad ya que cada línea cobra sentido por si misa, porque ocupa un lugar preciso en los estilos. Y mira la salida que produce:

```
.sidebar a:hover {
  color: #d7c603;
}
.sidebar .widget {
  background-color: rgba(0, 0, 0, 0.85);
}
.sidebar .widget-title {
  color: #BBB;
}
```

Como puedes ver _Sass_ es realmente muy fácil de usar. 

Para terminar, te dejo el código completo de los estilos personalizados usados en este sitio. Si tienes alguna sugerencia, por favor, házmela saber.

```
@mixin transparencia($color, $grado) {
  background-color:rgba($color, $grado/100);
}
 
@mixin box-shadow($top, $left, $blur, $size, $color, $inset: false) {
  @if $inset {
    -webkit-box-shadow:inset $top $left $blur $size $color;
    -moz-box-shadow:inset $top $left $blur $size $color;
    box-shadow:inset $top $left $blur $size $color;
  } @else {
    -webkit-box-shadow: $top $left $blur $size $color;
    -moz-box-shadow: $top $left $blur $size $color;
    box-shadow: $top $left $blur $size $color;
  }
}
 
@mixin rounded($radius: 0.5em) {
  -webkit-border-radius: $radius;
  -moz-border-radius: $radius;
  border-radius: $radius;
}
 
@mixin gradient($from, $to) {
  background: -webkit-gradient(linear, left top, left bottom, from($from), to($to));
  background: -moz-linear-gradient(top,  $from, $to);
  filter:  progid:DXImageTransform.Microsoft.gradient(startColorstr='#{$from}', endColorstr='#{$to}');
}
 
@mixin prende(){
  opacity: 0.2;
  filter: alpha(opacity=100);
  &:hover{
    opacity: 1;
    filter: alpha(opacity=100);
  }
}

body {
  font-family: 'Lato', sans-serif;
  font-size: 16px;
}

.single, .page, .archive {
  color: #DDD;
}


.agency-pro-blue {  
  .entry-title {
    color: #CCC;
    a {
      color: #DDD;
      &:hover {
        color: #d7c603;
      }
    }
  }
}

.featured-content {
  article {
    @include transparencia(white, 60);
  }
  .entry-title {
    color: black;
    a {
      color: #333;
    }
  }
}


.entry-content {
  a {
    &:hover {
      color: #d7c603;
    }
  }
  blockquote {
    @include transparencia(white, 60);
    @include rounded();
    font-family: Georgia, serif;
    font-size: 18px;
    font-style: italic;
    margin: 0.25em 0;
    padding: 0.25em 10px 0 30px;
    line-height: 1.45;
    position: relative;
    color: #383838;
    margin-left: 60px;
    border-left: 3px solid black;
    &:before {
      display: block;
      content: "\201C";
      font-size: 80px;
      position: absolute;
      left: -43px;
      top: -20px;
      color: #ccc;
    }
  }
  sup, sub {
    font-size: 60%;
  }
  code {
    @include transparencia(black, 75);
    @include rounded(3px);
    color: #DDD;
    padding: 2px;
    font-size: 0.85em;
  }
  pre {
    white-space: pre;
    font-family: Consolas,Menlo,Monaco,Lucida Console,Liberation Mono,DejaVu Sans Mono,Bitstream Vera Sans Mono,Courier New,monospace,serif;
    margin-bottom: 10px;
    max-height: 600px;
    overflow: auto;
    padding: 5px;
    width: auto;
    @include transparencia(black, 60);
    @include rounded();
    padding: 10px 20px;
    code {
      @include transparencia(black, 0);
      color: #DDD;
      font-size: 0.85em;
    }
  }
}

.post, .page, .footer-widgets, #respond {
  @include transparencia(black, 70);
}

.footnotes {
  font-size: 0.8em;
}

.footer-widgets {
  .widget-title {
    color:#CCC;
  }
  a {
    &:hover {
      color: #d7c603;
    }
  }
}

.sidebar {
  a {
    &:hover {
      color: #d7c603;
    }
  }
  .widget {
    @include transparencia(black, 85);
  }
  .widget-title {
    color: #BBB;
  }
}
```

[^1]: Sass significa _Syntactically Awesome Style Sheets_ y puedes visitar su sitio en http://sass-lang.com

