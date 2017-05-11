Title: Aplicaciones reusables con Django
Date: 2015-08-09 12:45:20 a.m.
Category: Desarrollo
Tags:  django
Author: Javier Sanchez Toledano
Summary: 



Tengo que crear una aplicación reusable en Django. 

¿Les platiqué de la aplicación para controlar las quejas, sugerencias y felicitaciones en el cuadro de mando? Pues se me ocurrió hacerlo en un proyecto pero no pensé como integrarlo al proyecto actual.

La solución es convertir el proyecto en un paquete de Python, de esos que instalas con `pip` y los puedes descargar del índice de paquetes de Python (PyPI). Bueno, hoy tengo que aprender a hacerlos.

<!--more-->

Un paquete de Python proporciona una forma de agrupar código relacionado para poder reutilizarlo de forma simple. Un paquete de Python, por lo tanto, consiste en uno o más archivos de código Python (también conocido como _«módulos»_).

Se puede importar un paquete usando `import foo.bar` o `from foo import bar`. Para que un directorio se convierta en un paquete, debe contener un archivo especial llamado `__init__.py`, no importa si el archivo está vacío.

En este sentido, una _app_ de Django es un paquete de Python cuyo propósito específico es ser utilizado en un proyecto de Django. Un _app_ de Django debería seguir las buenas prácticas definidas por el Proyecto Django, por ejemplo, deberían contar con un archivo `models.py`.

## Control de quejas como una aplicación reusable

Como ya verifiqué que funciona, esta es la estructura de mi aplicación

```
crm\
    manage.py
    core\
        __init__.py
        settings.py
        urls.py
        wsgi.py
        templatetags\
            __init__.py
            crm_extras.py
    quejas\
        __init__.py
        admin.py
        models.py
        views.py
        migrations\
            __init__.py
    data\
        crm.db
    assets\
        css\
            bootstrap.min.css
            animate.min.css
            iconfont.css
            style.css
        js\
            jquery.js
            bootstrap.min.js
            retina.min.js
            animatescroll.js
        img\
            mac1.jpg
            mac2.jpg
            mac3.jpg
    templates\
        index.html
```

La aplicación que necesito en realidad es la que se llama `app` y podría copiarla a mi proyecto de Cuadro de Mando para usarla inmediatamente, pero si lo hago así, entonces cual es el chiste de este artículo, ¿verdad?

### Programas necesarios

Se necesitan varios progamas para crear los paquetes en Django. Por ejemmplo `setuptools`, y `pip`. Pero también utilizo `brew` para instalar programas en Mac OS X y `pip`. Además el código está ubicado en GitHub, por lo que también necesito `git`.

## Empaquetando apps

En Python, el verbo _empaquetar_ se refiere a preparar una aplicación en un formato específico para poder instalarla y usarla fácilmente. El propio _framework_ Django está empaquetado de una forma muy similar a esta. Dicen, que para una aplicación tan simple como la de `quejas`, crear el empaquetado no es tan difícil.

### Procedimiento

1. Lo primero que tienes que hacer es elegir el nombre de la aplicación, en este caso debemos crear un directorio fuera de la estructura de de crm. Llamaremos a este directorio `sgc-crm`.

    Cuando elijas el nombre de tu aplicación debes evitar los conflictos de nombres de tu paquete con el directorio PyPI. Algo que puede ayudar es agregar un prefijo como `django-` al nombre del paquete para su distribución,
     
    El nombre de la aplicación, el que colocas en la constante `INSTALLED_APPS` _debe _ ser único. Evita usar cualquier dombre usado por los paquetes que se distribuyen con Django, como `auth`, `admin` o `contrib`, por ejemplo.

1. Ahora movemos el directorio `crm` al directorio `sgc-crm`.

1. A continuación hay que crearun archivo llamado `scg-crm\README.rst` con el siguiente contenido.

        ======
        Quejas
        ======

        Quejas es una aplicación simple escrita en Django que permite visualizar los datos de Quejas, Sugerencias y Felicitaciones captadas en el INE Tlaxcala. 

        La documentación detallada se encuentra en el directorio "docs".
        
        Inicio rápido
        -------------
        
        1. Agrega "quejas" a la constante INSTALLED_APPS en tu configuración::
        
            INSTALLED_APPS = (
                ...
                'polls',
            )
        
        2. Incluye la configuración de URLs en el archivo urls.py de tu proyecto, por ejemplo::
            
            url(r'quejas/', include('quejas.urls')),

        3. Ejecura `python manage.py syncdb` para crear los modelos utilizados por la aplicación de Quejas.
        
        4. Inicia un servidor de desarrollo y visita la dirección http://127.0.0.1:8000/quejas/ para verificar el desempeño de la aplicación.

1. Crea un archivo `LICENCE`, usa alguna de las licencias que propone GitHub por ejemplo. Investiga un poco para que decidas cuál es la licencia que más te convenga.

1. Crea un archivo `setup.py` el cual proporciona los detalles sobre cómo contruir e instalar la aplicación. La explicación completa la dejaremos para otro momento (la verdad, tengo que investigar primero). Hay que crear el archivo `sgc-crm\setup.py` con el siguiente contenido:

        import os
        from setuptools import setup

        README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

        # allow setup.py to be run from any path
        os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

        setup(
            name='sgc-crm',
            version='0.1',
            packages=['quejas'],
            include_package_data=True,
            license='BSD License',  
            description='Un módulo para el indicador de quejas.',
            long_description=README,
            url='http://yo.toledano.org/',
            author='Javier Sanchez Toledano',
            author_email='javier@koding.mx',
            classifiers=[
                'Environment :: Web Environment',
                'Framework :: Django',
                'Intended Audience :: Developers',
                'License :: OSI Approved :: BSD License', 
                'Operating System :: OS Independent',
                'Programming Language :: Python',
                'Programming Language :: Python :: 2.6',
                'Programming Language :: Python :: 2.7',
                'Topic :: Internet :: WWW/HTTP',
                'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
            ],
        )

1. Solo se incluyen los módulos y paquetes incluídos en el paquete por default. Para incluir archivos adicionales necesitamos crear un archivo `MANIFEST.in`. La documentación de `setuptools` explica con detalle como crear este archivo, para nosotros basta con incluir las plantillas, los archivos estáticos y los archivos de `LEEME` y de licencia en el archivo `sgc-crm\MANIFEST.in`.

        include LICENSE
        include README.rst
        recursive-include crm/static *
        recursive-include crm/templates *

1. Con esto de los premios al mérito es importante documentar todo lo que se hace y como funciona esta aplicación. Creo que lo haré en otro momento. Pero voy a crear, eso si, el directorio `sgc-crm\docs` para que cuando, en el futuro, me de tiempo de crear la documentación, pueda incluirla. Hay que agregar esta línea en el archivo `sgc-crm\MANIFEST.in`.

        recursive-include docs 

    Este directorio no se ba a incluir en el paquete a menos que tenga de verdad algún archivo. Muchos programadores incluyen la documentación en sitios como [readthedocs.org](https://readthedocs.org/) (no es mi caso).

1. Por último, debemos crear el paquete con el comando `pythons setup.py sdist` (desde fuera de `sgc-crm`) y si todo sale bien tendremos el paquete `sgc-crm-0.1.tar.gz`.

Veamos...