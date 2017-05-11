Title: Configurar PostgreSQL en Heroku
Date: 2014/01/12 01:42
Category: Desarrollo
Tags: heroku, webdev, cloud, postgresql, paas
Slug: configurar-postgresql-en-heroku
Author: Javier Sanchez Toledano
Summary:

Vimos en un [artículo anterior](http://j.mp/ns-nitro01) como configurar nuestro entorno de trabajo para desarrollar una aplicación de Django en [Nitrous.IO][nitro]. Ahora vamos a crear una base de datos en PostgreSQL usando la plataforma gratuita que proporciona [Heroku][heroku].

__[Heroku][heroku]__ es una plataforma de servicios de cómputo (en inglés se llaman PaaS: _Plataform As A Service_) basada en Ubuntu que soporta distintos lenguajes de programación y proporciona herramientas de desarrollo en distintos niveles, desde el gratuito hasta el de alto desempeño.

Para el proyecto __Krypton__ vamos a crear una base de datos en PostgreSQL y la vamos a conectar con nuestra aplicación desarrollada en [Nitrous.IO][nitro], aunque por la fortaleza de la plataforma podemos usarla en otros proyectos, no solo en los desarrollados en Django.

## Cómo crear una base de PostgreSQL en Heroku

Lo primero que tienes que hacer es ir a [Heroku PostgreSQL](http://j.mp/ns-psql-heroku) y crear una cuenta:

![Heroku PostgreSQL](https://dl.dropboxusercontent.com/u/1090580/nspace/201401/nitro02-01-heroku.png)

Inscribirse es gratis y tendrás un servidor de base de datos PostgreSQL gratuito, aunque limitado a 10 mil registros. Para el desarrollo de nuestro proyecto eso es suficiente, cuentan con un plan básico que solo cuesta 9 dólares mensuales, aunque hay servicios bastante robustos para soportar cualquier tipo de carga, incluso las aplicaciones más pesadas.

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

Así que elegimos el plan de desarrollador que es gratuito y agregamos una base de datos.

![Plan Dev](https://dl.dropboxusercontent.com/u/1090580/nspace/201401/nitro02-02-heroku.png)

Se crea con esto una base de datos con un nombre aleatorio pero único. Si quieres cambiarle el nombre para que te sea más fácil tienes que irte al menú Apps,

![Menu Apps](https://dl.dropboxusercontent.com/u/1090580/nspace/201401/nitro02-04-heroku.png)

Ahí verás la lista de tus aplicaciones, selecciona la que acabas de crear,

![Lista de Apps](https://dl.dropboxusercontent.com/u/1090580/nspace/201401/nitro02-05-heroku.png)

Una vez dentro del panel de control de tu aplicación, selecciona el menú _Settings_ dónde verás la opción para cambiar el nombre en _Rename_.

![Rename](https://dl.dropboxusercontent.com/u/1090580/nspace/201401/nitro02-06-heroku.png)

De regreso a tu base de datos, dentro del panel de control de tu base de datos, encontrarás ahí los datos necesarios para conectarnos desde nuestra aplicación. Toma nota de ellos.

![Datos de conexión](https://dl.dropboxusercontent.com/u/1090580/nspace/201401/nitro02-07-heroku.png)

Para facilitarnos la vida, vamos a colocar estos datos dentro de nuestro entorno en [Nitrous.IO][nitro], y una forma es colocarlas en variables de entorno, dentro de nuestro archivo `.bashrc`

    export KRYPTON_DATABASE_HOST=exxxxxxxxxxxxxx.amazonaws.com
    export KRYPTON_DATABASE_NAME=dxxxxxxxxxxxxxxj
    export KRYPTON_DATABASE_USER=gxxxxxxxxxxxxxxn
    export KRYPTON_DATABASE_PASS=8xxxxxxxxxxxxxxU
    export KRYPTON_DATABASE_PORT=5432

Para usarlos en Django, por ejemplo, tendríamos que asegurarnos que tenemos en nuestro archivo `settings.py` el módulo `os` y tomar estos datos del entorno.

    import os

    DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'HOST': os.environ[KRYPTON_DATABASE_HOST],
            'NAME': os.environ[KRYPTON_DATABASE_NAME],
            'USER': os.environ[KRYPTON_DATABASE_USER],
        'PASSWORD': os.environ[KRYPTON_DATABASE_PASS],
            'PORT': 5432,
      }
    }

Y listo, ya tenemos una base de datos PostgreSQL, en [Heroku][heroku], una plataforma de servicios que contribuirá al éxito de nuestro proyecto.

[nitro]: http://j.mp/ns-nitro
[heroku]: http://j.mp/ns-heroku
