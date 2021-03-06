Title: El poder de los filtros en Genesis Framework
Date: 2013/11/21 16:07
Category: Desarrollo 
Tags: php, filtros, genesiswp , wordpress
Slug: el-poder-de-los-filtros-en-genesis-framework
Author: Javier Sanchez Toledano
Summary: 

Les quiero hablar un poco acerca de los *Rich Snippets*, pero antes les voy a contar como usar los filtros para ampliar las funcionalidades básica de [Genesis Framework](http://ito.mx/genesis).

Para poder vincular mi sitio a Google Plus, necesitaba agregar a mi perfil de autor un enlace a mi perfil de Google+, sin embargo aunque escribía correctamente el código, este no se imprimía en la página.

La razón: [Genesis Framework](http://ito.mx/genesis) filtra algunas etiquetas html que pueden ser consideradas inseguras. La solución burda era insertar el enlace al final de la página, por ejemplo, usando un *hook*:

```php
add_action ('genesis_after_endwhile', 'cyberia_author_gplus');
function cyberia_author_gplus() { 
  if ( is_author() ) {
    $google_profile = get_the_author_meta( 'google_profile' ); ?>
    <div class="gplus">
      <p>El perfil del autor en <a rel="me author" href="<?php echo esc_url( $google_profile ); ?>/about?rel=author">
      <img class="plus" src="http://ssl.gstatic.com/images/icons/gplus-16.png" width="16" height="16" border="0" align="">
      <strong>Google+</strong></a></p>
    </div>
<?php }
}
```

Esta función inserta el enlace que toma del perfil del autor y lo inserta al final del *loop*, y de hecho, aparece después de la navegación.

Una solución mucho más elegante y que además va con la filosofía de Genesis es usar **filtros** para modificar el comportamiento de las funciones.

Existe una función llamada `genesis_formatting_allowedtags()` que devuelve un arreglo con las etiquetas que están permitidas, y lo que vamos a hacer es agregar la propiedad `rel=` al arreglo de la etiqueta `a`.

```php
add_filter ('genesis_formatting_allowedtags', 'cyberia_filter_author_description', 5, 1);
function cyberia_filter_author_description ($intro_text) {
  $genesis_formatting_allowedtags['a'] = array( 'href' => array(), 'title' => array(), 'rel'=> array(), );
  return $genesis_formatting_allowedtags;
}   
``` 

Primero llamamos al filtro para que sea aplicado a `genesis_formatting_allowedtags` y el filtro lo que hace es modificar el *array*. Y esta función hace que el enlace a Google Plus sea correcto.
