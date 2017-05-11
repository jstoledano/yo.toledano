Title: Imágenes Destacadas en Genesis Framework  
Date: 2014/04/20 12:59  
Category: Desarrollo  
Tags: GenesisWP, thumbnail, images, WordPress
Summary: Un repaso rápido sobre cómo usar las imágenes destacadas en Genesis Framework.  

Me doy cuenta que debo de recuperar mi competencia para, no digamos crear temas, simplemente para usar día a día Framework de WordPress [__Genesis__][gen]. Así que voy a escribirme un tutorial sobre cómo usarlo y espero que a ustedes también les ayude.

## Imágenes destacadas en WordPress
Las imágenes destacadas, cuyo nombre es _featured images_ fueron agregadas a la versión 2.9 de WordPress, junto con otra característica complementaria, las __imágenes miniatura__ o _post thumbnail_[^1]. Estas miniaturas son muy usadas en los temas tipo _magazine_ o de películas para mostrar los carteles, por ejemplo.

Esta característica de _post thumbnail_ proporciona una forma estandarizada de mostrar una imagen de una forma bastante económica; antes se requería que se agregara la imagen en un campo personalizado, lo que hacía muy tediosa esta actividad; o peor aún se usaban _script_ que sobrecargaban el servidor o eran presa fácil de los _crackers_.

Afortunadamente [Genesis Framework][gen] proporciona una forma fácil de utilizar esta importante característica.

### Código para utilizar imágenes destacadas

Primero, debemos asegurarnos que en nuestro archivo `functions.php` exista soporte para esta función. Esto hará que se agregué el cuadro de dialogo a la interface del Escritorio.

    :::PHP
    add_theme_support( 'post-thumbnails' );

Esta función habilita la interface para imágenes destacadas, tanto en las entradas tipo _Post_ como en las tipo _Page_. Si solo necesitas las imágenes destacadas en un solo tipo de entrada, entonces tendrías que usar algo como esto:

    :::PHP
    add_theme_support( 'post-thumnails', array( 'post' );
    add_theme_support( 'post-thumnails', array( 'page' );

Simplemente elimina la línea que no desees.

Lo siguiente que debemos hacer es especificar las dimensiones de las imágenes miniatura. Aquí tenemos dos opciones: redimencionarla o _box-resizing_ y recortarla o _hard-cropping_.

La redimención o __box-resizing__ significa que se cambia o reduce el tamaño de la imagen __sin perder proporción__, es decir, sin distorcionarla hasta que _"quepa"_ dentro de la caja que especificaste en los parámetros. Imagina que es una caja de pizza y tienes que reducir el tamaño de la imagen hasta que quepa en la caja, si cabe en lo ancho, pero no en lo lago, debes seguir reduciendo. Po ejemplo, si tienes una imagen de 100&times;50 y una caja de 50&times;50, la imagen se reducirá a la mitad en ambas dimensiones, es decir quedará en 50&times;25. La imagen es más pequeña pero cabe en la caja. Si quieres que la imagen solo se ajuste del ancho, por ejemplo, en el parámetro de altura colocamos un valor tipo 9999 o algo así de imposible de alcanzar.

    :::PHP
    set_post_thumbnail_size( 50, 50 );

La segunda opción es el recorte o __hard-cropping__. En esta modalidad, la imagen se recorta hasta alcanzar las dimensiones especificadas _exactamente_. La ventaja es que obtienes exactamente lo que pediste. Si pides una miniatura de 50&times;50 obtienes una miniatura de 50&times;50. La desventaja es que tu imagen será recortada (ya sea de ambos lados o de arriba y abajo) para alcanzar el tamaño especificado, y perderás una parte de tu imagen.

    :::PHP
    set_post_thumbnail_size( 50, 50, true );

Ahora que hemos habilitado las imágenes en miniatura, ya podemos usar la en nuestra plantilla.

### Cómo usar miniaturas en una plantilla

Existen varias funciones relacionadas con las miniaturas o __thumbnails__ y las veremos a continuación.

- `has_post_thumbnail()`; regresa cierto o falso para indicar si la entrada actual tiene una imagen destacada.

        :::PHP
        <?php
          if ( has_post_thumbnail() ) {
            // el código que deseamos
          } else {
            // otra cosa
          }
        ?>


- `the_post_thumbnail()`; devuelve la imagen destacada, si existe:

        :::PHP
        <?php the_post_thumbnail(); ?>

Estas son las funciones básicas. En el siguiente artículo de la serie, veremos algunas de las funciones avanzadas.



!!! alert-info "Usa Genesis Framework"
    [Genesis][gen] te facilita construir rápida y fácilmente increíbles sitios web con WordPress. No importa si eres un principiante o un desarrollador avanzado, [Genesis][gen] te proporciona una base segura y optimizada para los motores de búsqueda con la que puede llegar a extremos que no son posibles usando solo WordPress. Es muy simple.  
    **!Empieza a usar hoy mismo [Genesis Framework][gen]!**


[gen]: http://j.mp/genesismx

[^1]: En esto de WordPress hay que usar los nombres en inglés porque así se llaman también las funciones que usan.
