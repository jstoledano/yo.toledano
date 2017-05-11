Title: Como instalar Python, Django, Nginx y Memcached en un servidor Ubuntu desde cero, parte 1
Date: 2013/12/16 04:32
Category: Desarrollo 
Tags: server-admin, python, django 
Slug: como-instalar-pytho-django-nginx-y-memcached-en-un
Author: Javier Sanchez Toledano
Summary: 

Recientemente me ofrecieron una oferta parte de [BurstNET][burst] para contratar una VPS a mitad de precio, así que decidí dejar temporalmente mi VPS en [DigitalOcean](http://j.mp/ns-ocean) y probar suerte con este servidor con el que tengo el doble de recursos a menos de la mitad de precio. 

El código de  **namespace.mx** pasó integró al servidor y una vez que todo funcionaba correctamente, hice el cambio de servidores, por lo que la mudanza fue transparente para los usuarios.

Pero vayamos por pasos.

## Preparación del Servidor

Como servidor elegí [Ubuntu 10.04 LTS Server](http://j.mp/18sLDf3) básicamente porque las otras imágenes que tiene disponibles [BurstNET][burst] ya no tienen soporte y esta versión es _Long Term Support_ y su soporte terminará en el 2015. También es que estoy muy acostumbrado a Ubuntu y a los comandos de `apt-get`, claro.

En general cualquier distribución de Ubuntu puede funcionar, pero para servidores recomiendo las que terminan en LTS. Puedes consultar que distribución usas con este comando.

    javier@dev:~$ cat /etc/issue
    Ubuntu 10.04.1 LTS \n \l

Una vez que recibes los datos para ingresar a tu VPS, algo que es inmediato, después de pagar, tu servidor está listo.

Lo siguiente que hay que hacer es asegurarnos que hay que actualizarlo, usando el siguiente comando:

	root@dev:~# apt-get update
    Obj http://ftp.debian.org squeeze Release.gpg
    Ign http://ftp.debian.org squeeze/main Translation-es
    Ign http://ftp.debian.org squeeze/contrib Translation-es        
    Obj http://ftp.debian.org squeeze Release                       
    Ign http://ftp.debian.org squeeze/main Packages/DiffIndex       
    Ign http://ftp.debian.org squeeze/contrib Packages/DiffIndex
    Obj http://security.debian.org squeeze/updates Release.gpg
    Ign http://security.debian.org squeeze/updates/main Translation-es
    Ign http://security.debian.org squeeze/updates/contrib Translation-es
    Obj http://security.debian.org squeeze/updates Release 
    Ign http://security.debian.org squeeze/updates/main Packages/DiffIndex
    Obj http://ftp.debian.org squeeze/main Packages
    Ign http://security.debian.org squeeze/updates/contrib Packages/DiffIndex
    Obj http://security.debian.org squeeze/updates/main Packages
    Obj http://security.debian.org squeeze/updates/contrib Packages
    Obj http://ftp.debian.org squeeze/contrib Packages
    Leyendo lista de paquetes... Hecho
    	
Si es necesario actualizar, usamos esta otra instrucción:

    root@dev:~# apt-get upgrade
    Leyendo lista de paquetes... Hecho
    Creando árbol de dependencias       
    Leyendo la información de estado... Hecho
    Los siguientes paquetes se han retenido:
      apt apt-utils aptitude bind9-host cpp cpp-4.4 dhcp3-client dhcp3-common dnsutils gcc-4.4-base
      iptables libbind9-60 libgcc1 libisccc60 liblwres60 libstdc++6 mutt python python-apt
      python-minimal x11-utils
    0 actualizados, 0 se instalarán, 0 para eliminar y 21 no actualizados.

Y puede ser necesario hacer actualizaciones mayores, cuando quedan paquetes por actualizar, como se observa en el mensaje anterior, por lo que aplica el siguiente comando:

    root@dev:~# apt-get dist-upgrade
    Leyendo lista de paquetes... Hecho
    Creando árbol de dependencias       
    Leyendo la información de estado... Hecho
    Calculando la actualización... Listo
    Los siguientes paquetes se ELIMINARÁN:
      libept0
    Se instalarán los siguientes paquetes NUEVOS:
      isc-dhcp-client isc-dhcp-common libboost-iostreams1.42.0 libdns69 libept1 libisc62 libisccfg62
      libmpfr4 libnfnetlink0 libtokyocabinet8 libxapian22 libxcb-atom1 python-apt-common python2.6
      python2.6-minimal
    Se actualizarán los siguientes paquetes:
      apt apt-utils aptitude bind9-host cpp cpp-4.4 dhcp3-client dhcp3-common dnsutils gcc-4.4-base
      iptables libbind9-60 libgcc1 libisccc60 liblwres60 libstdc++6 mutt python python-apt
      python-minimal x11-utils
    21 actualizados, 15 se instalarán, 1 para eliminar y 0 no actualizados.
    Necesito descargar 22.1MB de archivos.
    Se utilizarán 21.0MB de espacio de disco adicional después de esta operación.
    ¿Desea continuar [S/n]?

Asegúrate de cambiar la contraseña que te mandaron originalmente por una en la que tu puedas confiar. Usa este comando para hacerlo:

    root@dev:~# passwd

## Crear un usuario

Es importante aumentar la seguridad de nuestro servidor, por ello es muy recomendable no usar el usuario `root`, para evitar desde errores hasta fugas de seguridad. Para esto vamos a crear un usuario y le asignaremos permisos de administración, pero usando contraseñas. Veamos como hacerlo.

    root@dev:~# adduser javier
    perl: warning: Setting locale failed.
    perl: warning: Please check that your locale settings:
	    LANGUAGE = (unset),
	    LC_ALL = "",
	    LC_MONETARY = "es_MX.UTF-8",
	    LC_NUMERIC = "es_MX.UTF-8",
	    LC_MESSAGES = "es_MX.UTF-8",
	    LC_COLLATE = "es_MX.UTF-8",
	    LC_CTYPE = "es_MX.UTF-8",
	    LC_TIME = "es_MX.UTF-8",
	    LANG = "C"
    are supported and installed on your system.
    perl: warning: Faling back to the standard locale ("C").
    Adding user `javier' ...
    Adding new group `javier' (1000) ...
    Adding new user `javier' (1000) with group `javier' ...
    Creating home directory `/home/javier' ...
    Copying files from `/etc/skel' ...
    Enter new UNIX password: 
    Retype new UNIX password: 
    passwd: password updated successfully
    Changing the user information for javier
    Enter the new value, or press ENTER for the default
	    Full Name []: 
	    Room Number []: 
	    Work Phone []: 	
	    Home Phone []: 
	    Other []: 
    Is the information correct? [Y/n] y

El siguiente paso es asignarle a este usuario permisos de administrador.

De esta manera un usuario normal, usará comandos como administrador usando `sudo comando` y su contraseña, por lo que usar el usuario `root` ya no será necesario y se reducen las posibilidades de *hackeo*, evita que hagamos destrozos a nivel del sistema y guarda los registros de las actividades en un archivo de bitácora.

Primero debemos instalar el paquete `sudo` porque Debian 6 no lo instala por default.

    root@dev:~# apt-get install sudo
    Leyendo lista de paquetes... Hecho
    Creando árbol de dependencias       
    Leyendo la información de estado... Hecho
    Se instalarán los siguientes paquetes NUEVOS:
      sudo
    Necesito descargar 611kB de archivos.
    Se utilizarán 967kB de espacio de disco adicional después de esta operación.
    Des:1 http://ftp.debian.org squeeze/main sudo 1.7.4p4-2.squeeze.4 [611kB]
    Descargados 611kB en 3s (155kB/s)
    Seleccionando el paquete sudo previamente no seleccionado.
    (Leyendo la base de datos ... 17878 ficheros o directorios instalados actualmente.)
    Desempaquetando sudo (de .../sudo_1.7.4p4-2.squeeze.4_amd64.deb) ...
    Procesando disparadores para man-db ...
    Configurando sudo (1.7.4p4-2.squeeze.4) ...
    No /etc/sudoers found... creating one for you.

Ahora editamos este archivo `/etc/sudoers` usando un comando recién instalado llamado `visudo` que abre este archivo especial, que siempre es de solo lectura, y permite editarlo sin interferir en los permisos especiales que tiene el archivo.

Buscamos estas líneas y las remplazamos con nuestro usuario:

    # User privilege specification
    root    ALL=(ALL) ALL
    
Para que al final tengamos esta línea:

    javier    ALL=(ALL) ALL

Una vez que hemos configurado los permisos de administración, podemos cerrar la sesión de usuario y reconectarnos con nuestra cuenta sin privilegios, para continuar desde ahí con la configuración del servidor.

## Configurar SSH

En mi trabajo el puerto `22`, que corresponde al servidor `ssh` está bloqueado, por lo que debo usar otro distinto. Esto agrega seguridad a tu servidor, ya que además vamos a impedir que se use el usuario `root` a través de una conexión remota. Pero debes saber que si olvidas esta configuración no podrás entrar a tu sistema.

Abrimos entonces el archivo `/etc/ssh/sshd_config`

    javier@dev:~$ sudo vi /etc/ssh/sshd_config 
    
    We trust you have received the usual lecture from the local System
    Administrator. It usually boils down to these three things:

        #1) Respect the privacy of others.
        #2) Think before you type.
        #3) With great power comes great responsibility.

    [sudo] password for javier:

El mensaje aparece una sola vez y nos recuerda que debes ser precavidos cuando usamos los permisos de super usuario. 

Ahora localizamos las líneas siguientes en el archivo y hacemos los ajustes necesarios:

    Port 2222
    PermitRootLogin no
    UseDNS no
    AllowUsers javier

Para terminar, recargamos el servidor `sshd`, cerramos sesión y verificamos nuestra conexión.

    javier@dev:~$ sudo /etc/init.d/ssh reload
    
Y para conectarnos, debemos especificar el puerto que escribimos antes

    namespace:~ javier$ ssh -p 2222 javier@10.13.25.35

## Configurar la `timezone`

Resulta que la combinación que usaremos de Django y PostgreSQL tienen una forma muy precisa de manejar las fechas, por lo que si no queremos ver resultados diferentes en nuestro sitio, debemos asegurarnos que el huso horario está bien configurado.

Observa como el servidor te dará la hora del huso horario configurado en el sistema:

    javier@dev:~$ date
    lun dic  9 01:34:25 UTC 2013
    javier@dev:~$ export TZ=Mexico/General
    javier@dev:~$ date
    dom dic  8 19:34:53 CST 2013

Primero nos da la hora del Meridiano de Greenwich, UTC o Zulu y luego la Hora del Centro de México.

Para hacer estos cambios permanentes *reconfiguraremos* los datos de la *timezone* como administradores. Recuerda seleccionar el huso horario que más te convenga.

    javier@dev:~$ sudo dpkg-reconfigure tzdata

Seleccionamos primero el área geográfica, en mi caso `America`, luego el huso horario, que en mi caso puede ser `Mexico_City`, aunque también ya vimos que funciona con `Mexico/General`, pero eso depende de la distribución que uses. El resultado es el siguiente:

    Current default time zone: 'America/Mexico_City'
    Local time is now:      Sun Dec  8 19:42:51 CST 2013.
    Universal Time is now:  Mon Dec  9 01:42:51 UTC 2013.

El `CST` que vemos corresponde a las siglas de *Central Standard Time* que es el mismo que el uso que llamamos Hora del Centro de México o `ETC+6` y `ETC+5` en horario de verano o `DST`. Créanme que la precisión utilizada hace que estos detalles sean importantes.

## Configuración del servidor en Español

Para configurar Debian 6.0 en español, debemos instalar el paquete `localization-config`, 

    javier@dev:~$ sudo apt-get install localization-config
    Leyendo lista de paquetes... Hecho
    Creando árbol de dependencias       
    Leyendo la información de estado... Hecho
    Se instalarán los siguientes paquetes extras:
      libapt-pkg-perl libconfig-inifiles-perl
    Se instalarán los siguientes paquetes NUEVOS:
      libapt-pkg-perl libconfig-inifiles-perl localization-config
    0 actualizados, 3 se instalarán, 0 para eliminar y 0 no actualizados.
    Necesito descargar 193 kB de archivos.
    Se utilizarán 918 kB de espacio de disco adicional después de esta operación.
    ¿Desea continuar [S/n]?
    
Y a continuación el comando `update-locale-config` junto con el código del idioma que quieras,
    
    javier@dev:~$ sudo update-locale-config es_MX

Si ahora usamos el comando `date`, veremos algo de lo que ha cambiado[^2],

    javier@dev:~$ date
    dom dic  8 19:52:18 CST 2013

## Compilación de Python

En mi servidor la versión instalada de Python es la 2.6.2, y como yo quería una versión más nueva, descargué las fuentes de Python y me dispuse a compilarlas. 

No tiene mucha ciencia, solo necesitas algunos cuantos paquetes para poder hacerlo, 

Primero debemos instalar los programas de compilación.

    javier@dev:~$ sudo apt-get install build-essential

También instalé, porque no estaba seguro de cuales librerías necesitaba, algunos paquetes de desarrollo que necesita Python para construir los módulos de la biblioteca estándar.

    javier@dev:~$ sudo apt-get install libsqlite3-dev libreadline-dev libncurses5-dev libgdbm-dev libbz2-dev zlib1g-dev

Ahora descargamos el código fuente directamente del sitio de Python, desde esta dirección [http://www.python.org/download/](http://www.python.org/download/), la versión actual es la 2.7.6.

    javier@dev:~/download$ wget http://www.python.org/ftp/python/2.7.6/Python-2.7.6.tgz
    --2013-12-14 20:23:59--  http://www.python.org/ftp/python/2.7.6/Python-2.7.6.tgz
    Resolving www.python.org... 82.94.164.162, 2001:888:2000:d::a2
    Connecting to www.python.org|82.94.164.162|:80... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: 14725931 (14M) [application/x-tar]
    Saving to: `Python-2.7.6.tgz'

    100%[==========================================================>] 14,725,931  4.40M/s   in 3.7s    

    2013-12-14 20:24:03 (3.75 MB/s) - `Python-2.7.6.tgz.1' saved [14725931/14725931]

Lo descompactamos con `tar xfz Python-2.7.6.tgz` y nos cambiamos al directorio creado `cd Pyhon-2.7.6` para configurar y compilar el código fuente.

Primero lo configuramos, ejecutando el archivo `./configure` y luego compilamos el código fuente con `make`, así nomás.

Después de una compilación limpia, notarás que hay un aviso referente a librerías faltantes que impiden que ciertos módulos se compilen. Para solucionar este problema, solo debemos instalar los paquetes `-dev` correspondientes, como vimos hace un momento.

    Python build finished, but the necessary bits to build these modules were not found:
    _bsddb             _tkinter           bsddb185        
    dl                 imageop            sunaudiodev     
    To find the necessary bits, look in setup.py in detect_modules() for the module's name.

    running build_scripts
    
En mi servidor no compilé `tkinter` ni `sunaudiodev` porque no los voy a utilizar, pero si quisiera hacerlo tendría que instalar las librerías de apoyo correspondientes.

## Configuración de Python y virtualenv

Ahora vamos a preparar el programa **Python** para poder usar entornos virtuales y mejorar la forma en la que trabajaremos con Django. 

Primero debemos instalar un paquete que se llama [`setuptools`](https://pypi.python.org/pypi/setuptools) que nos dará un comando llamado `easy_install` y lo usaremos una sola vez para instalar `pip`.

Después de descargar y descomprimir el archivo, la instalación se lleva a cabo con Python:

    javier@dev:~/download/setuptools-2.0$ python setup.py install

Y luego, ya que está instalado, ejecutamos `easy_install`,
    
    javier@dev:~/download/setuptools-2.0$ easy_install pip

Y este es el programa que utilizaremos a partir de este momento para instalar y actualizar nuestro sistema de Python, ya que este `pip` junto con `virtualenv` nos permite configurar múltiples perfiles de Python sin que interfieran unos con otros.
    
Ahora toca actualizar el paquete `virtualenv`,

    javier@dev:~$ sudo pip install --upgrade virtualenv 
    
Ahora instalamos `virtualenvwrap` para manejar más fácilmente nuestros entornos virtuales.

    javier@dev:~$ sudo pip install virtualenvwrapper
    
!!! alert-error "Precaución"
    Debes cuidar de no ejecutar el comando anterior mientras esté activo un entorno virtual. Si no sabes si está activo uno, lo más seguro es que no.
    
A continuación vamos a crear un directorio donde ubicaremos los distintos entornos virtuales y una serie de variables globales para facilitar el manejo de estos entorno.

Primero creamos el directorio:

    javier@dev:~$ mkdir entornos
    
Luego editamos el archivo `~/.bashrc` y agregamos las siguientes variables.

    # Variables de entorno para los Entornos Virtuales
    export WORKON_HOME=~/entornos
    source /usr/local/bin/virtualenvwrapper.sh
    export PIP_VIRTUALENV_BASE=$WORKON_HOME
    export PIP_RESPECT_VIRTUALENV=true

Si usas Mac OS X, debes ajustar la ruta para `virtualenvwrapper.sh`, esa línea debe quedar de la siguiente manera, 

    source /Library/Frameworks/Python.framework/Versions/2.7/bin/virtualenvwrapper.sh

Y por el momento, vamos a dejar así la configuración porque necesitamos instalar otros paquetes a nivel servidor y no en los entornos virtuales.

## Instalación de PostgreSQL

Por motivos de trabajo, por convicción y por gusto seleccioné PostgreSQL como el servidor de base de datos, aunque no he dudado en dudar otros motores cuando algún cliente lo solicita, para mis proyectos personales he decidido usar al elefantito. Instalarlo en Debian es realmente muy simple:

    javier@dev:~$ sudo apt-get install postgresql postgresql-contrib

Y ahora es momento de configurar a nuestro usuario, administrador de base de datos, por lo que debemos hacer lo siguiente, escribir el nombre del usuario,una contraseña y elegir si el usuario recién creado tendrá permisos para crear usuarios y bases.

    javier@dev:~$ sudo su - postgres
    postgres@dev:~$ createuser -P
    Ingrese el nombre del rol a agregar: nspace
    Ingrese la contraseña para el nuevo rol: 
    Ingrésela nuevamente: 
    ¿Será el nuevo rol un superusuario? (s/n) n
        
Una vez creado, creamos también la base de datos, y asignamos a nuestro usuario como el dueño de la base.

    postgres@dev:~$ createdb --owner nspace  nbase
    postgres@dev:~$ logout
    
## Creación de entornos virtuales

Ahora que hemos instalado el manejador de bases de datos, entramos de lleno en la preparación del entorno de trabajo *ideal* para nuestro sitio y debemos crear el entorno virtual exclusivo para este sitio.

Contar con entornos virtuales hace muy fácil trabajar con diferentes proyectos en el mismo servidor sin que los requisitos de un proyecto interfieran con los otros. 

Recordemos que todos nuestros proyectos utilizan el directorio `entornos`, así que procedemos a crear el entorno virtual para **namespace.mx**,

    javier@dev:~$ mkvirtualenv nspace
    New python executable in nspace/bin/python
    Installing Setuptools..............................................................................................................................................................................................................................done.
    Installing Pip.....................................................................................................................................................................................................................................................................................................................................done.
    (nspace)javier@dev:~$
    
Este comando crea el entorno virtual y lo activa de una vez, el `(nspace)` en el indicador nos dice el nombre del entorno virtual en el que estamos trabajando. Si el entorno no está activado, lo podemos activar como sigue,

    javier@dev:~$ workon nspace
    
Y con esto tenemos listo nuestro entorno virtual para trabajar instalar Django.

## Instalación de Django

La instalación de Django, con el servidor configurado como lo tenemos es algo verdaderamente trivial. Podríamos por ejemplo tener diferentes versiones de Django para distintos proyectos sin que uno afecte a otro, porque cada entorno virtual está aislado y no tiene acceso a los otros.

Entonces, para instalarlo, solo debemos hacer lo siguiente, **con nuestro entorno activado**:

    (nspace)javier@dev:~$ pip install django
    Downloading/unpacking django
      Downloading Django-1.6.tar.gz (6.6MB): 6.6MB downloaded
      Running setup.py egg_info for package django
        warning: no previously-included files matching '__pycache__' found under directory '*'
        warning: no previously-included files matching '*.py[co]' found under directory '*'
    Installing collected packages: django
      Running setup.py install for django
        changing mode of build/scripts-2.6/django-admin.py from 664 to 775
        warning: no previously-included files matching '__pycache__' found under directory '*'
        warning: no previously-included files matching '*.py[co]' found under directory '*'
        changing mode of /home/javier/entornos/nspace/bin/django-admin.py to 775
    Successfully installed django
    Cleaning up...
    
Con esto es suficiente y podemos verificar la versión instalad de Django con el siguiente comando.

    (nspace)javier@dev:~$ python
    Python 2.6.6 (r266:84292, Dec 26 2010, 22:31:48) 
    [GCC 4.4.5] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import django
    >>> django.VERSION
    (1, 6, 0, 'final', 0)
    >>> 
    (nspace)javier@dev:~$
    
## Instalación de requisitos

Otra ventaja de `pip` es que puede hacer una lista de los paquetes instalados en el entorno virtual activo

Esto es importante, porque como dije al principio, estoy mudando mi blog y me interesa que no haya problemas por algún paquete faltante, así que en mi servidor actual, que en este caso es mi servidor de desarrollo, pido los paquetes instalados y los guardo en un archivo llamado `requisitos.txt`,

    (nspace)namespace:proyecto_namespace javier$ pip freeze --local > requisitos.txt 
    
El archivo resultante es como el siguiente,

    (nspace)namespace:proyecto_namespace javier$ cat requisitos.txt 
    BeautifulSoup==3.2.1
    Django==1.6
    Jinja2==2.7.1
    Markdown==2.4.dev
    MarkupSafe==0.18
    Pygments==1.6
    South==0.8.4
    Sphinx==1.1.3
    Unipath==1.0
    amqp==1.3.3
    anyjson==0.3.3
    argparse==1.2.1
    beautifulsoup4==4.3.2
    billiard==3.3.0.11
    brillixy==0.6.1
    celery==3.1.3
    django-annoying==0.7.7
    django-braces==1.2.2
    django-celery==3.1.1
    django-debug-toolbar==0.11.0
    django-floppyforms==1.1
    django-taggit==0.11.1
    docutils==0.11
    guess-language==0.2
    gunicorn==18.0
    ipython==1.1.0
    kombu==3.0.7
    mdx-smartypants==1.5.0
    namedentities==1.5.2
    psycopg2==2.5.1
    pyparsing==2.0.1
    pyreadline==2.0
    python-dateutil==2.2
    python-memcached==1.53
    python-pydown==0.1.0
    pytz==2013.8
    redis==2.8.0
    scss==0.8.72
    six==1.4.1
    smartypants==1.8.3
    sqlparse==0.1.10
    times==0.6.2
    
Y para instalar todos estos paquetes, debemos ejecutar la siguiente orden con nuestro entorno activado,

    (nspace)namespace:proyecto_namespace javier$ pip install -r requisitos.txt

No importa la ruta inicial ni el nombre del archivo, aunque se acostumbra en inglés `requeriments.txt`, pero como ven, en español, `requisitos.txt` también funciona.

## Configurar el *driver* de PostgreSQL con Django

En la lista de paquetes necesarios para nuestro proyecto se encuentra el *driver* que conecta a Django con PostgreSQL, en caso que sea necesario compilarlo, necesitarás instalar[^3] (como administrador) los paquetes necesarios, que son los siguientes:

* **`build-essentials`** -- que instala el compilador y los archivos y librerías asociados.
* **`libpq-dev`** -- este paquete contiene los archivos necesarios para compilar módulos de PostgreSQL.

## Ajustar la configuración al nuevo servidor

Ahora debemos ajustar la configuración del proyecto al nuevo servidor, solo en caso que hay cambios, pero por la configuración segmentada, solo debemos ajustar el archivo de configuración correspondiente. 

En mi caso, el archivo sería `producción.py`, pero la base de datos se llama igual, así como mi usuario.


En el siguiente artículo veremos como etá hecho este blog, pieza por pieza.

[^1]: Me salgo del tema, lo sé, pero estoy usando un ejemplo vivo en un servidor real, los errores que aparecen, los resuelvo en el momento y los documento para que quede constancia.

[^3]: Recuerda que estamos usando un servidor Ubuntu 10.04 LTS.

[^2]: En el servidor que utilicé creo que ya estaban los _locales_ configurados.

[burst]: "http://j.mp/ns-burst"
