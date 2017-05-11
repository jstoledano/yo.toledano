Title: Tutorial de metadatos con MetaBox
Date: 2013/12/26 20:05
Category: Desarrollo 
Tags: meta-box, custom-fields, genesiswp, wordpress
Slug: tutorial-de-metadatos-con-metabox
Author: Javier Sanchez Toledano
Summary: 

WordPress tiene la habilidad de crear permitir a los autores asignar campos personalizados, llamados *custom fields*, a una entrada. Esta información se conoce como **metadatos**, es decir, información sobre otra información.

Pueden ser los datos de un libro que estés leyendo (título, autor, editorial, edición, reseña), sobre una película (título, director, actores, resumen), sobre tu estado de ánimo (humor: feliz), sobre la música que estés escuchando (Ahora suena: Dream On de Aerosmith).

Claro que pueden contener información mucho más compleja, siempre en pares clave/valor. De hecho, los metadatos están planeados para aplicaciones de microformatos, esquemas de datos como Rich Snippets de Google u OpenGraph de Facebook.

Pero si en tu sitio utilizas siempre el mismo conjunto de campos personalizados, tener que elegirlos o escribirlos, cada vez que publicas un artículo, el proceso de vuelve muy poco eficiente. La solución son las **MetaBoxes** (su traducción sería MetaCajas) que son un conjunto de campos personalizados agrupados para su conveniencia en la pantalla de escritura de WordPress. Una vez que se ha definido una metabox, esos metadatos están a tu disposición para ser usados en cualquier post o página de tu sitio de WordPress.

Veamos un ejemplo simple. En los artículos publicados en Cyberia.MX[^1] aparece en la parte superior, una leyenda en letras blancas, que llamamos *SEOTexto*, utilizada para darle relevancia a las páginas en los buscadores y sean más fácilmente encontradas por los usuarios. Este SEOTexto esta compuesto por dos partes, un texto corto que funciona como título y una línea rápida e informativa. Muchos sitios implementan este tipo de técnicas, pero se imaginan tener que seleccionar los campos personalizados cada vez que publiques un artículo, corres el riesgo de olvidar algún campo personalizado.

[^1]: En este momento no hay ningún ejemplo vivo de un sitio con esta funcionalidad.

La solución en Cyberia.MX fue crear una metabox con esos dos campos personalizados para facilitar su captura y los campos los utilizo en las entradas individuales para crear el SEOTexto.

Para facilitar la creación de las metaboxes, seleccione a la mejor biblioteca de funciones disponible para WordPress, que es la creada por *Dimas Begunoff* de **Far in Space** llamada [**WPAlchemy**](http://conxb.com/wp-alchemy).

Una vez que lo has descargado, copia los archivos al directorio de tu child-theme, porque recuerda que no debes modificar directamente el [Framework Genesis][gen].

[gen]: http://conxb.com/genesismx

Ahora coloca una llamada a esta función en tu archivo `functions.php`, al principio del archivo:

    :::PHP
    include_once CHILD_DIR . '/lib/wpalchemy/MetaBox.php';

Son dos archivos, pero este que estamos llamando es la biblioteca de la clase y el otro, que se llama `MediaAccess.php` es el que proporciona los medios para manipular los controles, que veremos en un artículo posterior, de nivel avanzado.

Ahora necesitamos crear una clase para nuestro SEOTexto, y lo hacemos de esta manera:

    :::PHP
    $ficha = new WPAlchemy_MetaBox(array (
     'id' => '_ficha',
     'title' => 'Texto Seo',
     'template' => CHILD_DIR . '/lib/textoseo/ficha.php',
     'types' => array('post'),
     'context' => 'normal',
     'prefix' => 'seo_',
     'mode' => WPALCHEMY_MODE_EXTRACT )
    );

En este fragmento de código, creamos una ficha, de clase `WPAlchemy_MetaBox`, la identificamos como `_ficha`. Para no interferir con otros espacios de nombre, este identificador debe ser único. Le asignamos un título y nombramos una plantilla que usará nuestra metabox, indicamos en `types` que será usado en artículos (en un ejemplo más avanzado, crearemos una metabox para un tipo personalizado).

Otra clave importante es `prefix`, que identifica a nuestra caja, y también debe ser único para que no interfiera con otros espacios de nombres. Lo que sigue es crear la plantilla que decimos en la declaración de la clase que vamos a utilizar. La ficha de SEOTexto solo tiene dos campos, así que es una plantilla muy sencilla.

    :::PHP
    <div class="ficha_tecnica">
     <p>
     El texto que aparece en la parte superior de la página, mejora en gran medida la forma en la que Google indexa las páginas, <br />
     de ahí la necesidad de colocar adecuadamente un texto rico en palabras clave.
     </p>

     <?php /** Título SEO, va en H1 con formato especial **/ ?>
     <label>Título SEO <span>(<em>incluir la palabra clave</em>)</span></label>
     <p>
     <input type="text" name="<?php $metabox->the_name('seo_title'); ?>" value="<?php $metabox->the_value('seo_title'); ?>" />
     <span>Escribe el título SEO con la palabra clave principal. Ejemplo: <strong>Angry Birds para iPod</strong></span>
     </p>

     <?php /** Texto SEO, en una sola línea **/ ?>
     <label>Texto SEO <span>(<em>con palabras clave secundarias</em>)</span></label>
     <p>
     <input type="text" name="<?php $metabox->the_name('seo_text'); ?>" value="<?php $metabox->the_value('seo_text'); ?>" />
     <span>Escribir texto descriptivo en una sola línea con palabras clave secundarias <strong>Un divertido juego de estrategia para dispositivos iPod</strong></span>
     </p>

     <div style="clear: both;"></div>

    </div>

Básicamente es un formulario que contiene dos campos y sus etiquetas. Lo importante son los valores `name` y `value` que sirve para identificar los valores que cambian en cada entrada, por eso, permitimos que los maneje la propia clase `metabox`.

**`the_name`** es la función de la clase `metabox` que asigna y recupera la clave `seo_text` y `the_value` de la misma clase, asigna y recupera el contenido del par. Este código produce como salida la metabox en la pantalla de escritura de WordPress.

!!! alert-info "Usa Genesis Framework"
    [Genesis][gen] te facilita contruir rápida y fácilmente increíbles sitios web con WordPress. No importa si eres un principiante o un desarrollador avanzado, [Genesis][gen] te proporciona una base segura y optimizada para los motores de búsqueda con la que puede llegar a extremos que no son posibles usando solo WordPress. Es muy simple -- **!Empieza a usar hoy mismo [Genesis Framework][gen]!**
