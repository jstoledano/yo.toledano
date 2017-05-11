Title: Configurar un blog con Zinna y Django en Nitrous.IO
Date: 2014/01/12 05:02
Category: Desarrollo
Tags: krypton, django, zinnia
Slug: configurar-un-blog-con-zinna-y-django-en-nitrousio
Author: Javier Sanchez Toledano
Summary:

Ya vimos como crear un [entorno de programación](http://j.mp/ns-nitro01) en [Nitrous.IO][nitro], ya [creamos nuesra base de datos PostgreSQL](http://j.mp/ns-nitro02) en [Heroku][heroku], por lo que estamos listos para crear nuestro blog. Antes de entrar de lleno con el blog, vamos a asegurar que nuestro entorno virtual cuenta con todos los requisitos para poder operar con él.

## Intalación de requisitos

Recuerda que tenemos un entorno virtual y por lo tanto, debe estar activado.

    :::Bash
    javier@krypton:~$ workon krypton
    /bin/bash: warning: setlocale: LC_ALL: cannot change locale (es_MX.UTF-8)
    /bin/bash: warning: setlocale: LC_ALL: cannot change locale (es_MX.UTF-8)
    (krypton)javier@krypton:~$

## La conexión con PostgreSQL

Ya que nuestra base de es PostgreSQL, vamos a instalar el módulo `psycopg2` que es el estándar para Django. Con nuestro entorno virtual activado, usamos `pip` para instalarlo.

    :::bash
    (krypton)javier@krypton:~$ pip install psycopg2
    Downloading/unpacking psycopg2
      Downloading psycopg2-2.5.2.tar.gz (685kB): 685kB downloaded
      Running setup.py egg_info for package psycopg2

    Installing collected packages: psycopg2
      Running setup.py install for psycopg2
        building 'psycopg2._psycopg' extension
        gcc -pthread -fno-strict-aliasing -DNDEBUG -g -fwrapv -O2 -Wall -Wstrict-prototypes -fPIC -DPSYCOPG_DEFAULT_PYDATETIME=1 -DPSYCOPG_VERSION="2.5.2 (dt dec pq3 ext)" -DPG_VERSION_HEX=0x090204 -DPSYCOPG_EXTENSIONS=1 -DPSYCOPG_NEW_BOOLEAN=1 -DHAVE_PQFREEMEM=1 -I/usr/include/python2.7 -I. -I/usr/include/postgresql -I/usr/include/postgresql/9.2/server -c psycopg/psycopgmodule.c -o build/temp.linux-x86_64-2.7/psycopg/psycopgmodule.o -Wdeclaration-after-statement

    [--- Luego de muchos otras líneas, llegamos al final ---]

    Successfully installed psycopg2
    Cleaning up...

Este módulo compila el controlador usando las librerías de PostgreSQL, que tienen que estar presentes, así como los programas de desarrollo, como `g++`, `make` y otros.

!!! alert-info "En Nitrous.IO tienes un entorno completo"
    Afortunadamente, en [Nitrous.IO] no tienes que preocuparte, porque tienes todos los programas y librerías instalados, así que olvídate de referencias incompletas.

## Zinnia, la elección del blog

En __namespace.mx__ el código del blog está escrito por mi completamente, pero la realidad es que no es el mejor y sobre todo porque reinventaba la rueda. Claro que el objetivo es aprender, y con ese mismo espíritu de aprendizaje es que ahora tomo un código profesional para avanzar en mi aprendizaje personal.

Entonces el blog elegido es __[Zinnia][zinnia]__. Se define como una aplicación extensible para administrar blogs. Y es bastante ligero, ya que como ellos mismos dicen, cualquier módulo que pudo ser manejado por otra aplicación se ha dejado de lado.

El autor de de Zinnia es el francés [Fantomas42](https://github.com/Fantomas42/) que ha hecho excelentes contribuciones a Python, además de Zinnia.

## Dependencias de Zinnia

Revisando las dependencias de Zinnia, vemos que necesitamos los módulos `Pyllow`, `django-mptt`[^1], `django-tagging` y `beautifulsoup4`. De forma opcional, enlista `pytz`, `South`, `pyparsing` y `django-xmlrpc`.

Para instalar estas dependencias más facilmente vamos a crear un archivo llamado `requirements.txt`[^2] con todos estos módulos.

Solo hay una acotación en esta lista. El módulo `Pyllow` tiene que ser instalado usando `easy_install`

# El proyecto Krypton

Ahora si, empezamos con el proyecto __krypton__ en el desarrollaremos un blog para hablar de _criptomonedas_, como Bitcoin, Litecoin, Quarkcoin, las famosas _cryptos_, de ahí el nombre del proyecto.

Empezamos creando un subdirectorio desde nuestro IDE en [Nitrous.IO][nitro], y lo llamaremos `proyecto_krypton`.

    mkdir proyecto_krypton

y dentro creamos un archivo, con nuestro IDE o con `vim` llamado `requirements.txt` con el siguiente contenido:

    Django==1.6.1
    Pillow==2.3.0
    South==0.8.4
    argparse==1.2.1
    beautifulsoup4==4.3.2
    django-mptt==0.6.0
    django-tagging==0.3.1
    django-xmlrpc==0.1.5
    psycopg2==2.5.2
    pyparsing==2.0.1
    pytz==2013.9
    wsgiref==0.1.2

Es muy importante aclarar que este archivo de dependencias no es estático. Si mañana agregamos un nuevo módulo podemos actualizar este archivo de forma muy fácil con el comando `pip freeze > requirements.txt`.

## Instalación de Zinnia

Vamos a instalar Zinnia directamente desde las fuentes en [GitHub](http://j.mp/ns-zinnia_git) usando también `pip`, como no.

    (krypton)javier@krypton:~$ pip install -e git://github.com/Fantomas42/django-blog-zinnia.git#egg=django-blog-zinnia
    Obtaining django-blog-zinnia from git+git://github.com/Fantomas42/django-blog-zinnia.git#egg=django-blog-zinnia
      Cloning git://github.com/Fantomas42/django-blog-zinnia.git to ./entornos/krypton/src/django-blog-zinnia
      Running setup.py egg_info for package django-blog-zinnia

    [--- Muchas líneas mas ---]

        Adding django-blog-zinnia 0.14.dev to easy-install.pth file

        Installed /home/action/entornos/krypton/src/django-blog-zinnia
    Successfully installed django-blog-zinnia
    Cleaning up...

## La estructura del proyecto

Esto es importante, vamos a usar una estructura que permita exportar el proyecto a repositorios de control de fuentes o usar aplicaciones de sincronización como la que usa [Nitrous.IO][nitro] y de hecho, ya tenemos nuestro primer nivel que es `proyecto_krypton`. Esta es la estructura propuesta, que es un estándar en los proyectos de desarrollo en Django.

1. Proyecto Krypton
    1. Directorio de Django para el proyecto
        1. Configuracion
        1. Blog
        1. Utilerias
        1. Ticker
        1. Foro
        1. Plantillas
        1. Foundation
        2. Media
    1. Documetancion

Ahora toca crear el proyecto de Django, dentro del directorio del proyecto.

    (krypton)javier@krypton:~$ cd proyecto_krypton/
    (krypton)javier@krypton:~/proyecto_krypton$ django-admin.py startproject krypton
    (krypton)javier@krypton:~/proyecto_krypton$ cd krypton/

Esto instala el esqueleto básico pero funcional de un proyecto en Django, y podemos verificar que todo funciona ejecutando el servidor de pruebas.

    (krypton)javier@krypton:~/proyecto_krypton/krypton$ python manage.py runserver 0.0.0.0:8000
    Validating models...

    0 errors found
    January 12, 2014 - 04:51:26
    Django version 1.6.1, using settings 'krypton.settings'
    Starting development server at http://0.0.0.0:8000/
    Quit the server with CONTROL-C.

Es importante que agregues `0.0.0.0:8000` a la línea de comandos para que puedas ver el proyecto en tu navegador, usando la dirección que aparece en __Preview URI__ en la configuración de tu caja.

Y dejamos aquí este artículo, pero antes vamos a hacer un repaso de lo que tenemos hasta este punto.

* Configuramos un _caja_ en [Nitrous.IO][nitro], con lo que tenemos un servidor de alto desempeño con 512 Mb de memoria y 1000 Mb de espacio. Lee este artículo ["Cómo desarrollar una aplicación con Nitrous.IO"](http://j.mp/ns-nitro01)
* Creamos una base de datos PostgreSQL de alta disponibilidad en la red Heroku y configuramos las variables de conexión en nuestra caja: ["Configurar PostgreSQL en Heroku"](http://j.mp/ns-nitro02)
* Instalamos Django y todas las dependencias para ejecutar el motor de nuestro blog que es [Zinnia](zinnia), también configuramos la estructura básica de nuestro proyecto y probamos que el servidor tenga salida a Internet.


[nitro]: http://j.mp/ns-nitro
[heroku]: http://j.mp/ns-heroku
[zinnia]: http://j.mp/ns-zinnia

[^1]: `django-mptt` es un módulo para crear árboles de datos transversales preordenados. No tengo idea que signifique eso, pero ya nos enteraremos más adelante.

[^2]: El nombre del archivo puede ser cualquiera, por ejemplo `requisitos.txt`, pero es un estándar y seguir los estándares es una buena práctica.
