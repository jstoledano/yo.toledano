Title: Configuración de Nginx y WordPress
Date: 2014/01/19 03:25
Category: Desarrollo 
Tags: nginx, wordpress 
Slug: configuracion-de-nginx-y-wordpress
Author: Javier Sanchez Toledano
Summary: 

Pues resulta que cambiar al servidor Nginx fue más fácil de lo que pensaba. [Nginx][nginx], que se pronuncia algo así como _engine x_ o sea "motor x" en inglés es un servidor web, un proxy inverso, y un proxy de correo escrito por Igor Sysoev. Es muy famoso porque funciona en sitios gigantes de Rusia, como Yandex, el buscador; Mail.Ru, un servidor de correo; además lo utilizan sitios de alto tráfico como Netflix y WordPress.

Según sitios especializados, Nginx tiene el 15% de la cuota de mercado de servidores y tiene una acelerada tendencia a la alza.

## Nginx y yo

Había intentado antes usar otros servidores web que hicieran funcionar este sitio y el finado `xxx.xx` de forma más eficiente, había intentado con Cherokee Project (que funciona muy bien con Django, pero no pude agregarle soporte para PHP),  con LiteSpeed server (pero no pude hacer funcionar el certificado de seguridad y no pude compilar PHP). Yo sé, es mi culpa.

Y entonces decidí probar con Nginx y me llevé una sorpresa. Al principio su configuración me parecía un poco críptica, pero después la entendí y ahora me parece bastante lógica y coherente. Y el rendimiento es supremo: no solo es más rápido que Apache2, también es más fácil la gestión de contenido estático, el cache del sitio, la ejecución de PHP es acelerada y es facilísimo instalar certificados de seguridad.

## Nginx y WordPress

