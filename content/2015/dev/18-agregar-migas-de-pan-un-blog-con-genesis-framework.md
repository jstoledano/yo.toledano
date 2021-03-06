Title: Agregar migas de pan a un blog con Genesis Framework
Date: 2013/11/21 16:45
Category: Desarrollo 
Tags: php, filtros, wordpress, genesiswp
Slug: agregar-migas-de-pan-un-blog-con-genesis-framework
Author: Javier Sanchez Toledano
Summary: 

Crear temas con el [Framework Genesis](http://ito.mx/genesis) es realmente fácil. Es como jugar con bloques de lego y solo tenemos que agregar los bloques que necesitamos.

Por ejemplo, si queremos agregar migas de pan a nuestras páginas, algo que favorece el enlazamiento interno, solo tenemos que agregar el siguiente código al archivo `functions.php`:

```language-php
/**
 * Corrije la migajitas de pan.
 *
 * @author Javier Sanchez Toledano
 * @link http://namespace.mx
 *
 * @param array $args Los argumentos para las migajitas
 * @return array Las migajitas corregidas
 */
add_filter( 'genesis_breadcrumb_args', 'cyberia_breadcrumb_args' );
function cyberia_breadcrumb_args( $args ) {
    $args['home']               = 'Portada';
    $args['sep']                = ' &#8594; ';
    $args['labels']['prefix']   = 'Aqui estás: ';
    $args['labels']['author']   = 'Archivo de ';
    $args['labels']['category'] = 'Archivo de '; // A partir de Genesis 1.6
    $args['labels']['tag']      = 'Archivo de ';
    $args['labels']['date']     = 'Archivo de ';
    $args['labels']['search']   = 'Buscando ';
    $args['labels']['tax']      = 'Archivo de ';
    $args['labels']['404']      = 'No encontrado: '; // A partir de Genesis 1.5
    return $args;
}    
```

!!! notice "Necesitas Genesis Framework"
    Para poder ejecutar este código, necesitas contar con [Genesis Framework](http://ito.mx/genesis). 
