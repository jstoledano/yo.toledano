Title: Layout al azar en WordPress
Date: 2013/11/28 21:59
Category: Desarrollo 
Tags: filtros, genesiswp, nivelbasico, wordpress
Slug: layout-al-azar-en-wordpress
Author: Javier Sanchez Toledano
Summary: 

Como una prueba de concepto, más que algo verdaderamente útil en producción, esta función nos ayuda a cambar el _layout_ (o la estructura de la página en WordPress) al azar.

Lo que hace primero es tomar un número al azar entre uno y dos, que son las opciones que se programaron, aunque evidentemente puede tener cualquier cantidad de opciones, pero bueno, para empezar, dos son suficiente.

A continuación, asigna uno de los dos _layout_ dependiendo del número que haya salido en la función `random`.

```language-php
/**
  * Funcion Cyberia Layout
  * @name cyberia_layout
  * @author Sanchez Toledano
  * @link http://namespace.mx
  *
  * @param $opt - el layout del sitio
  * @return $opt - el nuevo layout
  */
add_filter('genesis_pre_get_option_site_layout', 'cyberia_layout');
function cyberia_layout($opt) {
  if ( rand(1,2)==2 ) :
    $opt = 'sidebar-content';
  else:
    $opt = 'content-sidebar';
  endif;
  return $opt;
}
```

Como verán, la función es muy simple y cada vez que se recarga la página se genera un nuevo _layout_. Esto al final resulta cansado para el visitante y por eso es solo un concepto.

!!! alert-info "Usa Genesis Framework"
    [Genesis][gen] te facilita contruir rápida y fácilmente increíbles sitios web con WordPress. No importa si eres un principiante o un desarrollador avanzado, [Genesis][gen] te proporciona una base segura y optimizada para los motores de búsqueda con la que puede llegar a extremos que no son posibles usando solo WordPress. Es muy simple -- **!Empieza a usar hoy mismo [Genesis Framework][gen]!**
   
[gen]: http://ito.mx/genesis