En realidad la configuración funciona para cualquier sitio que necesite WordPress, pero escribo mi experiencia ahora que regrese a WordPress y [Genesis Framework][genesis] en mi blog personal [**Yo, Toledano**](http://yo.toledano.org)[^1].

### Desinstalación de Apache2

En mi servidor venía instalado `apache2` como servidor, pero no lo iba a ocupar. Intenté desinstalarlo, pero me apareción extraños mensajes acerca de que se iban a desinstalar otros paquetes. Y es que en Ubuntu, `apache2` pertenece al grupo `base` como requisito. Si lo quietaba, pues intentaba desinstalar todo el grupo base y pues no.

Entonces decidí desactivarlo. Simplemente no iba a arrancar automáticamente, solo cuando yo lo hiciera manualmente. Para desactivar el servicio utilicé este comando:

    update-rc.d -f  apache2 remove
    

### Instalación de Nginx

Nginx utiliza una variación de FastCGI con PHP que es más eficiente que la implementación original llamada `php-fpm` que significa en inglés *FastCGI Process Manager* que tiene algunas características que lo hacen sobresalir, por ejemplo:

* Los procesos se crean bajo demanda
* Estadísticas básicas
* Gestión de procesos avanzada con paradas y arranques en caliente (_graceful stop/start_)
* Habilidad para iniciar _workers_ con diferentes usuarios, grupos, entornos, etc.
* Registro en las bitácoras estándar del sistema
* y muchas más…

Entonces necesitamos instalar precisamente el paquete `nginx` y el paquete `php-fpm`:

    sudo apt-get install nginx php5-fpm

Ubuntu se encargará además de instalar todas las dependencias necesarias para que ambos programas se ejecuten adecuadamente. Ambos programas instalan servicios que podemos parar, arrancar o revisar con el comando `service`:

    sudo service nginx start
    sudo service php-fpm stop

## Configuración de Nginx

Ahora vamos a ver como configurar un dominio con Nginx para que funcione con WordPress. Y vamos a ver que es eso de proxy inverso.

Vamos a crear un archivo en la siguiente ruta:

    /etc/nginx/sites-availabe/wordpress.conf
    
donde colocaremos la configuración de nuestro sitio. Al colocarlos ahí quedan disponibles (como su nombre lo dice) y se activan hasta que colocamos un enlace en el directorio `sites-enable`.

### Sobre el dominio

Primero vamos a configurar el dominio, le vamos a indicar a Nginx que escuhe peticiones para ese dominio y en que puerto va a escuchar.

    server {
        listen 80;
        server_name example.com;

        client_max_body_size 200m;

        root /ruta/hacia/mis/archivos;
        index index.php index.html index.htm;
    }


Esta es la primera parte de nuestro archivo de configuración. Veamos las opciones utilizadas detalladamente. **Todas las líneas termina con punto y coma `;`**.

* **`listen`**:  
ser refiere al puerto de escucha. El puerto estándar es el 80, o el 443 si utilizas certificados de seguridad, en cualquier caso, aquí especificas el número de puerto.
* **`server_name`**:  
simplemente colocamos el nombre del dominio.
* **`client_max_body_size`**  
habilita al servidor de responder con contenido de gran tamaño. 
* **`root`**  
indica la ruta donde se encuentran los archivos, recuerda que la ruta debe ser completa.
* **`index`**  
indica que archivo debe devoler Nginx cuando no se solicita ninguno. Va a enviar el primero si existe, si no intenrará con el segundo, sino con el tercero, etc.

### Compresión de salida

Comprimir la salida de nuestro sitio es una buena práctica, no solo ahorra ancho de banda, sino que es más rápida la respuesta porque los archivos son más pequeños, lo que resulta en una mejor experiencia para el usuario. Esta es la configuración para la compresión dentro del grupo `server`[^2].

    gzip on;
    gzip_disable "msie6";
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_buffers 16 8k;
    gzip_http_version 1.1;
    gzip_types text/plain text/css application/json application/x-javascript text/xml application/xml application/xml+rss text/javascript

Algunas líneas debemos revisarlas con más detalle: `gzip on` activa la compresión. La línea `gzip_disable` dice para Internet Explorer 6 no debe funcionar. La última línea nos dice que tipos de archivos debe comprimir. No cambies los valores propuestos a menos que de verdad sepas lo que estás haciendo.


### Ubicaciones

Ahora, igualmente dentro del grupo `server` vamos a crear subgrupos para definir ubicaciones dentro del servidor y su comportamiento. Veamos una ubicación, llamada `location` por Nginx y analicemos su contenido.

Podría parecer que las expresiones regulares son muy difíciles pero ya existe mucha información y ejemplos en la red, así que no debe ser complicado encontrar una regla para nuestras situaciones más comunes.

    location ~ \.php$ {
        try_files $uri =404;
        fastcgi_pass unix:/var/run/php5-fpm.sock;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }
    
**`location`**   
Indica el comportamiento de la `location` definida a continuación. En este caso la regla es `~`, una expresión regular que indica cualquier coincidencia, respetando mayúsculas. La segunda regla es `\.php$` que significa que aplica a todos los archivos cuya terminación sea `.php`.  
  
  A continuación abrimos un subgrupo donde indicaremos cuál será el comportamiento dentro de la regla que acabamos de definir.   
  
* **`try_files`**: dice que intente encontrar el archivo y si falla, que lance un error 404.
* **`fastcgi_pass`**: indica la ubicación del servidor `fastcgi`. Usar _sockets_  es más eficiente que usar servidores de red.
* **`fastcgi_index`**: Nos dice cuál es el archivo por default para esta ubicación y 
* **`fastcgi_param`** nos dice con qué parámetros debemos llamar al procesador FastCGI.
   
Entonces ya definimos qué hacer con los archivos `.php`. Veamos otro ejemplo.
    
### Especificar el cache de navegación

Google[^3] recomienda para mejorar el desempeño de los sitios web que ciertos tipos de archivo deben enviarse tal cual son, sin agregarles _cookies_ e indicando cuando expira ese contenido, de modo que si el navegador lo tiene en su cache, utilice ese archivo en vez de descargarlo.

Vamos a crac otro conjunto de reglas, ahora aplicables a esos archivos que queremos acelerar, los iconos, imágenes, archivos de hojas de estilo, JavaScript y archivos de fuentes.

    location ~* \.(?:ico|css|js|gif|jpe?g|png|ttf|woff)$ {
      access_log off;
      expires 30d;
      add_header Pragma public;
      add_header Cache-Control "public, mustrevalidate, proxy-revalidate";
    }
    
Las reglas definidas para estos archivos dicen que deben enviarse los encabezados `Pragma public` y `Cache-Control`.   `access_log` dice que el acceso a estos archivos no se registre en las bitácoras; `expires` dice que el navegador debe guardar esos archivos por 30 días antes de solicitarlos de nuevo.

### Permalinks de WordPress

El siguiente conjunto de reglas, es el más simple y activan los permalinks en WordPress. En realidad es una sola regla muy simple, pero toral para nuestro sitio.

    location / {
      try_files $uri $uri/ /index.html;
    }

WordPress procesa los permalinks  con el archivo índice atrapando los errores 404. En  `apache` cuando llamamos a un post de WordPress con permalink _bonito_ se produce un error 404 porque dicho post no existe físicamente en le servidor, entonces WordPress atrapa el error y manda la solicitud al archivo `index.php` que lo procesa  adecuadamente.

Con Nginx pasa exactamente lo mismo, solo que la regla dice:
    
    try_files $uri $uri/ /index.html;
    
intenta enviar la solicitud, si fallas, manda el índice de la ubicación (que en nuestro caso es precisamente `index.php`) y si eso falla, manda el archivo `índex.html`.

Es decir, al usar _pretty permalinks_ siempre nos quedaremos en la segunda opción y todo funcionará como se espera.

### Otras reglas para WordPress

Las siguientes dos reglas nos dicen que hacer con los archivos `robots.txt` y `favicon.ico`, simplemente no registramos los accesos a esos archivos y no lanzamos mensajes de error si no están presentes.

  location = /robots.txt  { access_log off; log_not_found off; }
    location = /favicon.ico { access_log off; log_not_found off; }

La última ubicación que vamos a definir es la del error 500, por si falla el servidor, los visitantes vean algo mejor que el indescifrable mensaje de error de Nginx.

    error_page 500 502 503 504 /500.html;
    location = /500.html {
      root /siempre/uso/la_misma/ruta/assets/;
    }

## Proxy reversible, ¿qué pokemón es ese?

En el modelo tradicional cliente/servidor que conocemos gracias al popular servidor Apache, cuando un visitante hace una solicitud a nuestro navegador, la solicitud es procesada por Apache.

Nginx funciona como un intermediario entre el servidor y los visitantes, lo que nos da pauta a tratar de forma más eficiente la respuestas que entregamos a los usuarios.

Por ejemplo, Nginx se encarga de los archivos estáticos, por lo que no son una carga para la aplicación. Comprime la salida antes de enviarla a los visitantes, y evita que la aplicación tenga que hacerlo. Podemos balancear la carga de nuestra aplicación, ejecutando una copia de la aplicación e indicado a Nginx que la use cuando sea necesario. Puede manejar cache de la aplicación, respondiendo rápidamente con las copias almacenadas sin tener que llamar a la aplicación. Entre otras cosas.

Nginx es tan eficiente como proxy reversible, que incluso se puede utilizar como intermediario entre el exterior y *el propio servidor Apache*. 

Al hacer que Nginx se encargue de la comunicación con el exterior, nuestra aplicación se encarga de una sola cosa, sin administrar cargas adicionales.

## El archivo completo

Aquí te presento el archivo completo para que lo utilices en tu propio servidor, solo tienes que hacer unos pequeños ajustes para indicar tu servidor `server_name` y la raíz de tu sitio `roto`.

    server {
      ##
      # Datos del Servidor - tienes que ajustarlo
      ##
      listen 80;
      server_name example.com;     
      root /la/ruta/a/tu/sitio;

      ##
      # No cambiar a partir de este punto hasta error 500
      ##
      index index.php index.html index.htm;
      client_max_body_size 4G;
      
      ##
      # Procesar archivos .php con php-fpm
      ##
      location ~ \.php$ {
        try_files $uri =404;
        fastcgi_pass unix:/var/run/php5-fpm.sock;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
      }  

      ##
      # Archivos estáticos
      ##
      location ~* \.(?:ico|css|js|gif|jpe?g|png|ttf|woff)$ {
        access_log off;
        expires 30d;
        add_header Pragma public;
        add_header Cache-Control "public, mustrevalidate, proxy-revalidate";
      }

      ##
      # Permalinks bonitos para WordPress
      ##
      location / {
        try_files $uri $uri/ /index.html;
      }

      ##
      # No registrar robots.txt y favicon.ico
      ##
      location = /robots.txt { access_log off; log_not_found off; }
      location = /favicon.ico { access_log off; log_not_found off; }

      ##
      # Compresión de archivos
      ##
      gzip on;
      gzip_disable "msie6";
      gzip_vary on;
      gzip_proxied any;
      gzip_comp_level 6;
      gzip_buffers 16 8k;
      gzip_http_version 1.1;
      gzip_types text/plain text/css application/json application/x-javascript text/xml application/xml application/xml+rss text/javascript

      ##
      # Páginas de error 500
      ##
      error_page 500 502 503 504 /500.html;
      location = /500.html {
        root /siempre/uso/la/misma/ruta/;
      }
    }



[nginx]: http://j.mp/ns-nginx
[genesis]: http://j.mp/ns-genesis

[^1]: Y de la mano de Amy Lee Adams, como podrán ustedes apreciar.

[^2]: Esto quiere decir que debe estar **dentro** de las llaves que engloban todas las configuraciones de `server`.

[^3]: En inglés [*Leverage Browse Caching*](http://j.mp/ns-cache-browsing)
