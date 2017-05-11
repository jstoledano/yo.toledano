Title: Django, Buenas Prácticas
Date: 2015-08-09 12:45:54 a.m.
Category: Desarrollo
Tags:  django
Author: Javier Sanchez Toledano
Summary: 



Ahora si, en serio, voy a comenzar el proyecto de productos cartográficos y lo voy a iniciar con el pie derecho.

Voy a documentar todas las __buenas prácticas__ para crear proyectos en **Django** y no solo eso, también las voy a poner en práctica en el proyecto __Karthos__.

<!--more-->

Primero les voy a platicar un poco acerca del proyecto __Karthos__. Es un portal web que tiene como función la consulta de los productos cartográficos de la entidad y del catálogo de documentos.

Estas dos aplicaciones funcionarán en la parte pública del portal. Existirá una sección _«privada»_ en la que se controlará la actualización de la base geográfica digital.

Este portal va a funcionar en la Intranet de la organización en la que trabajo, por lo que el uso tanto de la parte pública como de la cerrada está restringida a los usuarios de la Intranet.

### Desarrollo, Pruebas y Despliegue

El desarrollo del sistema se hará en una computadora con Mac OS X 10.10 Yosemite, usando la terminal y [Atom](http://atom.io), un editor de código abierto.

Las pruebas se harán en una VPS con [Ubuntu 14.04](http://ubuntu.com) al igual que el despliegue.

## El gestor de paquetes:
El primer paso es instalar el controlador de paquetes `pip` y el segundo el administrador de entornos virtuales `virtualenv`. Empezamos con `pip`:

    javier@koding:~$ sudo apt-get install python-pip
    [sudo] password for javier:
    Leyendo lista de paquetes... Hecho
    Creando árbol de dependencias
    Leyendo la información de estado... Hecho
    Se instalarán los siguientes paquetes extras:
      python-colorama python-distlib python-html5lib python-pkg-resources
      python-setuptools
    Paquetes sugeridos:
      python-lxml python-genshi python-distribute python-distribute-doc
    Paquetes recomendados:
      python-dev-all
    Se instalarán los siguientes paquetes NUEVOS:
      python-colorama python-distlib python-html5lib python-pip
      python-pkg-resources python-setuptools
    0 actualizados, 6 se instalarán, 0 para eliminar y 0 no actualizados.
    Necesito descargar 604 kB de archivos.
    Se utilizarán 2 699 kB de espacio de disco adicional después de esta operación.
    ¿Desea continuar? [S/n]

    Des:1 http://archive.ubuntu.com/ubuntu/ trusty/universe python-colorama all 0.2.5-0.1ubuntu1 [18.3 kB]
    Des:2 http://archive.ubuntu.com/ubuntu/ trusty/universe python-distlib all 0.1.8-1 [113 kB]
    Des:3 http://archive.ubuntu.com/ubuntu/ trusty/main python-html5lib all 0.999-2 [83.2 kB]
    Des:4 http://archive.ubuntu.com/ubuntu/ trusty/main python-pkg-resources all 3.3-1ubuntu1 [61.9 kB]
    Des:5 http://archive.ubuntu.com/ubuntu/ trusty/main python-setuptools all 3.3-1ubuntu1 [230 kB]
    Des:6 http://archive.ubuntu.com/ubuntu/ trusty/universe python-pip all 1.5.4-1 [97.7 kB]
    Descargados 604 kB en 1seg. (392 kB/s)
    Seleccionando el paquete python-colorama previamente no seleccionado.
    (Leyendo la base de datos ... 30705 ficheros o directorios instalados actualmente.)
    Preparing to unpack .../python-colorama_0.2.5-0.1ubuntu1_all.deb ...
    Unpacking python-colorama (0.2.5-0.1ubuntu1) ...
    Seleccionando el paquete python-distlib previamente no seleccionado.
    Preparing to unpack .../python-distlib_0.1.8-1_all.deb ...
    Unpacking python-distlib (0.1.8-1) ...
    Seleccionando el paquete python-html5lib previamente no seleccionado.
    Preparing to unpack .../python-html5lib_0.999-2_all.deb ...
    Unpacking python-html5lib (0.999-2) ...
    Seleccionando el paquete python-pkg-resources previamente no seleccionado.
    Preparing to unpack .../python-pkg-resources_3.3-1ubuntu1_all.deb ...
    Unpacking python-pkg-resources (3.3-1ubuntu1) ...
    Seleccionando el paquete python-setuptools previamente no seleccionado.
    Preparing to unpack .../python-setuptools_3.3-1ubuntu1_all.deb ...
    Unpacking python-setuptools (3.3-1ubuntu1) ...
    Seleccionando el paquete python-pip previamente no seleccionado.
    Preparing to unpack .../python-pip_1.5.4-1_all.deb ...
    Unpacking python-pip (1.5.4-1) ...
    Processing triggers for man-db (2.6.7.1-1) ...
    Configurando python-colorama (0.2.5-0.1ubuntu1) ...
    Configurando python-distlib (0.1.8-1) ...
    Configurando python-html5lib (0.999-2) ...
    Configurando python-pkg-resources (3.3-1ubuntu1) ...
    Configurando python-setuptools (3.3-1ubuntu1) ...
    Configurando python-pip (1.5.4-1) ...

Ahora, nos aseguramos de contar con las versiones más recientes de `python-setuptools` y `python-pip` actualizándolas usando el propio `pip`, primero `setuptools`:

    javier@koding:~$ sudo pip install --upgrade setuptools
    Downloading/unpacking setuptools from https://pypi.python.org/packages/3.4/s/setuptools/setuptools-5.4.2-py2.py3-none-any.whl#md5=8c51acdd5ddadeec330e0170b5b6cf90
      Downloading setuptools-5.4.2-py2.py3-none-any.whl (528kB): 528kB downloaded
    Installing collected packages: setuptools
      Found existing installation: setuptools 3.3
        Uninstalling setuptools:
          Successfully uninstalled setuptools
    Successfully installed setuptools
    Cleaning up...

y luego `pip`[^1]:,

    javier@koding:~$ sudo pip install --upgrade pip
    Downloading/unpacking pip from https://pypi.python.org/packages/py2.py3/p/pip/pip-1.5.6-py2.py3-none-any.whl#md5=4d4fb4b69df6731c7aeaadd6300bc1f2
      Downloading pip-1.5.6-py2.py3-none-any.whl (1.0MB): 1.0MB downloaded
    Installing collected packages: pip
      Found existing installation: pip 1.5.4
        Uninstalling pip:
          Successfully uninstalled pip
    Successfully installed pip
    Cleaning up...


## Entornos virtuales

El segundo paso es instalar el controlador de entornos virtuales llamado `virtualenv`. Este programa nos permite crear entorno de trabajo de Python aislados unos de otros, creando un espacio limpio, sin dependencias, de modo que podemos tener diferentes proyectos funcionando con dependencias y requerimientos independientes entre si, trabajando sin conflictos gracias a que `virtualenv` aísla un entorno de otro.

Instalamos `virtualenv` usando `pip`:

    javier@koding:~$ sudo pip install virtualenv
    Downloading/unpacking virtualenv
      Downloading virtualenv-1.11.6-py2.py3-none-any.whl (1.6MB): 1.6MB downloaded
    Installing collected packages: virtualenv
    Successfully installed virtualenv
    Cleaning up...

### Macros para `virtualenv`

Ahora vamos a instalar un auxiliar para manejar los entornos virtuales más fácilmente. Se llama `virtualenvwrapper` y nos proporciona una serie de macros que nos permiten gestionar rápidamente nuestros entornos.

    javier@koding:~$ sudo pip install virtualenvwrapper
    Downloading/unpacking virtualenvwrapper
      Downloading virtualenvwrapper-4.3.1.tar.gz (86kB): 86kB downloaded
      Running setup.py (path:/tmp/pip_build_root/virtualenvwrapper/setup.py) egg_info for package virtualenvwrapper

        Installed /tmp/pip_build_root/virtualenvwrapper/pbr-0.10.0-py2.7.egg
        [pbr] Processing SOURCES.txt
        warning: LocalManifestMaker: standard file '-c' not found

        warning: no previously-included files found matching '.gitignore'
        warning: no previously-included files found matching '.gitreview'
        warning: no previously-included files matching '*.pyc' found anywhere in distribution
        warning: no files found matching '*.html' under directory 'docs'
        warning: no files found matching '*.css' under directory 'docs'
        warning: no files found matching '*.js' under directory 'docs'
        warning: no files found matching '*.png' under directory 'docs'
    Requirement already satisfied (use --upgrade to upgrade): virtualenv in /usr/local/lib/python2.7/dist-packages (from virtualenvwrapper)
    Downloading/unpacking virtualenv-clone (from virtualenvwrapper)
      Downloading virtualenv-clone-0.2.5.tar.gz
      Running setup.py (path:/tmp/pip_build_root/virtualenv-clone/setup.py) egg_info for package virtualenv-clone

    Downloading/unpacking stevedore (from virtualenvwrapper)
      Downloading stevedore-0.15.tar.gz (348kB): 348kB downloaded
      Running setup.py (path:/tmp/pip_build_root/stevedore/setup.py) egg_info for package stevedore

        Installed /tmp/pip_build_root/stevedore/pbr-0.10.0-py2.7.egg
        [pbr] Processing SOURCES.txt
        warning: LocalManifestMaker: standard file '-c' not found

        warning: no previously-included files found matching '.gitignore'
        warning: no previously-included files found matching '.gitreview'
        warning: no previously-included files matching '*.pyc' found anywhere in distribution
        warning: no files found matching '*.html' under directory 'docs'
        warning: no files found matching '*.css' under directory 'docs'
        warning: no files found matching '*.js' under directory 'docs'
        warning: no files found matching '*.png' under directory 'docs'
        warning: no files found matching '*.py' under directory 'tests'
    Requirement already satisfied (use --upgrade to upgrade): argparse in /usr/lib/python2.7 (from stevedore->virtualenvwrapper)
    Installing collected packages: virtualenvwrapper, virtualenv-clone, stevedore
      Running setup.py install for virtualenvwrapper
        [pbr] Reusing existing SOURCES.txt
        changing mode of build/scripts-2.7/virtualenvwrapper.sh from 644 to 755
        changing mode of build/scripts-2.7/virtualenvwrapper_lazy.sh from 644 to 755
        Skipping installation of /usr/local/lib/python2.7/dist-packages/virtualenvwrapper/__init__.py (namespace package)
        Installing /usr/local/lib/python2.7/dist-packages/virtualenvwrapper-4.3.1-py2.7-nspkg.pth
        changing mode of /usr/local/bin/virtualenvwrapper_lazy.sh to 755
        changing mode of /usr/local/bin/virtualenvwrapper.sh to 755
      Running setup.py install for virtualenv-clone

        Installing virtualenv-clone script to /usr/local/bin
      Running setup.py install for stevedore
        [pbr] Reusing existing SOURCES.txt
    Successfully installed virtualenvwrapper virtualenv-clone stevedore
    Cleaning up...

Para asegurar el correcto funcionamiento de `virtualenvwrapper` debemos agregar estás líneas a nuestro archivo `.bashrc`.

    export WORKON_HOME=$HOME/.entornos
    export PROJECT_HOME=$HOME/proyectos
    source /usr/local/bin/virtualenvwrapper.sh

Las dos primera líneas crean dos variables que le dicen a `virtualenv` dónde debe crear los entornos y dónde los proyectos. La tercera línea, carga desde el inicio de la sesión los macros de `virtualenvwrapper`.

Para activar virtualenvwrapper de inmediato, podemos hacer lo siguiente:

### Crear el entorno `karthos`

Ahora si, estamos listos para crear nuestro proyecto. Esto lo hacemos con el siguiente macro.

    javier@koding:~$ mkvirtualenv karthos
    New python executable in karthos/bin/python
    Installing setuptools, pip...
    done.

Esta simple instrucción copia el programa `python` a la ruta que indicamos en la variable de entorno y copia también los programas necesarios para instalar paquetes en nuestro proyecto.

Como decía más arriba, los entornos están aislados uno de otros. Esto quiere decir que podemos tener tres proyectos funcionando al mismo tiempo, uno con Django 1.4, otro con Django 1.6 y uno más con Django 1.7, cada uno con sus propios paquetes y dependencias, sin que entren en conflicto.

Podemos ver que nuestro entorno está activado porque nuestra línea de comando muestra el nombre del entorno entre paréntesis:

    (karthos)javier@koding:~$

Para activar nuestro entorno, debemos escribir lo siguiente:

    javier@koding:~$ workon karthos
    (karthos)javier@koding:~$

Para salir del entorno escribimos simplemente `deactivate`:

    (karthos)javier@koding:~$ deactivate
    javier@koding:~$  

### Notas

Esta es la primera entrega de la serie de __buenas prácticas__ para gestionar proyectos de Django. El día de hoy vimos que una buena práctica es utilizar entornos virtuales para aislar nuestros proyectos y controlar las dependencias de cada uno de forma independiente.

Mañana veremos otra buena práctica.

[^1]: Me hace gracia que usamos `pip` para actualizar `pip`.
