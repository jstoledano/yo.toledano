Title: Cómo hacer un gestor de objetos en Django
Date: 2015-08-09 12:42:57 a.m.
Category: Desarrollo
Tags:  django, models
Author: Javier Sanchez Toledano
Summary: 


Como recordarán en el [artículo anterior](http://t.co/r9hSSyX6MW) vimos como crear un modelo de usuario con algunas características agregadas al modelo estándar de Django.

Cuando sustituímos el modelo `User` por uno creado a nuestras necesidades, debemos definir un gestor relacionado, es decir una clase `Manager` que sobreescriba las funciones de `create_user` y `create_superuser`.

Dentro del archivo `nucleo/models.py`, agregamos el siguiente código, __antes__ de la clase `Pipol`.

```python
from django.contrib.auth.models import BaseUserManager

class PipolManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError(
                'Los usuarios deben tener una dirección de correo válida.'
            )

        if not kwargs.get('username'):
            raise ValueError(
                'Los usuarios deben tener un nombre de usuario válido.'
            )

        if not kwargs.get('entidad'):
            raise ValueError('Debe seleccionar una entidad.')

        if not kwargs.get('sitio'):
            raise ValueError('Debe seleccionar una junta.')

        if not kwargs.get('puesto'):
            raise ValueError('Debe seleccionar un puesto.')

        pipol = self.model(
            email=self.normalize_email(email), username=kwargs.get('username')
        )

        pipol.set_password(password)
        pipol.save()

        return pipol

    def create_superuser(self, email, password, **kwargs):
        pipol = self.create_user(email, password, **kwargs)

        pipol.is_admin = True
        pipol.save()

        return pipol
```

Ahora analizaremos esta clase línea por línea.

```python
        if not email:
            raise ValueError(
                'Los usuarios deben tener una dirección de correo válida.'
            )

        if not kwargs.get('username'):
            raise ValueError(
                'Los usuarios deben tener un nombre de usuario válido.'
            )
```

Ya que se requiere que los usuarios tengan un correo y un nombre de usuario, debemos lanzar un error si falta alguno de estos atributos.

```python
        if not kwargs.get('entidad'):
            raise ValueError('Debe seleccionar una entidad.')

        if not kwargs.get('sitio'):
            raise ValueError('Debe seleccionar una junta.')

        if not kwargs.get('puesto'):
            raise ValueError('Debe seleccionar un puesto.')
```

Y ya que definimos que la entidad, el sitio y el puesto son obligarios, lanzamos errores cuando no se definen estos valores.

```python
        pipol = self.model(
            email=self.normalize_email(email), username=kwargs.get('username')
        )
```

También debemos definir el modelo para la clase `PipolManager`, usando `self.model` que se refiere al modelo definido en `BaseUserManager` de forma predeteriminada. Este comportamiento estándar está definido en `settings.AUTH_USER_MODEL`, el cual cambiaremos en un momento, más adelante.

```python
        pipol = self.create_user(email, password, **kwargs)

        pipol.is_admin = True
        pipol.save()
```

Para no violar el principio DRY[^1] de Django, para crear al administrador con `create_superuser`, simplemente dejamos que `create_user` se encargue de esta función y libera a `create_superuser` que solo se ocupa de marcar un objeto `Pipol` como administrador.

## Confirgurar `AUTH_USER_MODEL`

Aunque tengamos nuestro modelo `Pipol`, cuando usemos el comando `python manage.py createsuperuser` se seguirá creando un modelo `User`, porque hasta este moemnto, Django no sabe que vamos a usar otro modelo para manejar nuestras cuentas.

Para definir este comportamiento debemos actualizar el valor de `settings.AUTH_USER_MODEL`, agregando esta línea en el archivo de configuración, que en nuestro caso está en `cmi/settings/base.py`.

```
AUTH_USER_MODEL = 'nucleo.Pipol'
```


---
### Notas

[^1]: DRY es _Don't Repeat Yourself_ algo así como _No seas repetitivo_.
