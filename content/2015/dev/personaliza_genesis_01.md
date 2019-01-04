Title: Personalizar Genesis
Date: 2015-08-09 12:46:18 a.m.
Category: Desarrollo
Tags:  wordpress, genesis, php
Author: Javier Sanchez Toledano
Summary:

Aunque lo más recomendable es hacerlo mediante un _plugin_ para conservar los cambios a través de temas y versiones, la forma original (y que sigue en uso) es usar el archivo `functions.php` y esa es la forma en la que voy a presentar las modificaciones a este tema.

El tema que usa este sitio es [**Agency Pro**][agency] un tema que utiliza [**Genesis Framework**][genesis] para funcionar. Aprovecha todas las ventajas del nuevo marcado `HTML5` y tiene una presentación realmente diferente a lo que nos tenía acostumbrado _StudioPress_.

<!--more-->

Las modificaciones que hice incluyen el cambio de tipografía, el uso de la versión más reciente de _jQuery_, modificaciones a los estilos de diversos elementos como `pre` y `code` y por supuesto, _transparencias_, muchas transparencias.

## Registro de Scripts

Para reemplazar la versión de _jQuery_ que usa WordPress, primero debemos eliminar del registro[^1] de guiones la versión _oficial_ y registrar la que nosotros queremos, dentro del archivo `functions.php`

De modo que agregamos una acción a la fila de carga de guiones y ahí eliminamos del registro la versión actual, registramos la nueva y la colocamos en la fila[^2].

    :::php
    /* *** jQuery 2.1.1 *** */
    add_action( 'wp_enqueue_scripts', 'jQuery211', 99);
    function jQuery211() {
      wp_deregister_script( 'jquery' );
      wp_register_script( 'jquery', '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js' );;
      wp_enqueue_script( 'jquery', '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js', array( 'jquery' ), '2.1.1', false );
    }

Esta función crea unn grupo de _scripts_ llamado `jQuery211` que contiene un solo _script_: `jquery.min.js` en su versión `2.1.1`.

Usando el mismo gancho `wp_enqueue_scripts`, agregamos otros _scripts_ que son necesarios para la música. En esta ocasiones, nos aseguramos que solo estén disponibles en las entradas individuales.

    :::php
    add_action('wp_enqueue_scripts', 'estilos_toledanos');
    function estilos_toledanos() {
        if ( is_singular( 'post' ) ) {
              wp_enqueue_style('music', '/assets/css/xemusicplayer.css');
            wp_register_script('music', '/assets/js/jquery-xemusicplayer-1.0.0.min.js' );
             wp_enqueue_script('music', '/assets/js/jquery-xemusicplayer-1.0.0.min.js', true );
            wp_register_script('video', '//cdnjs.cloudflare.com/ajax/libs/fitvids/1.0.1/jquery.fitvids.min.js');
             wp_enqueue_script('video', '//cdnjs.cloudflare.com/ajax/libs/fitvids/1.0.1/jquery.fitvids.min.js', true);
        }
    }

## Registro de Estilos

