Title: La nueva configuración de plantillas en Django
Date: 2015-08-09 12:43:36 a.m.
Category: Desarrollo 
Tags:  django
Author: Javier Sanchez Toledano
Summary: 



Hoy inicié un proyecto completamente nuevo en Django usando la versión **1.8 LTS**, pero copié la configuración de otro proyecto anterior y me llevé una sorpresa.

En realidad solo utilicé la configuración de directorios de plantillas, archivos estáticos y el directorio media, pero el error era que no encontraba las plantillas.

Esta es la configuración que sabe en versiones anteriores a la 1.8 de Django:

    from unipath import Path

    PROJECT_DIR = Path(__file__).ancestor(2)
    MEDIA_ROOT = PROJECT_DIR.child("media")
    STATIC_URL = '/assets/'
    MEDIA_URL = '/media/'
    STATIC_ROOT = PROJECT_DIR.child("static")
    STATICFILES_DIRS = (
        "assets",
    )
    TEMPLATE_DIRS = (
        "templates",
        PROJECT_DIR.child('encuestas', "templates"),
    )

    DEBUG = True
    TEMPLATE_DEBUG = True
    ALLOWED_HOSTS = []

Y esta era la que intentaba usar con el nuevo proyecto:

    PROJECT_DIR = Path(__file__).ancestor(2)
    MEDIA_ROOT = PROJECT_DIR.child("media")
    STATIC_URL = '/assets/'
    MEDIA_URL = '/media/'
    STATIC_ROOT = PROJECT_DIR.child("static")
    STATICFILES_DIRS = (
        "assets",
    )
    TEMPLATE_DIRS = (
        "templates",
        PROJECT_DIR.child('encuestas', "templates"),
    )

    DEBUG = True
    TEMPLATE_DEBUG = True
    ALLOWED_HOSTS = []

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

Lo que me parecía más raro era que si quitaba la variable `TEMPLATES` todo funcionaba de nuevo, pero no era el caso, no entendía por qué.

Lo que ocurre es que la configuración de las plantillas cambió en Django 1.8 porque ahora permite utilizar otros motores para plantillas. Por ahora solo sé de *Jinja 2*, pero uno puede escribir su propio motor.

Entonces cambió la configuración de los directorios dónde buscar las plantillas, que es una clave `DIRS` en el diccionario `TEMPLATES` y ahí es donde colocamos los valores que antes iban en TEMPLATE_DIRS.

    from unipath import Path

    PROJECT_DIR = Path(__file__).ancestor(2)
    MEDIA_ROOT = PROJECT_DIR.child("media")
    STATIC_URL = '/assets/'
    MEDIA_URL = '/media/'
    STATIC_ROOT = PROJECT_DIR.child("static")
    STATICFILES_DIRS = (
        "assets",
    )

    ...

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
                "templates",
                PROJECT_DIR.child('money', "templates"),
            ],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]
