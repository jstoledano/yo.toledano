Title: Cómo desarrollar una aplicación con Nitrous.IO
Date: 2014/01/12 00:42
Category: Desarrollo 
Tags: ide, webdev, krypton, cloud, nitrousio, paas 
Slug: como-desarrollar-una-aplicaicon-con-nitrousio
Author: Javier Sanchez Toledano
Summary: 

¿Ya conocen [Nitrous.IO][nitro]? Pues no se qué están esperando. 

__[Nitrous.IO][nitro]__ es una plataforma de desarrollo basada en la nube con un entorno de desarrollo que funciona en el navegador. Soporta entre otras bases de desarrollo Ruby, Python, Django, Go y Node.JS. Además permite desplegar tu aplicación en maquinas virtuales como Heroku, Azure, Rakespace, por ejemplo.

[Nitrous.IO][nitro] te ayuda a trabajar más fácil, inteligente y eficientemente. Puedes crear cualquier cantidad de _"cajas"_ usando unas plantillas que te permiten empezar a desarrllar verdaderamente rápido.

!!! alert-info "Pide una cuenta gratis"
    Solicita una cuenta en [Nitrous.IO][nitro] ahora, es completamente gratis. Al anotarte, recibes unos 150 _nitros_ que son una especie de puntos, que puedes utilizar para comprar memoria o espacio de disco. Los nitros que te dan al empezar te permiten crear una _caja_ con 348 Mb de memoria y 750 Mb de espacio en disco. __Crea tu cuenta haciendo [clic en este enlace][nitro]__.

## Objetivo

El objetivo es crear la aplicación que servirá para mi nuevo pasatiempo, las monedas virtuales como el Bitcoin, Litecoin y otras criptomonedas. El proyecto tiene el nombre clave __krypton__ y consta inicialmente de un blog, una cinta de noticias (se llama _ticket_) para mostrar cotizaciones de las _criptos_ y un convertidor de monedas. Posteriormente, cuando adquiera las competencias necesarias, un foro. Lo más importante de esto, es que todo esta desarrollado en Django.

### Las Cajas de Nitro

Una vez que tenemos nuestra cuenta podemos crear nuestra primera caja. Hay inicialmente cuatro configuraciones listas para usar, yo elegí __Django__.

![Plantillas](https://dl.dropboxusercontent.com/u/1090580/nspace/201401/nitro01-01-boxes.png)

En la parte inferior vemos unos controles para seleccionar el tamaño de la caja, tenemos 150 _nitros_ para repartir, pero la configuración inicial es suficiente.

![Nitros](https://dl.dropboxusercontent.com/u/1090580/nspace/201401/nitro01-02-boxes.png)

Al dar clic el botón en __Create Box__ estaremos listos para iniciar el desarrollo de nuestra aplicación.

Ahora mismo podemos revisar los datos de nuestra caja. Podemos reiniciarla, apagarla, cambiar su configuración. Es el panel de control de nuestro servidor.

Este panel de control contiene información sensible, por lo que es importante reservarla.

![Panel de Control](https://dl.dropboxusercontent.com/u/1090580/nspace/201401/nitro01-03-boxsettings.png)

Ahora debemos hacer clic en el botón __IDE__ para ir a nuestro entorno de desarrollo integrado.

### El IDE de Nitrous

Primero veamos una pantalla de nuestro entorno de desarrollo.

![El IDE](https://dl.dropboxusercontent.com/u/1090580/nspace/201401/nitro01-04-ide.png)

Como puedes ver es un editor completo, con panel de archivos, menús y una consola dónde puedes ejecutar comandos directamente en tu caja.

[nitro]: http://conxb.com/ns-nitro

Una vez que estamos dentro de nuestro entorno de desarrollo procederemos a preparar el espacio para empezar a crear nuestro proyecto.

## Preparación del entorno virtual

Como buena práctica de desarrollo, vamos a crear nuestro entorno virtual de Python. De forma normal la plantilla tiene instalado los módulos de `Django` y `psycopg2` para empezar a desarrollar, pero yo decidí crear un entorno virtual, por lo que debo volver a instalarlos.

Lo primero que tengo que hacer es agregar configurar la caja para facilitar el trabajo de los entornos virtuales, ya tenemos `virtualenv` y `virtualenvwrapper` por lo que agregamos las siguientes variables a nuestro archivo `~/.bashrc`:

    # Variables de entorno para los Entornos Virtuales
    export WORKON_HOME=~/entornos
    source /usr/local/bin/virtualenvwrapper.sh
    # source /Library/Frameworks/Python.framework/Versions/2.7/bin/virtualenvwrapper.sh
    export PIP_VIRTUALENV_BASE=$WORKON_HOME
    export PIP_RESPECT_VIRTUALENV=true

Al guardar el archivo podemos activar esta configuración escribiendo `source /.bashrc`.

Ahora sí creamos nuestro entorno con esta simple orden desde la consola:

    mkvirtualenv krypton

Y lo activamos así, también desde la consola.

    workon krypton

Con esto podemos ya instalar `django` usando `pip` que se instala en el entorno virtual.

    pip install django

Podemos abrir en la consola el intérprete `python` para verificar la instalación del _framework_:

    Python 2.7.3 (default, Sep 26 2013, 20:03:06) 
    [GCC 4.6.3] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import django
    >>> django.VERSION
    (1, 6, 1, 'final', 0)

Dejo hasta aquí nuestro artículo porque el siguiente es también muy importante. Vamos a usar __Horoku__ para gestionar nuestra base de datos.

Recuerda crear tu cuenta en __[Nitrous.IO][nitro]__.
