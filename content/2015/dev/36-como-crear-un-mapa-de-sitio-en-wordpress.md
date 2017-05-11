Title: Cómo crear un mapa de sitio en WordPress
Date: 2013/12/27 02:38
Category: Desarrollo 
Tags: genesiswp, templates, php, hooks, sitemap, wordpress
Slug: como-crear-un-mapa-de-sitio-en-wordpress
Author: Javier Sanchez Toledano
Summary: 

Una forma de mejorar el SEO de nuestro sitio es creando un mapa de su contenido. Este mapa del sitio no solo ayuda a los buscadores a descubrir nuestro contenido, también ayuda a los visitantes en este descubrimiento. Con [Genesis Framework][gen] crear un mapa de sitio es muy fácil.

¿Ya conoces el [Archivo Cyberia.MX](http://cyberia.mx/archivo)? Contiene todas las páginas publicadas, la lista de categorías, de autores (aunque por el momento solo aparezco yo) y los 100 post más recientes. Esta página usa una plantilla personalizada que contiene el código que produce el resultado. Lo único que hice fue crear una página y seleccionar la plantilla `Archivo`. Eso fue suficiente para tener mi mapa del sitio tal como la ves.

En este tutorial para [Genesis Framework][gen] veremos cómo crear una página de archivo y al mismo tiempo vamos a revisar detalladamente las etiquetas de plantillas de WordPress relacionadas con el archivo.
Crear un plantilla de página

Como vimos en el artículo anterior sobre _cómo crear una portada personalizada_ vimos que para crear una plantilla de página (en inglés _Template Page_) lo único que necesitamos es insertar el comentario `Template Name: Archivo`, pero para mejorar la legibilidad de nuestro código, agregamos comentarios adicionales. Veamos la primera parte del código:

    <?php
     /**
       * Template Name: Archivo
       * Esta plantilla crea un mapa del sitio.
       *
       * @category Cyberia
       * @package  Plantilla
       * @author   Cyberia.MX
       * @license  http://www.opensource.org/licenses/gpl-license.php GPL v2.0 (or later)
       * @link     http://cyberia.mx/tag/genesiswp
       **/

Realmente solo es necesario incluir el contenido de la línea 3, pero el resto del código nos proporciona información importante y nos permite utilizar documentadores de código como por ejemplo [phpDocumentor](http://www.phpdoc.org/) o [apigen](http://apigen.org/).

### Eliminar y agregar acciones de los hooks en Genesis WordPress

Los _hooks_ son “ganchos” de los que colgamos acciones en [Genesis Framework][gen], lo que nos permite crear fragmentos de código y contenido y colocarlos en cualquiera de los _hooks_ que define [Genesis Framework][gen].

Esto nos permite crear nuestro sitio web como si fuera un figura hecha con bloques de lego, y las posibilidades son verdaderamente inmesas. Poco a poco iremos descubriendo en esta serie todas las posibilidades de los _hooks_.

En [Genesis Framework][gen] existen **¡51 hooks!** lo que nos permite controlar todo nuestro sitio, pero en nuestra plantilla de página solo vamos a utiliza el _hook_ `genesis_post_content`. Este hook controla la salida del contenido del post o página y si existe la imagen destacada, pero dentro del div `#content`.

Primero vamos a desactivar del _hook_ la acción preprogramada por [Genesis Framework][gen] y que llama a la función interna `genesis_do_post_content`. Para desactivar esta acción usamos la función `remove_action`, que tiene dos parámetros: el primero es el _hook_ y el segundo es la acción o función que colgamos en el _hook_:
    
    :::php
    /** Desactivar la acción preprogramada por Genesis Framework **/
    remove_action( 'genesis_post_content', 'genesis_do_post_content' );     

La siguiente actividad es agregar una acción a este mismo _hook_. Recuerda que las acciones son funciones cuya salida se coloca en ese “gancho”, así que procura darle a tu acción/función un nombre que te ayude a comprender para qué existe.

Tenemos que usar la función `add_function` que tiene dos parámetros obligatorios y un tercero opcional: el primero es el nombre del _hook_, el segundo es el nombre de la acción/función que colgamos a dicho _hook_ y el tercero, que es opcional, es la prioridad (si más de una acción está colgada al mismo _hook_ se coloca primero la acción de prioridad más baja); en nuestro _hook_ esta acción es la única, por lo que agregar prioridades resulta ocioso.

    :::php
    add_action( 'genesis_post_content', 'cyberia_mapa_de_sitio' );

Llamamos a la acción `cyberia_mapa_de_sitio` porque va a producir el contenido de nuestro mapa del sitio, lo que ayudará a los visitantes y a los motores de búsqueda a descubrir y recorrer todo nuestro sitio.

### Acciones que crean contenido en Genesis Framework

La acción `cyberia_mapa_de_sitio` es una función que creará el contenido en nuestro sitio. Va a crear la lista de categorías, la lista de archivos por meses, la lista de autores y una lista con los 100 artículos más recientes.

Lo primero que hacemos es crear la función y cerrar el código PHP para mezclar el código con etiquetas HTML.
 
    :::php
    function cyberia_mapa_de_sitio() { ?>

A partir de este punto y hasta el cierre de la función mezclaremos las etiquetas del HTML y el código PHP.

#### Lista de Páginas

La salida de esta función se muestra en dos columnas. Cada columna está englobada en una capa con el estilo que permite visualizarlas una a lado de la otra.

    :::PHP
    <div class="archive-page">
       <h4>Páginas</h4>
       <ul>
         <?php wp_list_pages( 'title_li=' ); ?>
       </ul>

La función `wp_list_pages`[^1] muestra una lista de páginas con sus enlaces, toma varios argumentos en un arreglo, pero nosotros solo vamos a utilizar `title_li` sin ningún valor, para producir una salida de elementos englobada entre etiquetas `<ul> </ul>`. 

<p class="alert">Al final de este artículo encontrarás enlaces a todas las funciones utilizadas.</p>

#### Lista de Categorías

    :::php
    <h4>Categorías</h4>Lista de Categorías

    <h4>Categorías</h4>
    <ul>
        <?php wp_list_categories( 'sort_column=name&title_li=' ); ?>
    </ul>

Con este fragmento de código, mostramos la lista de categorías, usando la función `wp_list_categories`[^2], y damos como argumentos que ordene la lista usando el nombre, es decir, por orden alfabético con `sort_column=name` y que no agrega nada a los elementos de la lista con `title_li=`.

    :::php
    <ul>
        <?php wp_list_categories( 'sort_column=name&title_li=' ); ?>
    </ul>

#### Archivos Mensuales

La tercera sección de nuestra columna corresponde a los archivos mensuales. Aquí presentamos un enlace que lleva a cada mes que contenga artículos en nuestro blog, una de las muchas formas de presentar información que nos proporciona [Genesis Framework][gen] y WordPress.

    :::php
    <h4>Archivos Mensuales</h4>
      <ul>
        <?php wp_get_archives( 'type=monthly' ); ?>
      </ul>

    </div><!-- end .archive-page-->

La función utilizada es `wp_get_archives`[^3] y le indicamos en el parámetro que nos muestre los archivos mensuales con `type=monthly`.

Con esta sección cerramos la primera columna.

#### Lista de los archivos de un blog

La columna de la derecha contiene la lista de los 100 artículos más reciente de este blog, e inicia con la capa que forma la segunda columna de nuestro mapa de sitio.

    :::php
    <div class="archive-page">

       <h4>Artículos Recientes</h4>
       <ul>
         <?php wp_get_archives( 'type=postbypost&limit=100' ); ?>
       </ul>

     </div><!-- end .archive-page-->

En esta sección volvemos a hacer uso de la función `wp_get_archives`[^3] pero ahora con diferentes argumentos.

* **`type=postbypost`**. Significa que muestre los artículos o posts enlistados por el título del post
* **`limit=100`**. Establecemos el límite de artículos que queremos mostrar. En el caso de Cyberia.MX mostramos los 100 artículos más recientes.

### Cierre de una plantilla en Genesis Framework

Para terminar nuestra plantilla llamamos al motor de nuestro blog. No tenemos que agregar encabeza, pie de página, barras laterales o códigos adicionales. [Genesis Framework][gen] colocará la salida de nuestra acción en el lugar adecuado, es decir en el gancho o _hook_ que especificamos.

    :::php
    <?php
    }
    
    genesis();

Este es un ejemplo sencillo de la potencia que nos proporciona [Genesis Framework][gen].

### Código completo, plantilla Archivo

Aqui tienes el código completo de la plantilla.

    :::php
    <?php
     /**
       * Template Name: Archivo
       * Esta plantilla crea un mapa del sitio.
       *
       * @category Cyberia
       * @package  Plantilla
       * @author   Cyberia.MX
       * @license  http://www.opensource.org/licenses/gpl-license.php GPL v2.0 (or later)
       * @link     http://cyberia.mx/tag/genesiswp
       **/

     /** Desactivar la acción preprogramada por Genesis Framework **/
    remove_action( 'genesis_post_content', 'genesis_do_post_content' );
    add_action( 'genesis_post_content', 'cyberia_mapa_de_sitio' );

    /**
     * Esta función produce como salida un mapa del sitio en un esquema de dos
     * columnas, con etiquetas, categorías, archivos mensuales, autores y los archivos más recientes.
     */

    function cyberia_mapa_de_sitio() { ?>

      <div class="archive-page">

        <h4>Páginas</h4>
        <ul>
          <?php wp_list_pages( 'title_li=' ); ?>
        </ul>

        <h4>Categorías</h4>
        <ul>
          <?php wp_list_categories( 'sort_column=name&title_li=' ); ?>
        </ul>

        <h4>Archivos Mensuales</h4>
        <ul>
          <?php wp_get_archives( 'type=monthly' ); ?>
        </ul>

      </div><!-- end .archive-page-->

      <div class="archive-page">

        <h4>Artículos Recientes</h4>
        <ul>
          <?php wp_get_archives( 'type=postbypost&limit=100' ); ?>
        </ul>

      </div><!-- end .archive-page-->

    <?php
    }

    genesis();

!!! alert-info "Usa Genesis Framework"
    [Genesis][gen] te facilita contruir rápida y fácilmente increíbles sitios web con WordPress. No importa si eres un principiante o un desarrollador avanzado, [Genesis][gen] te proporciona una base segura y optimizada para los motores de búsqueda con la que puede llegar a extremos que no son posibles usando solo WordPress. Es muy simple -- **!Empieza a usar hoy mismo [Genesis Framework][gen]!**

[gen]: http://conxb.com/genesismx

[^1]: `wp_list_pages`: http://codex.wordpress.org/Function_Reference/wp_list_pages
[^2]: `wp_list_categories`: http://codex.wordpress.org/Template_Tags/wp_list_categories
[^3]: `wp_get_archives`: http://codex.wordpress.org/Template_Tags/wp_get_archives
