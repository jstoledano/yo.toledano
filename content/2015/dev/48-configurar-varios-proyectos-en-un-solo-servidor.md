Title: Configurar varios proyectos en un solo servidor
Date: 2014/01/16 03:52
Category: Desarrollo 
Tags: nginx, webdev 
Slug: configurar-varios-proyectos-en-un-solo-servidor
Author: Javier Sanchez Toledano
Summary: 

Listos para lanzar nuestro **proyecto krypton** en producción vamos a crear el
sitio en el servidor dónde se ejecuta este mismo sitio, es decir que
[namespace.mx](https://namespace.mx) y
[criptomonedas.com.mx](http://criptomonedas.com.mx) estarán en el mismo
servidor.

Vamos a crear tanto para el _proyecto namespace_ como para el _proyecto
krypron_ un entorno virtual, un arrancador **gunicorn**, un controlador en
**supervisor** y un sitio para el servidor **nginx**.

Primero creamos el entorno virtual `krypton` y lo activamos.

    mkvirtualenv krypton
    workon krypton

Ahora vamos a instalar los requisitos de la aplicación, que ya habíamos generado en [Nitrous.IO](http://conxb.com/ns.nitro).

    pip install - r requisitos.txt

## Configuración de Gunicorn

El siguiente paso es configurar `gunicorn`. [Gunicorn](http://conxb.com/ns-gunicorn) es un servidor de aplicaciones especializado para Python que es intermediario entre el servidor web exterior y el proyecto en Django.

Se instala para cada proyecto, usando `pip`:

    pip install gunicorn

A continuación vamos a crear el archivo `gunicorn_start` para cada proyecto, en la ruta `entorno/bin/`, por ejemplo para el proyecto krypton, esta es la ruta: `/home/krypton/entornos/krypton/bin/gunicorn_start` y ahí colocamos las variables de entorno que ocupa nuestro proyecto. Este es el contenido para el **proyecto krypton**.

    :::Bash
    #!/bin/bash
    NAME="krypton" # Nombre de la aplicación
    DJANGODIR=/home/javier/proyecto_krypton/krypton # Directorio del proyecto
    SOCKFILE=/home/javier/proyecto_krypton/run/krypton.sock # activamos la comunicación con el servidor via socket
    USER=javier # el usuario que ejecuta el proyecto
    GROUP=javier # el grupo al que pertenece el proyecto
    NUM_WORKERS=3 # cuantos workers vamos a desplegar

    echo "Starting $NAME as `whoami`"

    # Activamos el entorno virtual
    cd $DJANGODIR
    source /home/javier/entornos/krypton/bin/activate
    export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
    export PYTHONPATH=$DJANGODIR:$PYTHONPATH

    # Creamos las variables del entorno de producción
    export KRYPTON_DATABASE_HOST='exxxxxxxxxxxx4-27.compute-3.amazonaws.com'
    export KRYPTON_DATABASE_NAME='dxxxxxxxxxxxxj'
    export KRYPTON_DATABASE_PORT='5432'
    export KRYPTON_DATABASE_USER='gxxxxxxxxxxxxn'
    export KRYPTON_DATABASE_PASS='8xxxxxxxxxxxxU'

    export NITRO_SECRET_KEY='*oxxxxxxxxxxxxxxxxg'
    export DJANGO_SETTINGS_MODULE='krypton.settings.produccion'
    export DJANGO_WSGI_MODULE=krypton.wsgi # WSGI module name

    # Creamos el directorio de ejecucion
    RUNDIR=$(dirname $SOCKFILE)
    test -d $RUNDIR || mkdir -p $RUNDIR

    # Arrancamos el servidor gunicorn
    # Los programas controlados por supervisor no deben ejecutarse como demonios (--daemon)
    exec /home/javier/entornos/krypton/bin/gunicorn ${DJANGO_WSGI_MODULE}:application --name $NAME --workers $NUM_WORKERS --user=$USER --group=$GROUP --log-level=debug --bind=unix:$SOCKFILE

El archivo `gunicorn_start` debe tener permisos de ejecución, así debemos cambiarle los permisos con el siguiente comando:

    chmod 755 gunicorn_start

### El controlador supervisor

[Supervisord](http://conxb.com/ns-supervisor) es un programa que permite controlar y supervisar la ejecución de programas en Linux.

Para instalarlo debemos usar `apt-get` en sistemas basados en Debian o el instalador que que te corresponda. También debemos asegurarnos que se está ejecutando.

    sudo apt-get install supervisor
    sudo service supervisor start

Ahora debemos crear los archivos para supervisar las aplicaciones, que tiene el siguiente formato:

    [program:krypton]
    command = /home/javier/entornos/krypton/bin/gunicorn_start ; Que programa ejecutamos
    user = javier ; El usuarios que lo ejecuta
    stdout_logfile = /home/javier/proyecto_krypton/logs/gunicorn_supervisor.log ; La bitacora
    redirect_stderr = true

A continuación debemos hacer que `supervisor` lea los archivos:

    sudo supervisorctl reread

Luego hay que activarlo:
    
    sudo supervisorctl update
    sudo supervisorctl start krypton

## Configuración de Nginx

Es es un servidor web, que ha resultado una excelente alternativa a Apache2, el tradicional servidor de la web. La configuración no podría ser más diferente que la de Apache, pero aún así es basten sencilla, una vez que comprendes como funciona.

Nginx va a funcionar como un intermediario entre el exterior y nuestra aplicación. Es decir, un visitante solicita una página a `nginx` y este a su vez se la solicita a `gunicorn` usando _sockets_ que es una forma muy rápida de comunicación entre procesos.

Este sistema tiene tres ventajas muy grandes: el interior (es decir, nuestra aplicación) nunca está expuesta al exterior, la aplicación solo entrega la parte dinámica del sitio, y tercero `nginx` es muy eficiente entregando contenido estático lo que resta carga a la aplicación.

<div style="max-width:360px; margin: 25px auto;">
<!-- cyberia.336x289.01.top -->
<ins class="adsbygoogle"
style="display:inline-block;width:336px;height:280px"
data-ad-client="ca-pub-9466828947698623"
data-ad-slot="8590866557"></ins>
<script>
(adsbygoogle = window.adsbygoogle || []).push({});
</script>
</div>
<div style="clear:both;"></div> 

Este es el archivo del proyecto krypton, ubicado en el directorio `/etc/nginx/sites-available`:

    upstream krypton_app_server {
      server unix:/home/javier/proyecto_krypton/run/krypton.sock fail_timeout=0;
    }

    server {
      # Escucha del servidor
      listen 80;
      server_name criptomonedas.com.mx;

      # Compresión de archivos
      gzip              on;
      gzip_buffers      16 8k;
      gzip_comp_level   4;
      gzip_http_version 1.0;
      gzip_min_length   1280;
      gzip_types        text/plain text/css application/x-javascript text/xml application/xml application/xml+rss text/javascript image/x-icon image/bmp;
      gzip_vary         on;

      # Bitácora y registro de errores
      access_log //home/javier/proyecto_krypton/logs/nginx-access.log;
      error_log /home/javier/proyecto_krypton/logs/nginx-error.log;

      # Contenido estático
      location /assets/ {
        alias /home/javier/proyecto_krypton/krypton/assets/;
        expires 1y;
        log_not_found off;
      }

      location /media/ {
        alias /home/javier/proyecto_krypton/krypton/media/;
        expires 1y;
        log_not_found off;
      }

      location / {
        # No se que sea, pero si tiene una entrada en Wikipedia debe ser importante
        # http://en.wikipedia.org/wiki/X-Forwarded-For
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        # pasa el encabezado Host a krypton para que funcione 
        # la redirección correctamente.
        proxy_set_header Host $http_host;

        # Y para que nginx no haga osos con la redirecciones,
        # que al cabo ya esta arriba que onda
        proxy_redirect off;

        # Hacemos que los archivos estáticos los sirva nginx 
        # por lo que no pasamos esas solicitudes a krypton
        if (!-f $request_filename) {
          proxy_pass http://krypton_app_server;
          break;
        }
      }

      # Error 500 - Si uso la misma en todos mis proyectos
      error_page 500 502 503 504 /500.html;
      location = /500.html {
        root /home/javier/proyecto_namespace/namespace/assets/;
      }
    }

Luego lo ponemos como sitio habilitado:

    sudo ln -s /etc/nginx/sites-available/krypton.conf /etc/nginx/sites-enable/03krypton

El enlace se llama `03krypton` solo por cuestión de orden, hay otros sitios en mi servidor y se cargan de forma ordenada. 

Ahora solo tenemos que reiniciar el servidor y nuestro sitio estará listo.

    sudo service nginx restart

Y ya está completamente operativo el blog __Criptomonedas__. 

