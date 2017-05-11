Title: Configurar Django con LiteSpeed
Date: 2013/11/18 19:26
Category: Desarrollo 
Tags: admin, linux 
Slug: configurar-django-con-litespeed
Author: Javier Sanchez Toledano
Summary: 

Para poder usar Django con LiteSpeed, la mejor configuración que encontré fue con `ajp-wsgi`. Este programa[^1] es un servidor WSGI, escrito enteramente en C, implementa una compuerta tipo AJP[^2] entre el servidor y Django que incorpora al intérprete Python[^3], por lo que es más rápido que implementaciones hechas solo en Python.

Para poder compilarlo necesitamos el paquete de desarrollo de Python y el paquete básico de desarrollo de Ubuntu.

    sudo apt-get install python-pip python-dev build-essential

A continuación bajamos las fuentes del servidor AJP más recientes, las desempaquetamos, configuramos y realizamos la compilación.

    wget http://www.saddi.com/software/ajp-wsgi/dist/ajp-wsgi-1.1.tar.bz2
    tar xvfj ajp-wsgi-1.1.tar.bz2
    cd ajp-wsgi-1.1/
    python configure.py
    make
    sudo cp ajp-wsgi /usr/local/bin/

Luego creamos el archivo `run_ajp.py` que crea el servidor WSGI de Django.

    #!/usr/bin/env python
    # run_ajp.py
    import os
    os.environ["DJANGO_SETTINGS_MODULE"]="conxb.settings"

    from django.core.handlers.wsgi import WSGIHandler
    app = WSGIHandler()

Por último, creamos un archivo para ejecutarlo fácilmente.

    #!/usr/bin/env bash
    cd /home/javier/conxb.com/sitio
    /usr/local/bin/ajp-wsgi run_ajp app -B -l /dev/null

Nota que enviamos la salida al vacío (`/dev/null`) porque un sitio en producción puede crear un registro de cientos de megas de espacio. Pero si estás haciendo pruebas, enviar el registro a un archivo log puede ayudarte a encontrar errores.

Una forma de mejorar este archivo[^4] sería crear un guión de arranque que lance el `run_ajp.py` cada vez que se reinicia el servidor o bien una entrada cron que verifique cada cierto tiempo que el servidor se esté ejecutando y tome acciones al respecto.

Pero eso será tema para otro artículo.

[^1]: El autor es Allan Saddi, lo encuentran aquí: http://goo.gl/4v8jq
[^2]: Por si les interesa, la referencia al protocolo AJP de Apache: http://goo.gl/UzYPQ
[^3]: La propuesta 333 explica esta interface: http://goo.gl/vZPec
[^4]: La guía original es de LiteSpeed Tech: http://goo.gl/aA2Aa
