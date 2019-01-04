Title: Cómo agregar etiquetas de verificación de Google
Date: 2014/04/09 10:00
Category: Desarrollo
Tags: genesiswp, wordpress, php
Summary: Cómo agregar las etiquetas de verificación para los buscadores usando los hooks de Genesis Framework para un control más preciso de su localización.

Recientente integré en Yo, Toledano un reproductor de música basado en jQuery 2.0. Así que me enfrenté al problema de cambiar la versión de jQuery en WordPress de la versión 1.10 a la versión más actual 2.0.2.

Además debo de añadir a la página los archivos que hace hacen funcionar al reproductor que son dos `js` y una hoja de estilos.

En este pequeño tutorial vamos a ver como reemplazar la versión de jQuery que usa WordPress por la versión más nueva y también vamos a agregar los archivos `js` y `css` en la cabecera de nuestro sitio.

> __Usa Genesis Framework__  
[Genesis][gen] te facilita construir rápida y fácilmente increíbles sitios web con WordPress. No importa si eres un principiante o un desarrollador avanzado, [Genesis][gen] te proporciona una base segura y optimizada para los motores de búsqueda con la que puede llegar a extremos que no son posibles usando solo WordPress. Es muy simple.  
**!Empieza a usar hoy mismo [Genesis Framework][gen]!**
[gen]: http://conxb.com/genesismx

## Cambiar la versión de jQuery en Genesis Framework

Lo primero que vamos a hacer es agregar una acción a uno de los ganchos disponibles en WordPress, el que se llama `wp_enqueue_scripts`. Dentro de este gancho vamos a colocar nuestra función que hace tres cosas:

1. Evita que se cargue el jquery por defecto
2. Registra el nuevo jquery para evitar problemas de dependiencias
3. Agrega el script a la cabecera.

Usamos las funciones `wp_enqueue_script` y `wp_register_script`. Este último registra el script y se asegura que los que dependan de jQuery lo utilicen y el primero lo coloca en el lugar adecuado.

```php
add_action( 'wp_enqueue_scripts', 'jQuery200', 99);
function jQuery200() {
    wp_deregister_script( 'jquery' );
    wp_register_script( 'jquery', '//code.jquery.com/jquery-2.0.2.min.js' );;
    wp_enqueue_script( 'jquery', '//code.jquery.com/jquery-2.0.2.min.js', array( 'jquery' ), '2.0.2', false );
}
```

La función 'wp_enqueue_script' toma 5 argumentos, que son los siguientes:

+ __`$handle`__, que es el grupo de script que comparten las mismas dependencias. En nuestro ejemplo es `jquery`.
+ __`$src`___, es la URL del scriipt. En el ejemplo uso la CDN de jQuery.
+ __`$deps`__, es un array de las dependencias, en el ejemplo es `array('jquery')` y es un argumento indispensable, porque de este script dependen casi todos los demás.
+ __`$ver`__, este argumento opcional sirve para referencia de la versión utilizada, en nuestro ejemplo es `'2.0.2'` que corresponde a la versión actual de jQuery.
+ __`$in_footer`__, es un valor booleano para indicar si se debe colocar el script al final del documento. En nuestro caso usamos `false`.

### Agregar scripts a Genesis Framework

Agregar scripts que no tienen tantas dependencias es mucho más fácil, el ejemplo anterior es el caso más completo, pero por lo general agregar archivos será algo mucho más simple. Veamos el ejemplo del reproductor de música.

Este requiere 3 líneas en el encabezado de las páginas: una hoja de estilos, un script para el reproducto de música y uno adicional para el reproductor de videos.

La parte más interesante, es que estos archivos solo los necesitamos en las entradas individuales, que es donde aparece el reproductor. Así que agregué una condicional para asegurarme que solo en estas entradas vamos a tenerlos.

```php
add_action('wp_enqueue_scripts', 'estilos_toledanos'); 
function estilos_toledanos() {
    if (is_single()) {
          wp_enqueue_style('music', '/assets/css/xemusicplayer.css');
        wp_register_script('music', '/assets/js/jquery-xemusicplayer-1.0.0.min.js' );
         wp_enqueue_script('music', '/assets/js/jquery-xemusicplayer-1.0.0.min.js' );
        wp_register_script('video', '//cdnjs.cloudflare.com/ajax/libs/fitvids/1.0.1/jquery.fitvids.min.js');     
         wp_enqueue_script('video', '//cdnjs.cloudflare.com/ajax/libs/fitvids/1.0.1/jquery.fitvids.min.js');
    }
}
```

Este código funciona excelente en __[Genesis Framework][gen]__, pero en general va a funcionar en cualquier instalación de WordPress.
