Title: Serializar modelos en Django con REST Framework  
Date: 2015-04-12 12:42:30  
Category: Desarrollo  
Tags:  django, rest, cmi, angularjs    
Author: Javier Sanchez Toledano  
Summary: Cómo transfomar modelos de Django en objetos JSON por medio de la serialización.  

El __cmi__ será una aplicación basada en Django de una sola página, utilizando __AngularJS__, un _framework_ con el que haremos las solicitudes AJAX al servidor para obtener los datos que mostraremos en la página web. Antes de poder enviar los datos al cliente, necesitamos darles un formato que el cliente pueda entender; en este caso, utilizaremos JSON. 

El proceso de transformar los modelos de Django en JSON se llama _serialización_ y es de lo que se trata este artículo.

El modelo que vamos a serializar se llama `Pipol`, el serializador que vamos acrear se llamará `PipolSerializer`.

## Django REST Framework

Django __REST Framework__ es un conjunto de herramientas que proporcionan un conjunto de características para muchas aplicaciones web, incluyendo los serializadores. Vamos a usar estas características en el _cmi_ para ahorrarnos trabajo y frustraciones. 

Para instalar Django REST Framework ejecutamos el comando `pip`:

```bash
$ pip install djangorestframework
```

Creamos el archivo `core/serializers.py` y agregamos el siguiente código:

```python
# -*- coding: UTF-8 -*-

#         app: mx.ine.cmi
#      módulo: core.serializers
# descripción: Serializadores para control de usuarios
#       autor: Javier Sanchez Toledano
#       fecha: domingo, 12 de abril de 2015


from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers
from .models import Pipol


class PipolSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Pipol
        fields = ('id', 'email', 'username', 'created_at', 'updated_at',
                  'nombre', 'paterno', 'materno', 'tagline', 'entidad',
                  'sitio', 'puesto', 'is_mspe', 'is_activo', 'password',
                  'confirm_password')

        def create(self, datos_verificados):
            return Pipol.objects.create(**datos_verificados)

        def update(self, instance, datos_verificados):
            instance.username = datos_verificados.get('username', instance.username)
            instance.tagline = datos_verificados.get('tagline', instance.tagline)

            instance.save()

            password = datos_verificados.get('password', None)
            confirm_password = datos_verificados('confirm_password', None)

            if password and confirm_password and password == confirm_password:
                instance.set_password(password)
                instance.save()

            update_session_auth_hash(self.context.get('request'), instance)

            return instance

```

Analicemos el código línea por línea:

```python
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)
```

En lugar de incluir el campo `password` en la tupla `fields`, como vermos más adelante, definimos explícitamente el campo al principio de la clase `PipolSerializer`. La razón para hacer esto es que asi podemos pasar el atributo `required=False`. Cada campo en `fields` es obligatorio, pero no queremos actualizar la contraseña a menos que proporcionemos una nueva.

`confirm_password` es similar a `password` y se usa para asegurarnos que no tenemos errores al escribir la contraseña.

Fíjate en el argumento `write_only=True`. El password del usuario, aunque se haya _ofuscado_ y _salteado_[^1], __no debe ser visible__ para el cliente en la respuesta de AJAX.

```python
    class Meta:
```

La subclase `Meta` define los metadatos que el serializador necesita para operar.

```python
        fields = ('id', 'email', 'username', 'created_at', 'updated_at',
                  'nombre', 'paterno', 'materno', 'tagline', 'entidad',
                  'sitio', 'puesto', 'is_mspe', 'is_activo', 'password',
                  'confirm_password')
```

El atributo `fields` de la clase `Meta` es dónde especificamos cuales atributos del modelo `Pipol` vamos a _serializar_. Debemos tener mucho cuidado con la selección de estos porque algunos campos, como `is_superuser`, no deben estar disponibles para el cliente por razones de seguridad.




---
### Notas

[^1]: _hashed and salted_. No hay una forma fácil de traducir esto, pero estas dos actividades se utilizan para ofuscar la contraseña de modo que nadie, excepto el usuario, pueda conocerla. De hecho no se compara la contraseña que se escribe con la almacenada (porque no está almacenada), sino que se ofusca la contraseña escrita y se compara con la huella almacenada.