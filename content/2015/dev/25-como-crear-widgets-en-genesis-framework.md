Title: Cómo crear widgets en Genesis Framework
Date: 2013/11/27 14:38
Category: Desarrollo 
Tags: functionsphp, widgets, genesiswp, wordpress
Slug: como-crear-widgets-en-genesis-framework
Author: Javier Sanchez Toledano
Summary: 

¿Ya vieron el slider en la portada de Cyberia.MX? Es un plugin que se llama **Genesis Slider** y que puedes descargar desde el sitio de StudioPress o instalarlo desde el depósito de extensiones de WordPress. Este plugin solo funciona con el [Framework Genesis](http://ito.mx), por lo que se integra de forma totalmente transparente y no necesita ninguna librería adicional.

!!! alert-danger "Aviso"
    Cyberia.MX era un blog que ya no está activo y poco a poco su archivo está siendo trasladado a **namespace.mx**.

La cuestión es que crea un *widget* y se arrastra al área que quieras en el menú Apariencia -> Widgets de tu escritorio. ¡Pero yo no tenía un área de *widgets* dónde quería poner mi *slider*! Así que me dispuse a crear el área necesaria.

En realidad, lo que se crea se llama **sidebar**, aunque no sea una barra lateral y dentro de esta área se colocan los espacios para los *widgets*.

El primer paso es registrar la sidebar, agregando esta función en tu archivo `functions.php`:

```language-php
/*
 * Registro de la Sidebar
 ********************************************************** */
genesis_register_sidebar(
  array(
    'id'            => 'slider_sidebar',
    'name'          => 'Espacio para el Slider',
    'description'   => 'Crea un espacio para colocar el slider en la homepage.',
  )
);
```

El argumento de la función es un arreglo con tres claves que no deben faltar:

- **`id`**, es el identificador de tu sidebar y debe ser único para evitar conflictos con otros sidebars que hayas definido. 
- **`name`**, este es el nombre que vemos en la barra de widgets, te sirve para identificarlo visualmente. 
- **`description`**, este argumento es opcional, pero es una buena práctica incluirlo en tu código. 

El siguente paso es crear el área en el tema. En mi caso quiero que aparezca antes del contenido y solo en la portada. El gancho o *hook* en este punto se llama `genesis_before_loop`, así que ahí agrego el código.

```language-php
/*
 * Agregar la sidebar a la portada
 ********************************************************** */
add_action ('genesis_before_loop', 'cyberia_slider_sidebar');
function cyberia_slider_sidebar () {
  if ( is_home() ) {
    echo '<div class="slider_sidebar">';
      dynamic_sidebar( 'slider_sidebar' );
    echo '</div>';
  }
}
```

Agregamos la acción al gancho y colocamos ahí el resultado de nuestra función, que lo que hace es verificar que sea la portada, con `is_home()` y ahí agrega nuestra sidebar, con la función `dynamic_sidebar` y el nombre de la sidebar como argumento.

Por último agregamos un poco de estilo a nuestro widget, que es usando la clase `slider_sidebar`.

```language-css
/*
 * 42=. Slider Sidebar
 ********************************************************** */
.slider_sidebar {
  margin: 0 auto 25px;
}
```

Y eso es suficiente, ya podemos arrastrar nuestro widget, cualquiera, a esta sidebar que aparece solo en la portada antes del *loop*.

!!! alert-info "Usa Genesis Framework"
    [Genesis][gen] te facilita contruir rápida y fácilmente increíbles sitios web con WordPress. No importa si eres un principiante o un desarrollador avanzado, [Genesis][gen] te proporciona una base segura y optimizada para los motores de búsqueda con la que puede llegar a extremos que no son posibles usando solo WordPress. Es muy simple -- **!Empieza a usar hoy mismo [Genesis Framework][gen]!**
   
[gen]: http://ito.mx/genesis

