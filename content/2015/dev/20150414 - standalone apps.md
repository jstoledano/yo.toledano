Title: Aplicaciones reutilizables en Django  
Date: 2015-04-14 21:35:22  
Category: Desarrollo  
Tags:  django, webdev,   
Author: Javier Sanchez Toledano  
Summary: Cómo crear aplicaciones reusables en Django  


> Voy a confesar una cosa: nunca había entendido como funcionaban las plantillas en Django o como hacer aplicaciones reutilizables. Hasta hoy.

Para empezar voy a hablar del proyecto en el que estoy trabajando. Es muy simple: se trata de una aplicación para capturar los resultados de encuestas, con algunos datos de identificación (`fecha` y `modulo`), cuatro preguntas que solo permiten escribir números del 0 al 10 y un combo para elegir 5 opciones. 
Es una aplicación de captura muy rápida y genera toda una serie de estadísticas anuales, mensuales y por módulo.

Pero lo que hace no es importante en este artículo, se trata de convertir esta aplicación en un componente modular del cuadro de mando y al mismo tiempo en una aplicación independiente. Y además se debe poder instalar usando el comando `pip`.

Lo primero fue entender la estructura del proyecto.

```
├── dist
├── docs
├── requeriments
└── src
    ├── assets -> ~/proyectos/cmi/src/assets/
    ├── core
    ├── encuestas
    │   ├── migrations
    │   ├── templates
    │   │   └── encuestas
    │   └── templatetags
    ├── sgc_aprobacion.egg-info
    └── templates -> ~/proyectos/cmi/src/templates/
```

Veamos cada uno de los directorios:

+ `dist` - Este directorio se crea automáticamente por `setuptools` cuando se crea el paquete de distribución.
+ `docs` - Contiene los documentos del aplicativo.
+ `requeriments` - Para los archivos de requisitos, por si hay locales y de producción.
+ `src` - Es donde reside el proyecto.
+ `src/assets` - Es un enlace simbólico a los archivos estáticos.
+ `src/core` - Es el proyecto de desarrollo, su función es asegurar que la aplicación funciona.
+ `src/encuestas` - Es el proyecto en cuestión.
+ `sgc_aprobacion.egg-info` - Es un directorio creado por `setuptools` al empaquetar el proyecto.
+ `templates` - Un enlace simbólico a las plantillas.

## El núcleo

En tanto que el proyecto `sgc-aprobacion` funcionará dentro del Cuadro de Mando Integral, tiene que asegurar que las metáforas visuales son las mismas que el núcleo. Por eso se utilizan los archivos del proyecto central, `assets` y `templates` que proporcionan la base para el resto de los proyectos.

En el proyecto `sgc-aprobacion` indicamos dónde encontrar tanto las plantillas como los archivos estáticos en la configuración, `core/settings.py` que solo se utiliza para desarrollo.

```python
from unipath import Path

PROJECT_DIR = Path(__file__).ancestor(2)
STATIC_URL = '/assets/'
STATIC_ROOT = PROJECT_DIR.child("static")
STATICFILES_DIRS = (
    "assets",
)
TEMPLATE_DIRS = (
    "templates",
    PROJECT_DIR.child('encuestas', "templates"),
)
```

Con `PROJECT_DIR` establecemos el directorio del proyecto, relativo a `src/core/settings.py`, por lo que el `ancestor(2)` es, precisamente, `src`. A partir de este directorio, localizamos `STATIC_ROOT`, ubicado en `src/static`. Agregamos a los archivos estáticos, los directorios `assets`, para poder después recopilarlos con `collectstatic`. 

A continuación, lo que resulto una revelación para mi: las plantillas.

Colocamos en `src/templates` las plantillas base, que son comunes para todos los proyectos del __cmi__. Pero las plantillas que usamos en el proyecto quedan en `src/encuestas/templates`. Y en este directorio solo están las plantillas del proyecto, por los estáticos, la base y los auxiliares están en otro proyecto. De ahí la modularidad. Y la velocidad de desarrollo.

Ahora solo hay que preocuparse por el contenido.

## La creación del paquete

Crear una aplicación independiente en Django resultó más simple de lo que pensaba. Usando el paquete `setuptools` solo creé el archivo `setup.py`, dentro del proyecto original.

```python
# -*- coding: UTF-8 -*-

#         app: mx.ine.cmi.aprobacion
#      módulo: setup
# descripción: Instalación del aplicativo
#       autor: Javier Sanchez Toledano
#       fecha: lunes, 13 de abril de 2015


import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='sgc-aprobacion',
    version='1.0-rc1',
    package_dir={'': 'src'},
    packages=['encuestas'],
    include_package_data=True,
    license='MIT License',
    description='Aplicativo para el control del indicador Aprobación Ciudadana.',
    long_description=README,
    url='http://10.69.0.68/',
    author='Javier Sanchez Toledano',
    author_email='javier.sanchezt@example.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2.7.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
```


Aquí no utilizó `unipath` porque no tengo la experiencia suficiente (_todavía_) para modificar esta plantilla.

Es un archivo estándar, que se encuetra en el sitio de Django. Solo hay una importante diferencia.

El sitio de Django menciona que hay que crear otro directorio y mover ahí la aplicación[^1] pero con la línea `package_dir={'': 'src'},` esto no es necesario, ya que su función es indicar que el proyecto está en el directorio `src` pero este, no forma parte del paquete. 

Con este parámetro no hay que mover nada y todo queda en el mismo directorio.

Por último, hay que indicarle a `setuptools` que agregue directorio adicionales, usando el archivo `MANIFEST.in`:

```
include LICENSE
include README.md
recursive-include docs/ *
recursive-include requeriments/ *
recursive-include src/encuestas/templatetags *
recursive-include src/encuestas/templates *
```

Y tenemos listo el proyecto para empaquetarlo y distribuirlo.

---
### Notas

[^1]: Pueden seguir las instrucciones directamente del sitio de Django: [https://docs.djangoproject.com/en/1.8/intro/reusable-apps/](https://docs.djangoproject.com/en/1.8/intro/reusable-apps/)





