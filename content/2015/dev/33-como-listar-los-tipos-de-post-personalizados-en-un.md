Title: Como listar los tipos de post personalizados en un mapa de sitio de WordPress
Date: 2013/12/07 03:47
Category: Desarrollo 
Tags: genesiswp, wp_query, php, wordpress 
Slug: como-listar-los-tipos-de-post-personalizados-en-un
Author: Javier Sanchez Toledano
Summary: 

Ayer estaba revisando la página de archivo que vimos en el artículo anterior [Cómo crear un mapa de sitio en WordPress con Genesis Framework](http://conxb.com/19sblkG) y me di cuenta de algo: a la lista de artículos recientes le faltan las entradas personalizadas.

Más allá de si son pocas o no, se espera que en esa lista estén los 100 artículos más recientes, no solo los que tienen el tipo *post*. Lo que ocurre es que la función que usamos `wp_get_archives( 'type=postbypost&limit=100' );` trabaja solo con este tipo de artículos.

Para solucionar este problema vamos a escribir una consulta que nos muestre exactamente lo que queremos y vamos a modificar nuestra página de archivo con esta función.

El truco lo hace la función `WP_Query`[^1], tal como lo veremos a continuación.

[^1]:A mi entender, [`WP_Query`](http://j.mp/cyberia-wpquery) es la función más potente de WordPress y le vamos a dedicar muchos artículos para poder comprenderla y dominarla.

Lo primero que vamos a hacer es definir los argumentos para nuestra función:

```language-php
<?php
  $args=array(
    'post_type' => array( 'post','peliculas', 'libros', 'apps'),
    'post_status' => 'publish',
    'posts_per_page' => 100,
  );
```

En la línea 3, vemos un arreglo que indica los tipos de artículos que vamos a mostrar. En el arreglo incluímos todos nuestros tipos personalizados y al propio tipo post, quedando así: `array( 'post','peliculas', 'libros', 'apps')`.

La línea 4 determina que solo se enlisten los artículos que hayan sido publicados, para evitar que se muestren los borradores, por ejemplo: `'post_status' => 'publish',`.

La línea 5 establece el número de artículos que vamos a mostrar: `100`, con el argumento `post_per_page`.

Esos tres argumentos son suficientes para asegurar que tenemos todos los tipos de artículos en nuestro mapa de sitio.

Estos argumentos los pasamos a la función, primero creando una variable que contendrá el objeto[^2] que devuelve `WP_Query` y a continuación creado dicho objeto.

[^2]: Los loops creados con `WP_Query` son objetos y accedemos a sus propiedades almacenadas en la variable respectiva.

~~~language-php
$my_query = null;
$my_query = new WP_Query($args);
~~~

A continuación tenemos un *loop* al que recorreremos una y otra vez hasta agotar la respuesta. Usaremos para hacer la lista, solo el título y el permalink de los artículos, como vemos a continuación.

~~~language-php
if( $my_query->have_posts() ) {
    while ($my_query->have_posts()) : $my_query->the_post(); ?>
      <li><a href="<?php the_permalink() ?>" rel="bookmark" title="Enlace permanente a <?php the_title_attribute(); ?>"><?php the_title(); ?></a></li>
      <?php
    endwhile;
  }
  wp_reset_query();  
?>
~~~

Cerramos nuestro código restaurando los datos globales que usamos con `the_post()`.

Mira el código completo:

```language-php
<?php
  $args=array(
    'post_type' => array( 'post','peliculas', 'libros', 'apps'),
    'post_status' => 'publish',
    'posts_per_page' => 100,
  );
  $my_query = null;
  $my_query = new WP_Query($args);
  if( $my_query->have_posts() ) {
    while ($my_query->have_posts()) : $my_query->the_post(); ?>
      <li><a href="<?php the_permalink() ?>" rel="bookmark" title="Enlace permanente a <?php the_title_attribute(); ?>"><?php the_title(); ?></a></li>
      <?php
    endwhile;
  }
  wp_reset_query();  
?>
```

Este código debe reemplazar en nuestra plantilla de archivo la línea 47, y tendremos una salida como la que puedes ver en nuestro archivo[^3].

[^3]: En realidad ya no existe el archivo de Cyberia.MX

!!! alert-info "Usa Genesis Framework"
    [Genesis][gen] te facilita contruir rápida y fácilmente increíbles sitios web con WordPress. No importa si eres un principiante o un desarrollador avanzado, [Genesis][gen] te proporciona una base segura y optimizada para los motores de búsqueda con la que puede llegar a extremos que no son posibles usando solo WordPress. Es muy simple -- **!Empieza a usar hoy mismo [Genesis Framework][gen]!**
   
[gen]: http://ito.mx/genesis
