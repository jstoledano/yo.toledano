Title: Cómo crear post relacionados sin usar plugins
Date: 2013/11/27 15:47
Category: Desarrollo 
Tags: genesiswp, php, wordpress 
Slug: como-crear-post-relacionados-sin-usar-plugins
Author: Javier Sanchez Toledano
Summary: 

Mucha gente cree que tener muchos _plugins_ provoca que el desempeño de un blog disminuya. En realidad no depende del número de extensiones, más bien de las acciones que lleven a cabo esos _plugins_. Un solo _plugin_ mal programado puede provocar un gran desastre en un blog. Usar extensiones o _plugins_ nos ahorra tiempo y facilita nuestra vida si no podemos conseguir el código necesario para realizar una acción específica.

Sin embargo, a veces es necesario prescindir de las extensiones, cuando no encontramos ninguna que satisfaga nuestras necesidades.

Por ejemplo, en Cyberia.MX trataba de agregar una lista de artículos relacionados para ofrecer a los lectores contenido relevante de acuerdo al tema que estuvieran leyendo. Hay un _plugin_ muy bueno llamado _RelatedPost_ de [René Ade](http://www.rene-ade.de/), que hace un excelente trabajo, pero debido a las características de este sitio no podía usar una de sus mejores funcionalidades: imágenes en la lista de artículos relacionados.

__Nick the Geek__ publicó este código en su sitio y funciona muy bien, por eso me permito publicarlo con las adaptaciones necesarias, por ejemplo, elimino de la comparación la etiqueta `code`, y ciertas categorías que ya no uso y no quiero que salgan en las recomendaciones.

Agrego además, mejoro un poco el atributo `title` para las imágenes y los enlaces, para darle un mejor servicio a los usuarios.

Lo primero que hace este código es verificar que sea un post individual, para que no se active en la portada, páginas o resultados de búsqueda.
A continuación, usando las etiquetas contenidas en el artículo actual hace una consulta para encontar otros posts que contengan estas mismas etiquetas. Se usa la función `WP_Query` para hacer esta consulta.

Esta función es muy potente, pero también muy compleja y usa un arreglo con los atributos de la consulta. En el caso de Cyberia.MX, agregamos los tipos de entradas personalizados _«libros»_, _«apps»_ y _«películas»_. Agregamos además un parámetro adicional para eliminar una etiqueta que no será usada en la búsqueda de relacionados. Los parámetros son `post_type` y `tag__not_in`, ambos reciben un _array_ con los valores que agregaremos a la consulta.

```language-php
'post_type'             => array( 'post', 'peliculas', 'libros', 'apps'),
'tag__not_in'           => array ( 70, ),
```

Otras características de esta consulta es el número de post que queremos que regrese como resultado (`showposts`), que ignore los post fijos (`ignore_sticky_posts`) y que ignore igualmente ciertos tipos de post que no serán usados en la consulta (`post-format-link`, `post-format-status`, `post-format-asides` y `post-format-quote`). Si en tu blog no usas estos formatos, puedes eliminar este _array_.

Con el resultado de la consulta, armamos la lista de imágenes y enlaces. Para las imágenes y los enlaces agregamos el atributo `title`, usando el título del artículo actual (`single_post_title`) y el título del artículo recomendado (`get_the_title`).

```language-php
$img = genesis_get_image() ? genesis_get_image(
  array( 'size' => 'cyberia_related',
   'attr' => array (title=>'Si te gustó &ldquo;'. 
    single_post_title('', false) .'&rdquo;, tal vez te pueda interesar «' . 
    get_the_title() . '»') )
  ) : '<img src="' . 
    get_bloginfo( 'stylesheet_directory' ) . 
    '/images/related.png" alt="Si te gustó &ldquo;'. 
    single_post_title('', false) .'&rdquo;, tal vez te pueda interesar «' . 
    get_the_title() . '»" />';
$related .= '<li><a href="' . get_permalink() . 
  '" rel="bookmark" title="Si te gustó &ldquo;'. 
  single_post_title('', false) .'&rdquo;, tal vez te pueda interesar «' . 
  get_the_title() . '»">' . $img . get_the_title() . '</a></li>';
```

Algo parecido usamos con las categorías, eliminando las categorías no usadas (`category__not_in`) y agregando el atributo title al resultado. Por último, la función regresa un resultado, solo si existen artículos relacionados.

```language-php
if ( $related ) {
  printf( '<div class="breadcrumb" id="related"><h3 class="related-title">Artículos Recomendados</h3><ul class="related-list">%s</ul></div>', $related );
}
```

Aquí tienen todo el código.

```language-php
add_action( 'genesis_after_post_content', 'cyberia_related_posts' );
/**
 * Outputs related posts with thumbnail
 *
 * @author Nick the Geek
 * @url http://designsbynickthegeek.com/tutorials/related-posts-genesis
 * @global object $post
 */

function cyberia_related_posts() {
  if ( is_single ( ) ) {
    global $post;
    $count = 0;
    $postIDs = array( $post->ID );
    $related = '';
    $tags = wp_get_post_tags( $post->ID );
    $cats = wp_get_post_categories( $post->ID );
    if ( $tags ) {
      foreach ( $tags as $tag ) {
        $tagID[] = $tag->term_id;
      } // foreach
      $args = array(
        'post_type'             => array( 'post','peliculas', 'libros', 'apps'),
        'tag__in'               => $tagID,
        'tag__not_in'           => array ( 70, ),
        'post__not_in'          => $postIDs,
        'showposts'             => 5,
        'ignore_sticky_posts'   => 1,
        'tax_query'             => array(
          array(
            'taxonomy'  => 'post_format',
            'field'     => 'slug',
            'terms'     => array(
              'post-format-link',
              'post-format-status',
              'post-format-aside',
              'post-format-quote' ), // terms
            'operator'  => 'NOT IN' 
          )
        ) //tax_query
      ); //args
      $tag_query = new WP_Query( $args );
      if ( $tag_query->have_posts() ) {
        while ( $tag_query->have_posts() ) {
          $tag_query->the_post();
          $img = genesis_get_image() ? genesis_get_image(
            array( 'size' => 'cyberia_related',
              'attr' => array (title=>'Si te gustó &ldquo;'.
                single_post_title('', false) .'&rdquo;, tal vez te pueda interesar «' .
                get_the_title() . '»') 
            ) 
          ) : '<img src="' .
            get_bloginfo( 'stylesheet_directory' ) .
            '/images/related.png" alt="Si te gustó &ldquo;'.
            single_post_title('', false) .'&rdquo;, tal vez te pueda interesar «' .
            get_the_title() . '»" />';
          $related .= '<li><a href="' . get_permalink() .
            '" rel="bookmark" title="Si te gustó &ldquo;'.
            single_post_title('', false) .'&rdquo;, tal vez te pueda interesar «' .
            get_the_title() . '»">' . $img . get_the_title() . '</a></li>';
          $postIDs[] = $post->ID;
          $count++;
        }
      } // if $tag_query
    } // $tags
    if ( $count <= 4 ) {
      $catIDs = array( );
      foreach ( $cats as $cat ) {
        if ( 3 == $cat )
          continue;
        $catIDs[] = $cat;
      } // foreach
      $showposts = 5 - $count;
      $args = array(
        'post_type'             => array( 'post','peliculas', 'libros', 'apps'),       
        'category__in'          => $catIDs,
        'category__not_in'      => array ( 1,4,72,34,236, ),
        'post__not_in'          => $postIDs,
        'showposts'             => $showposts,
        'ignore_sticky_posts'   => 1,
        'orderby'               => 'rand',
        'tax_query'             => array(
          array(
            'taxonomy'  => 'post_format',
            'field'     => 'slug',
            'terms'     => array(
              'post-format-link',
              'post-format-status',
              'post-format-aside',
              'post-format-quote' ),
            'operator' => 'NOT IN'
          ) // array tax_query in
        ) // tax_query
      ); // $args
      $cat_query = new WP_Query( $args );
      if ( $cat_query->have_posts() ) {
        while ( $cat_query->have_posts() ) {
          $cat_query->the_post();
          $img = genesis_get_image() ? genesis_get_image(
            array( 
              'size' => 'cyberia_related',
              'attr' => array (
                title=>'Si te gustó &ldquo;'.
                single_post_title('', false) .'&rdquo;, tal vez te pueda interesar «' .
                get_the_title() . '»'
              )
            ) 
          ) : '<img src="' . get_bloginfo( 'stylesheet_directory' ) .
           '/images/related.png" alt="Si te gustó &ldquo;'. single_post_title('', false) .
           '&rdquo;, tal vez te pueda interesar «' . get_the_title() . '»" />';
          $related .= '<li><a href="' . get_permalink() . '" rel="bookmark" title="Si te gustó &ldquo;'. single_post_title('', false) .'&rdquo;, tal vez te pueda interesar «' . get_the_title() . '»">' . $img . get_the_title() . '</a></li>';
        } // while $cat_query
      } // if $cat_query
    } // if $count ,= 4
    if ( $related ) {
      printf( '<div class="breadcrumb" id="related"><h3 class="related-title">Artículos Recomendados</h3><ul class="related-list">%s</ul></div>', $related );
    }
    wp_reset_query();
  } // if ( is_single() )
}
```

!!! alert-info "Usa Genesis Framework"
    [Genesis][gen] te facilita contruir rápida y fácilmente increíbles sitios web con WordPress. No importa si eres un principiante o un desarrollador avanzado, [Genesis][gen] te proporciona una base segura y optimizada para los motores de búsqueda con la que puede llegar a extremos que no son posibles usando solo WordPress. Es muy simple -- **!Empieza a usar hoy mismo [Genesis Framework][gen]!**
   
[gen]: http://ito.mx/genesis
