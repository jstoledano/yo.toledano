Title: Configuraciones Múltiples para Django
Date: 2014/01/12 10:05
Category: Desarrollo 
Tags: paas, django
Slug: configuraciones-multiples-para-django
Author: Javier Sanchez Toledano
Summary: 

Este es el cuarto artículo de una serie dedicada a documentar la creación de un sitio web. Los tres artículos anteriores son los siguientes:

* [Cómo desarrollar una aplicación con Nitrous.IO](http://conxb.com/ns-nitro01)
* [Configurar PostgreSQL en Heroku](http://conxb.com/ns-nitro02)
* [Configurar un blog con Zinna y Django en Nitrous.IO](http://conxb.com/ns-nitro03)

Este artículo tiene que ver con un patrón de programación que permite mantener un proyecto de Django de forma profesional y sin tiempos muertos. Considera que en con el **Proyecto Krypton** tengo un *servidor local*, en mi laptop; tengo el *servidor de ensayos* y pruebas en [Nitrous.IO][nitro] y mi *servidor de producción*, donde correrá el proyecto una vez terminado. 

Cada uno de estos tres servidores usa una base de datos distinta, en el servidor local tengo instalado el paquete `django-admin-bar`  y además edito las plantillas usando `compass`. En el servidor de pruebas uso una base de datos en Heroku. En el servidor de producción no aplica la opción de `DEBUG`, uso `Gunicorn`, etc. Es decir, hay diferentes entornos de desarrollo y uno de los principios de Django, el principal desde mi punto de vista, dice que no debemos repetirnos (**DRY**, es No Te Repitas o *Don't Repeat Yourself* ) y otro más dice que debemos usar la menor cantidad de código. 

Entonces seguiremos estos principios de programación y usaremos una configuración común para los tres entornos y configuraciones específicas para cada uno, que contengan **solo las opciones necesarias para cada ambiente**.

Tendremos una configuración que llamaremos `local`, para mi laptop; una configuración llamada `nitro` para el servidor de despliegue y una configuración llamada `producción` para el sitio que servirá a los usuarios. Estas tres configuraciones tendrán una base en común y así la llamaremos `base` y con esa vamos a empezar.

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

## Configuración base de Django en un ambiente múltiple

Lo primero que tenemos que hacer es crear un paquete llamado `settings` en nuestra app principal. Es decir, Django de forma predeterminada crea un archivo `settings.py` que es un módulo por si mismo, puedes importarlo en otras aplicaciones y usar las constantes definidas en ese archivo, como lo harías con otro módulo. 

Al crear un directorio y colocar un archivo `__init__.py` en él, este directorio se convierte en un **paquete** y por lo tanto puede contener otros módulos dentro de su nombre de espacio (o *namespace*) a los que podemos acceder con la notación de punto. Es decir, tendremos un módulo `settings.base`, `settings.local`, `settings.nitro` y `settings.produccion` y solo tenemos que activar el módulo correspondiente al entorno de desarrollo en el que estemos.

Vamos a nuestro IDE y creamos una carpeta a la que llamaremos `settings`, haciendo clic con el botón derecho (o con ctrl + clic en las Mac) y eligiendo `New Folder`, aparece una pequeña área de edición donde escribiremos el nombre `settings`:

![folder settings](https://dl.dropboxusercontent.com/u/1090580/nspace/201401/nitro04-02-settings.png)

Dentro de esta carpeta y con la misma técnica del botón derecho (ctrl+clic si usas Mac) crearemos un archivo al que nombraremos `__init__.py`. El nombre es importante, son donde guiones de subrayado (`__`), luego la palabra `init` y luego otros dos guiones de subrayado (`__`). Este archivo le indica a Python que este directorio es un paquete que contiene uno o más módulos.

Este archivo puede estar vacío, aunque el programa que utilizo para editar en el entorno `local` agrega esta línea:

    __author__ = 'Javier Sanchez'
    
Ahora vamos a crear el archivo de configuración base, que contiene las constantes comunes para todos los entornos de desarrollo y producción. Por lo tanto, creamos un nuevo archivo llamado `base.py` dentro de la carpeta `settings`. 

Para hacer más fácil la creación de nuestra configuración base, vamos a abrir el archivo `settings.py` original y de ahí tomaremos las constantes comunes.

## La configuración base

**1. Codificación** - 
La primera línea de mi archivo es la indicación de codificación, ya que documento mi código en español con acentos y `ñ`, es importante decirle a Python que use `UTF-8` para procesar mis archivos.

    # -*- coding: utf-8 -*-
    
Después acostumbro a colocar la identificación del archivo dentro del proyecto. No es precisamente para usarlas como *docstrings* pero me funcionan. Tal vez en el futuro pueda reemplazarlas[^1].

    #         name: mx.com.criptomonedas.settings.base
    #       author: Javier Sanchez Toledano
    #        email: javier(at)namespace.mx
    #          url: https://namespace.mx
    #  description: Configuración base para el proyecto krypton
    #      version: 0.1.0

**2. La ruta base** - 
Hasta la versión 1.5.x de Django, las rutas hacia los directorios de un proyecto 
tenían que escribirse completas, lo que se conoce como *hard coding*. A partir de la versión 1.6 las rutas se *calculan* usando como punto de partida el archivo actual. 

De forma predeterminada se usa el módulo `os.path` para esto, aunque también es posible usar [Unipath](http://conxb.com/ns-Unipath) que parece ser una solución más elegante y es la que usaremos en este proyecto. Usando las rutas calculadas nos aseguramos que nuestro proyecto siempre funcione, sin importar dónde lo coloquemos, y no importando tampoco el sistema operativo ni el sistema de archivos utilizado.

    from unipath import Path
    PROJECT_DIR = Path(__file__).ancestor(3)
    MEDIA_ROOT = PROJECT_DIR.child("media")
    STATIC_URL = '/assets/'
    STATIC_ROOT = PROJECT_DIR.child("static")
    STATICFILES_DIRS = (
        PROJECT_DIR.child("assets"),
    )
    TEMPLATE_DIRS = (
        PROJECT_DIR.child("templates"),
    )
    
**3. Constantes comunes** -
Las siguientes líneas muestras las constantes comunes para los diferentes entornos en donde se ejecutará el proyecto Krypton. 

    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )
    ROOT_URLCONF = 'krypton.urls'
    WSGI_APPLICATION = 'krypton.wsgi.application'

    # Internacionalización
    # Ver https://docs.djangoproject.com/en/1.6/topics/i18n/
    LANGUAGE_CODE = 'es-mx'
    TIME_ZONE = 'Mexico/General'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True

    SITE_ID = 1
    ALLOWED_HOSTS = []

    import django.conf.global_settings as DEFAULT_SETTINGS
    TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS + (
        "django.core.context_processors.request",
    )
    
**4. Las aplicaciones comunes** - 
Veremos más adelante que es posible activar aplicaciones en un ambiente local que no estén presentes en otros, mientras tanto configuramos las aplicaciones y nos remitimos a [la documentación de Zinnia](http://conxb.com/ns-zinnia-doc-apps), que el blog elegido para el proyecto.

    INSTALLED_APPS = (
      'django.contrib.auth',
      'django.contrib.admin',
      'django.contrib.sites',
      'django.contrib.comments',
      'django.contrib.sessions',
      'django.contrib.messages',
      'django.contrib.staticfiles',
      'django.contrib.contenttypes',
      'tagging',
      'mptt',
      'zinnia',
    )

Vemos que aparecen ciertas aplicaciones que no están en la configuración básica, como `django.contrib.sites` para la gestión sitios, el sistema de comentarios `django.contrib.comments`, el gestor de tipos de contenido `django.contrib.contenttypes`, la aplicación `taggit` para etiquetas, `mptt` que es una aplicación que ocupa internamente Zinnia[^2] y la propia aplicación del blog `zinnia`.

**5. Lo que se deja fuera** - 
Se dejan fuera varias constante, que van entonces en las configuraciones específicas.

La primera es la configuración de la base de datos, `DATABASES`. Aunque en los tres entornos de desarrollo uso [PostgreSQL](http://conxb.com/ns-postgresql) en producción y en [Nitrous.IO][nitro] y [Posrgress.app](http://conxb.com/ns-postgresqapp) en Mac, los parámetros de conexión cambian.

También queda fuera la clave secreta (`SECRET_KEY`) que como **buen práctica**
 es conveniente dejarla en las variables de entorno. Tal vez en el entorno de desarrollo que tu utilices sea diferente, pero tanto en [Nitrous.IO][nitro]  como en Mac y en mi servidor de producción puedo usar `export` dentro del archivo `.bashrc` para tener esa variable delicada de forma controlada.

Tener las variables *sensibles* dentro del entorno en el que se ejecute la aplicación podría dar la impresión que no es necesario contar con configuraciones específicas. Sin embargo, como desarrollador, encuentro más cómodo ver esos datos de forma independiente. Es por eso que prefiero definirla de forma separada.

## Configuración de Django para un servidor de desarrollo

Ahora en el IDE vamos a crear un archivo llamado `nitro.py` dentro de nuestro módulo de `settings` y vamos a colocar ahí las configuraciones restantes y que son específicas para nuestro servidor de desarrollo.

**1. La clave secreta** - 
Después de las líneas de codificación e identificación empezamos importando la configuración base, que contiene las opciones comunes.

    from .base import *

Como ves hacemos uso de la ruta relativa, para simplificar el código utilizado. Luego importamos el módulo `os` para tener acceso a las variables del entorno, usando la lista `os.environ`:

    import os
    SECRET_KEY = os.environ['NITRO_SECRET_KEY']

**2. Configuración de la base de datos** - 
Tenemos dos opciones, colocar los datos de conexión que no proporciona Heroku o bien usar la recomendación de Nitrous.IO de usar variables de entorno. Las dos opciones son válidas, así que queda al gusto de cada uno.

    DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'HOST': os.environ['KRYPTON_DATABASE_HOST'],      
            'NAME': os.environ['KRYPTON_DATABASE_NAME'],
            'USER': os.environ['KRYPTON_DATABASE_USER'],
        'PASSWORD': os.environ['KRYPTON_DATABASE_PASS'],
            'PORT': 5432,    
      }
    }

**3. Depuración** - 
Podemos especificar tres opciones relacionadas con la depuración del código y son las siguientes:

    DEBUG = True
    TEMPLATE_DEBUG = True
    ALLOWED_HOSTS = []
    
La primera, `DEBUG` muestra mensajes informativos cuando encuentra un error en el código, de forma que nos ayuda a solucionarlo. Lo mismo pasa con `TEMPLATE_DEBUG` pero ahora con las plantillas. Si estás dos opciones están en falso (`False`), entonces debemos especificar que direcciones de internet tienen permitido servir la aplicación, pero eso lo veremos cuando despleguemos nuestro proyecto en producción.

El archivo de configuración `local.py` es muy parecido, solo que como está en mi laptop, la seguridad es un poco más relajada y codifico completamente la clave secreta y los parámetros de conexión a mi base de datos.

## Uso de configuraciones específicas en Django

Ahora bien, para verificar que nuestro servidor está funcionando debemos indicarle a Django dónde está la configuración, es decir, como se llama el módulo. Podemos hacerlo usando variables de entorno, colocando la siguiente línea en el archivo `.bashrc` o el que corresponda en tu sistema operativo o servidor de despliegue:

    export DJANGO_SETTINGS_MODULE=krypton.settings.local
    
Pero también podemos hacerlo desde la línea de comandos, arrancando nuestro servidor de esta forma:

    python manage.py runserver 0.0.0.0:8000 --settings=krypton.settings.local
    
Como verificamos que nuestra configuración independiente funciona, dejamos aquí este artículo.

    0 errors found                                                                                                                                                 
    January 12, 2014 - 03:58:54                                                                                                                                    
    Django version 1.6.1, using settings 'krypton.settings.nitro'                                                                                                  
    Starting development server at http://0.0.0.0:8000/                                                                                                            
    Quit the server with CONTROL-C.                                                                                                                                
    [12/Jan/2014 03:59:43] "GET / HTTP/1.1" 200 1757

En la próxima entrega de la serie veremos con se configura Zinnia.

[nitro]: http://j.mp/ns-nitro

[^1]: Usar *docstrings* es una buena práctica que debo adoptar de inmediato, pero primero tengo que aprender a usar [Sphinx](http://pythonhosted.org/an_example_pypi_project/sphinx.html#full-code-example)

[^2]: La verdad no se qué es y para qué sirve, pero prometo averiguarlo.
