Title: Integrar el protocolo OpenGraph en Genesis
Date: 2013/11/28 22:06
Category: Desarrollo 
Tags: genesiswp, php, wordpress
Slug: integrar-el-protocolo-opengraph-en-genesis
Author: Javier Sanchez Toledano
Summary: 

El protocolo Open Graph te permite integrar tus páginas en el tejido de las redes sociales como **Facebook** y **Google+**. Al insertar ciertas etiquetas que describen tu página le proporcionas funcionalidades que permiten convertir a tu sitio en un objeto que puede ser usado en perfiles sociales, fuentes de contenido o para conectar usuarios[^1].

El protocolo OpenGraph es el corazón del *tejido social*[^2] de Facebook; los usuarios solo tienen que preocuparse por sus conexiones. Gracias a que este gigante de las redes sociales hizo público este protocolo, todos podemos beneficiarnos de lo que ofrece.

Permite entre otras cosas establecer la página como un objeto y asignarle propiedades para describirlo. Por ejemplo, podemos describir una página como un artículo y asignarle características como título, autor, etc. Pero también podemos crear un «evento» y describir sus característica como horario, ubicación participantes.

Gracias al poder que proporciona [Genesis Framework][gen] podemos controlar de manera granular la descripción de los contenidos de nuestra web y así las redes sociales no tendrán que *adivinar* las propiedades del objeto que compartimos. De esta manera, podremos indicarle a Facebook o a Goolge+[^3] qué queremos compartir y cómo queremos que se visualice.

![El Protocolo OpenGraph](/media/20131128/opengraph.png "El Protocolo OpenGraph")

### OpenGraph con Genesis Framework

La primera acción de nuestro código es agregar al *hook*, es determinar el gancho donde vamos a *"colgar"* nuestro código. Ya que las propiedades OpenGraph son meta-descripciones (es decir, que describen propiedades del documento), deben colocarse en el encabezado, antes del cierre de la etiqueta `head`. Por eso el gancho o *hook* a utilizar es `wp_head`, a donde colgamos la función `cyberia_opengraph` con una ponderación de 15 (a menor ponderación más importancia).

La definición de la función `cyberia_opengraph` funciona solo con las entradas individuales, de ahí que solo se active con la condicional `is_single()`, puedes crear un conjunto de propiedades para la portada, pero en este ejemplo, las entradas individuales son suficientes.

Las propiedades tienen títulos claros en inglés. Y estos son los que utilizamos en esta función:

- `og:title` es el título del objeto, y usamos `the_title_attribute( 'echo=0' )`, es decir, el título del nuestra entrada.
- `og:site_name` es el nombre de nuestro sitio. Yo utilizo el nombre del blog y la descripción. No necesito una función, así que escribo la dirección directamente.
- `og:type` indica el tipo de objeto, en mi caso siempre es artículo[^4], `article` porque debe ser en inglés.
- `og:url` es el *permalink* de tu artículo, toca usar la función `get_permalink()`. Uso `get_permalink` porque devuelve la URL simplemente, `the_permalink` devuelve un enlace y el texto de anclaje, por lo que no sirve para OpenGraph.
- `og:description` usamos el contenido de la descripción en la sección SEO (recuerda que [Genesis Framework][gen] incorpora potentes características SEO y no requiere de plugins adicionales. La función entonces es `genesis_get_custom_field( '_genesis_description' )`.
- `og:locale` es el idioma en el que se comparte y se interactúa con el objeto. En mi caso es `es_LA` que corresponde al Español de Latinoamérica[^5].
- `og:image` corresponde a la imagen que acompaña al objeto. En el caso de Cyberia.MX es una buena práctica agregar a cada artículo una imagen destacada, y usamos la función `genesis_get_image (array('format'=>'url', 'size'=>'cyberia_home'))` para mostrar la miniatura que queremos. La opción es que el sitio que usa nuestro objeto elija la primera imagen que encuentre y eso no siempre es conveniente.
- `og:image:width` y `og:image:height` establecen las dimensiones de la miniatura, de modo que tenemos un absoluto control sobre lo que mostramos.

Aquí tienes el código completo de la función `cyberia_opengraph`:

```language-php
/**
 * Function cyberia_opengraph
 *
 * Adiciona la meta información que usa OpenGraph
 *
 * @author Javier Sanchez
 * @link http://cyberia.mx
 *
 * @param none
 * @return opengraph metadata
 */
add_action ('wp_head', 'cyberia_opengraph', 15);
function cyberia_opengraph () {
  if ( is_single () ) { ?>
    <meta property="og:title" content="<?php echo the_title_attribute( 'echo=0' ); ?>" />
    <meta property="og:site_name" content="Cyberia.MX - Cyberia es Internet... Internet es tu mundo" />
    <meta property="og:type" content="article" />
    <meta property="og:url" content="<?php echo get_permalink(); ?>"/>
    <meta property="og:description" content="<?php echo genesis_get_custom_field( '_genesis_description' ); ?>" />
    <meta property="og:locale" content="es_LA" />
    <meta property="og:image" content="<?php echo genesis_get_image (array('format'=>'url', 'size'=>'cyberia_home')); ?>" />
    <meta property="og:image:type" content="image/jpeg" />
    <meta property="og:image:width" content="200" />
    <meta property="og:image:height" content="200" />
  <?php }
}
```

Cuando compartimos este contenido en Facebook o en Google+ observarás que usan nuestras propiedades OpenGraph y se muestra lo que nosotros establecimos. Así controlamos cómo se comparte y como ven los usuarios de las redes sociales a nuestro sitio.

![OpenGraph en Google+](/media/20131128/opengraph_google_plus-595x400.png "OpenGraph en Google+")

![OpenGraph en Facebook](/media/20131128/opengraph_facebook.png "OpenGraph en Facebook")

!!! notice "Usa Genesis Framework"
    [Genesis][gen] te facilita contruir rápida y fácilmente increíbles sitios web con WordPress. No importa si eres un principiante o un desarrollador avanzado, [Genesis][gen] te proporciona una base segura y optimizada para los motores de búsqueda con la que puede llegar a extremos que no son posibles usando solo WordPress. Es muy simple -- **!Empieza a usar hoy mismo [Genesis Framework][gen]!**
   
[gen]: http://ito.mx/genesis

[^1]: El concepto de OpenGraph es muy amplio y puedes consultarlo en su propio sitio [http://ogp.me](http://ogp.me)

[^2]: En realidad Facebook no lo llama *tejido social* sino **"social graph"**, pero como podrás comprobar en la imagen que acompaña a este artículo, la red es un tejido vivo, cambiante.

[^3]: Hasta donde he podido comprobar, las propiedades de OpenGraph también son utilizadas por la red Google+.

[^4]: Por supuesto que hay muchos [tipos de objetos](http://ogp.me/#types) definidos por OpenGraph.

[^5]: Por ejemplo para España sería `es_ES` que corresponde al Castellano.


