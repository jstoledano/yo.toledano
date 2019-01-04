Title: Cómo crear una portada personalizada en WordPress usando Genesis Framework
Date: 2013/11/19 15:36
Category: Desarrollo
Tags: php, genesiswp, wordpress
Slug: como-crear-una-portada-personalizada-en-wordpress-
Author: Javier Sanchez Toledano
Summary:

Les comparto el siguiente escenario: quiero que mi portada, la de <strong>Cyberia.MX</strong> muestre las entradas de algunas categorías, pero no todas. También quiero que muestro los tipos de entradas personalizados que he creado (<em>Custom Post Types</em>), por ejemplo, películas, aplicaciones, libros, sitios web.

La solución era, por supuesto un <em>loop</em> personalizado, pero para evitar llenar mi archivo <code>functions.php</code> de código que solo se ejecutaría en una sola página, decidí crear una página personalizada y asignarla como mi página principal.


Es cierto que <a href="http://ito.mx/genesis"><strong>Genesis Framework</strong></a> permite especificar las categorías que quieres excluir — con referencia a la primera parte de mi problema —, pero me parece que me da un mejor control especificarlo dentro de los argumentos de mi <em>loop</em> personalizado.

Además, por alguna razón, en <strong>Prose</strong> (el tema que utiliza este sitio) esa configuración no era tomada en cuenta.

La solución total a esta serie de características es una página personalizada asignada como página estática — que no es una página estática, pero de eso hablaré en otro momento —.

Para poder incluir el código en esta <em>página estática</em> debemos crear primero una plantilla de página y esto es simple porque solo es necesario un comentario en el archivo <code>.php</code>, aunque para efectos de clarificar el código, agrego algunos comentarios que ayudan a comprender el objetivo de la plantilla.

```php
<?php
/**
 * Este archivo crea la plantilla Portada para Cyberia.MX
 *
 * @author Javier Sanchez
 * @package Prose
 * @subpackage Personalización
 */

 /*
Template Name: Portada
*/
```

Eso es suficiente para que esta plantilla aparezca como opción al momento de editar una página.

<img class="aligncenter size-full wp-image-1227" title="wordpress_atributos_de_la_pagina" src="http://cyberia.mx/media/wordpress_atributos_de_la_pagina.jpg" alt="wordpress_atributos_de_la_pagina" width="202" height="197" />

El siguiente paso es eliminar el <em>loop</em> por defecto y agregar una acción con el nuestro:

```
remove_action('genesis_loop', 'genesis_do_loop');
add_action ('genesis_loop', 'cyberia_home_loop');
```

Ahora que hemos declarado que el <em>loop</em> lo va a proporcionar la función <code>cyberia_home_loop</code> vamos a declarar los argumentos para nuestro <em>loop</em>. Estos argumentos tienen el formato que se utiliza para la función <strong><a href="http://codex.wordpress.org/Class_Reference/WP_Query">WP_Query</a></strong>, ya que <code>genesis_custom_loop</code> es una forma más potente y simplificada que la función original.

```php
$args = array (
  'post_type' => array( 'post','peliculas', 'libros', 'apps'),
  'paged' => get_query_var('page') ? get_query_var('page') : 1,
  'category__not_in' => array (34, 35, 36, 236,72, 210, 229,72,4,1,213)
);
```

Lo primero que hacemos es llamar a la variable global <code>$paged</code> para asegurar la correcta paginación del blog en la portada personalizada. La siguiente línea crea la variable <code>$args</code> como un arreglo que contiene los tres argumentos de mi consulta personalizada:
<ul>
    <li><code>post_type</code> — indica en un arreglo qué tipos de entradas van a consultarse, ya que de forma estándar solo se incluye el tipo <code>'post'</code>, pero en mi caso hay tres tipos de entradas más.</li>
    <li><code>paged</code> — indica que debe seguirse el orden de paginación previamente configurado.</li>
    <li><code>category__not_in</code> — este es el que más me interesa, establece en un arreglo cuáles categorías <strong>no deben incluirse</strong> en la salida de la consulta.</li>
</ul>
Esta variable <code>$args</code> la pasamos como argumento a la función <code>genesis_custom_loop</code> en la siguiente línea de nuestra función:

    :::php
    genesis_custom_loop ( $args  );

La última línea de nuestra página personalizada es la llamada al motor de nuestro blog:

    :::php  
    genesis();

A continuación te muestro el código completo:

```php
<?php
/**
 * Este archivo crea la plantilla Portada para Cyberia.MX
 *
 * @author Javier Sanchez
 * @package Prose
 * @subpackage Personalización
 */

 /*
Template Name: Portada
*/

remove_action('genesis_loop', 'genesis_do_loop');
add_action ('genesis_loop', 'cyberia_home_loop');
function cyberia_home_loop () {

  $args = array (
    'post_type' => array( 'post','peliculas', 'libros', 'apps'),
    'paged' => get_query_var('page') ? get_query_var('page') : 1,
    'category__not_in' => array (34, 35, 36, 236,72, 210, 229,72,4,1,213)
  );
  genesis_custom_loop ( $args  );
}

genesis();

?>
```

Nuestra página no debe tener ningún contenido, al elegir esta plantilla el contenido se genera automáticamente. Y por supuesto tenemos todos los <em>hook</em> y <em>filtros</em> acostumbrados.

La ventaja de crear páginas personalizadas en <a href="http://ito.mx/genesis"><strong>Genesis Framework</strong></a> es que todas no es necesario crear pruebas condicionales para activar códigos cuando vemos la portada. Esta plantilla se llama automáticamente y todo el código dentro se ejecuta. Es como un archivo <code>functions.php</code> exclusivo para la Portada.

Y claro que podemos tener plantillas personalizadas para categorías, post específicos, etiquetas, etc. Pero poco a poco iremos conociendo esta potente característica de <a href="http://ito.mx/genesis"><strong>Genesis Framework</strong></a>.

<strong>Actualización:</strong> Republico esta entrada porque el código anterior tenía un error que ocasionaba que siempre se presentara la página 1 en la portada. Por alguna razón que desconozco la variable global <strong>$paged</strong> no se tomaba en cuenta. Ahora sí.

Agregué esta línea que hace que todo funcione con normalidad.

    :::php
    'paged' => get_query_var('page') ? get_query_var('page') : 1,

!!! alert-info "Se necesita Genesis Framework"
    Recuerda, para poder utilizar el código mostrado en este artículo, es necesario contar con [Genesis FrameWork](http://ito.mx/genesis).
