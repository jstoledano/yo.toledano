Title:  Actualizando el Cuadro de Mando   
Date: 2015-09-15 18:11:41
Category: desarrollo
Tags:  django, python, cmi
Summary: 


El Cuadro de Mando Integral es un conjunto de aplicaciones que han funcionado desde hace uno cuatro años con **Django**. Pero no he podido actualizar ni la versión de *Python* y peor aún, la versión de **Django**, que sigue usando la versión 1.6.4 que ya no tiene soporte y que me impide aprovechar muchas de las ventajas que ofrece **Django Framework**.

Así que tomé el código fuente del servidor y una copia de la base de datos del *CMI* para poder trabajar en mi laptop.

### Entorno virtual

Lo primero que hice fue crear un nuevo entorno virtual para empezar desde cero:

```bash
toledano@toledano src (master) $ mkvirtualenv cmi
New python executable in cmi/bin/python2.7
Also creating executable in cmi/bin/python
Installing setuptools, pip...done.
```

Y también actualizo el `pip`, para tener todo en la última versión:

```bash
(cmi)toledano@toledano src (master) $ pip install --upgrade pip
Downloading/unpacking pip from https://pypi.python.org/packages/py2.py3/p/pip/pip-7.1.2-py2.py3-none-any.whl#md5=5ff9fec0be479e4e36df467556deed4d
  Downloading pip-7.1.2-py2.py3-none-any.whl (1.1MB): 1.1MB downloaded
Installing collected packages: pip
  Found existing installation: pip 1.5.6
    Uninstalling pip:
      Successfully uninstalled pip
Successfully installed pip
Cleaning up...
```

### Requisitos

La lista de requisitos del *CMI* ya tiene algunos años y al haber sido generada con la orden `pip freeze` tenía las versiones exactas con las que funciona el *Cuadro de Mando*. Además no estoy seguro que sea necesite todos los paquetes que aparecen en la lista. Estos son algunos de los paquetes instalados en el Cuadro de Mando:

```
Django==1.6.2
Markdown==2.4
MySQL-python==1.2.5
South==0.8.4
Unipath==1.0
django-annoying==0.7.9
django-bootstrap-toolkit==2.15.0
django-crispy-forms==1.4.0
django-timedeltafield==0.7.1
django-tinymce==1.5.2
ipython==1.2.1
psycopg2==2.5.2
readline==6.2.4.1
six==1.5.2
wsgiref==0.1.2
```

Cómo les decía, tengo algunas dudas sobre ciertos paquetes, como `django-crispy-forms`, `South` y `django-bootstrap-toolkit`. Además, como no puedo migrar a PostgreSQL no necesito `psycopg`.

Al final, la lista queda de la siguiente manera.

```
Django
Markdown
MySQL-python
Unipath
argparse
django-annoying
django-bootstrap-toolkit
django-taggit
django-timedeltafield
django-tinymce
django-watson
gunicorn
ipython
readline
six
wsgiref
```

Estos son los requisitos generales, la idea es que ninguna aplicaciones del cuadro de mando requiera algún paquete que no esté en esta lista y de ser posible, eliminar por lo menos tres paquetes: `django-annoying`, `django-bootstrap-toolkit` y `django-timedeltafield`. Los paquetes `ipython` y `readline` no son extrictamente necesarios, y `gunicorn`, `argparse` y `wsgiref` no se necesitan en desarrollo, solo en producción.

La estrategia es crear tres grupos de requisitos: el grupo `base` con paquetes comunes, `local` con los paquetes que se usan en desarrollo y `produccion` para lo que se indica.

Este sería el grupo `base`:

```
Django
Markdown
MySQL-python
Unipath
django-taggit
django-tinymce
django-watson
six
```

Este es el grupo `local`:

```
ipython
readline
django-debug-toolbar
```

Y en el grupo `produccion` tenemos

```
argparse
gunicorn
wsgiref
```

Ahora si, vamos a instalar los requisitos para el CMI.

### MySQL-Python

Encuentro un pequeño problema al instalar el paquete `mysql-python`...

```bash
Collecting MySQL-python (from -r requeriments/base.txt (line 3))
  Downloading MySQL-python-1.2.5.zip (108kB)
    100% |████████████████████████████████| 110kB 231kB/s 
    Complete output from command python setup.py egg_info:
    sh: mysql_config: command not found
    Traceback (most recent call last):
      File "<string>", line 20, in <module>
      File "/private/var/folders/p2/_vvdgwbx6zd55v10f8kjrngw0000gn/T/pip-build-NfrQ4v/MySQL-python/setup.py", line 17, in <module>
        metadata, options = get_config()
      File "setup_posix.py", line 43, in get_config
        libs = mysql_config("libs_r")
      File "setup_posix.py", line 25, in mysql_config
        raise EnvironmentError("%s not found" % (mysql_config.path,))
    EnvironmentError: mysql_config not found
    
    ----------------------------------------
Command "python setup.py egg_info" failed with error code 1 in /private/var/folders/p2/_vvdgwbx6zd55v10f8kjrngw0000gn/T/pip-build-NfrQ4v/MySQL-python
```

El conector, para poder compilarse, se necesita enlazar con las librerías de MySQL. Para lograrlo, `pip` pregunta al programa `mysql_config` dónde se encuentran las librerías. Esto complica un poco las cosas. Primero porque necesitamos instalar el programa `cmake` y la forma de hacerlo es usando `brew`.

```
(cmi)toledano@toledano Downloads $ brew install cmake
Warning: You are using OS X 10.11.
We do not provide support for this pre-release version.
You may encounter build failures or other breakage.
==> Downloading http://www.cmake.org/files/v3.3/cmake-3.3.1.tar.gz

... eliminio muchas líneas de información ...

Add the following to your init file to have packages installed by
Homebrew added to your load-path:
(let ((default-directory "/usr/local/share/emacs/site-lisp/"))
  (normal-top-level-add-subdirs-to-load-path))
==> Summary
🍺  /usr/local/Cellar/cmake/3.3.1: 1901 files, 33M, built in 15.6 minutes
```

Como uso el programa [MAMP](https://www.mamp.info/en/), debo instalar los componentes adicionales: [MAMP_components_2.0.2.dmg](http://sourceforge.net/projects/mamp/files/latest/download?source=files).




Porque se necesita compilar y no se encuentra la librería de **MySQL** para enlazar el conector. Como uso un programa llamado [MAMP](https://www.mamp.info/en/) debo incluir la ruta de los ejecutables al momento de compilar, para que `pip` encuentre el programa `mysql_config`.