El siguiente paso también ocurre en el archivo `functions.php` y consiste en  reemplazar la tipografía usada en el tema original que es [EB Garamond](https://www.google.com/fonts/specimen/EB+Garamond) por [__Lato__](https://www.google.com/fonts/specimen/Lato).

Para esto hay una función muy parecida a la anterior para anotar en la lista de estilos uno más: `wp_enqueue_style`:

    :::php
    wp_enqueue_style('google-fonts', '//fonts.googleapis.com/css?family=Lato:300,700,300italic,700italic|Spinnaker', array(), CHILD_THEME_VERSION);

Esta línea registra los estilos para las fuentes Lato y Spinnaker usados en el tema, pero debe usarse dentro del _hook_ `wp_enqueue_scripts`, por lo que debemos crear una función que lo haga.

    add_action('wp_enqueue_scripts', 'toledano_fuentes');
    function toledano_fuentes() {
        wp_enqueue_style('google-fonts', '//fonts.googleapis.com/css?family=Lato:300,700,300italic,700italic|Spinnaker', array(), CHILD_THEME_VERSION);
    }

El procedimiento de reemplazo de la tipografía requiere de un paso adicional en la hoja de estilos, pero eso lo haremos más adelante.

## Usar ganchos en Genesis Framework

Aprovechando que estamos en el archivo `functions.php` vamos a agregar unas cuantas cosas mas usando ganchos ya sea de WordPress o alguno de los más de 50 que nos proporciona [Genesis Framework][genesis].

### Agregar scripts a una página

Vamos a agregar un _script_ a nuestra página en la sección `head` y para ello vamos a utilizar el gancho (o _hook_) de WordPress `wp_head`:

    add_action('wp_head', 'toledano_adsense', 30);
    function toledano_adsense() {
      echo '<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>';
    }

### El gancho `genesis_before`

El gancho `genesis_before` se coloca inmediatamente después de la marca `body` y antes de cualquier contenido, y este punto es el que buscamos para insertar el siguiente guión de _Google Tag Manager_ [^3]:

    :::html
    add_action('genesis_before', 'toledano_tag_manager');
    function toledano_tag_manager() {?>
        <!-- Google Tag Manager -->
        <noscript>
        <iframe
          src="//www.googletagmanager.com/ns.html?id=xxx-xxxxxx"
          height="0"
          width="0"
          style="display:none;visibility:hidden"></iframe>
        </noscript>
        <script>
        (function(w,d,s,l,i){
          w[l]=w[l]||[];w[l].push({
            'gtm.start': new Date().getTime(),event:'gtm.js'
          });
          var f=d.getElementsByTagName(s)[0],
              j=d.createElement(s),
              dl=l!='dataLayer'?'&l='+l:'';
          j.async=true;
          j.src='//www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
        })
        (window,document,'script','dataLayer','xxx-xxxxxx');
        </script>
    <!-- End Google Tag Manager -->
    <?php }


## Filtros en Genesis Framework

Una de las características más poderosas[^4] de [Genesis Framework][genesis] son los filtros, que modifican muchas funciones. En este tema vamos a usar un filtro para cambiar el pie de página.

    add_filter( 'genesis_footer_creds_text', 'toledano_creds_text' );
    function toledano_creds_text() {
      echo '<div class="creds"><p>';
      echo '<a href="/blog/">Blog</a>';
      echo ' &middot; <a href="/archivo/" title="Mapa del Sitio">Mapa del Sitio</a> ';
      echo ' &middot; <a href="/politica/" title="Política de Privacidad">Aviso de Privacidad</a>';
      echo ' &middot; <a href="/contacto/" title="Formulario de Contacto">Contacto</a>';
      echo '</p><p>';
      echo 'Copyright &copy; ';
      echo date('Y');
      echo ' &middot; Tema <a href="/ir/agency"><strong>Agency Pro</strong></a> ';
      echo ' &middot; Funciona con <a href="/ir/genesis" title="Genesis Framework">Genesis Framework</a>';
      echo '</p></div>';
    }

Estas son todas las modificaciones que hice al archivo `functions.php`. Decía al principio que lo ideal era colocar estos cambios en un plugin, porque cuando se actualice el tema, lo que haya cambiado en el archivo se perderá, y en cambio, en una extensión, no pasaría eso. Otra ventaja adicional es que no importa que cambie de tema, los cambios se aplican desde el plugin y seguirían funcionando.

El día de mañana veremos los cambios en los estilos, que también son muy interesantes.

[agency]: /ir/agency
[genesis]: /ir/genesis

[^1]: En inglés hay una palabra para eso: _deregister_, sería algo así como _desregistrar_.  
[^2]: En realidad, dado que la función es `enqueue`, el verbo sería _encolar_, pero, obvio, nunca voy a usar tal aberración (aunque sea correcta).  
[^3]: El sistema de __Google Tag Manager__ es buenísimo y creo que no se conoce ni se usa ampliamente. Tendré que escribir sobre él para darlo a conocer.  
[^4]: Pero que casi nunca uso porque _¡no les entiendo!_
