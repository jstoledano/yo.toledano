Title: Extender el modelo de usuario en Django
Date: 2015-08-09 12:42:29 a.m.
Category: Desarrollo
Tags:  django
Author: Javier Sanchez Toledano
Summary: 


Django tiene un modelo de usuario que ofrece muchas funcionalidades. El problema con `User` es que no puede ampliarse para incluir más información. Por ejemplo, para el *Cuadro de Mando Integral* necesitamos saber el sitio en dónde trabajan y el puesto[^1].

El modelo `User` hereda de `AbstractBaseUser` de donde vienen todas sus funciones. Al crear un nuevo modelo `Pipol` y heredar de `AbstractBaseUser`, le damos a nuestro modelo las mismas funciones que `User` (ofuscación de contraseña, manejo de sesiones, etc.) y además le damos la posibilidad de contar con los campos que necesitamos, como `sitio` y `puesto`.

En Django, el concepto de una *«aplicación»* se usa para organizar el código de una manera coherente. Una *app* es un módulo que combina el código de modelos, vistas, serializadores, que están relacionados de alguna manera. Por ejemplo, el primer paso para construir el Cuadro de Mando Integral[^2] será crear una *app* llama `nucleo`. La aplicación `nucleo` será la que contenga el código para el registro de cuentas, registrarse, salir y otra información relevante para el **cmi**.

Creamos entonces nuestra *app* `nucleo` ejecutando el siguiente código:

```language-python
$ python manage.py startapp nucleo
```

El modelo `Pipol`
-----------------

Para empezar, crearemos el modelo `Pipol` que mencionamos antes.

En el editor de nuestra preferencia[^3] abrimos el archivo `core/models.py` y lo editamos para que quede como sigue[^4]:

```language-python
# -*- coding: UTF-8 -*-

#         app: mx.ine.cmi
#      módulo: core
# descripción: Núcleo del CMI
#       autor: Javier Sanchez Toledano
#       fecha: sábado, 11 de abril de 2015

from django.contrib.auth.models import AbstractBaseUser
from django.db import models

class Pipol(AbstractBaseUser):
    '''
    Clase para gestionar los usuarios del cuadro de mando integral.
    Incluye la posibilidad de incluir otras entidades y poder filtrar
    de acuerdo con ello.
    '''
    ENTIDADES = (
        (29, 'Tlaxcala'),
    )
    SITIOS = (
        (0, 'Junta Local'),
        (1, '01 Junta Distrital'),
        (2, '02 Junta Distrital'),
        (3, 'O3 Junta Distrital')
    )

    VEL = 'VEL'
    VSL = 'VSL'
    VRL = 'VRL'
    VOL = 'VOL'
    VCL = 'VCL'
    VED = 'VED'
    VSD = 'VSD'
    VRD = 'VRD'
    VOD = 'VOD'
    VCD = 'VCD'
    JMM = 'JMM'
    JOSA = 'JOSA'
    JOCE = 'JOCE'
    RA = 'RA'

    PUESTOS = (
        (VEL, 'Vocal Ejecutivo de Junta Local'),
        (VSL, 'Vocal Secretario de Junta Local'),
        (VRL, 'Vocal del RFE de Junta Local'),
        (VCL, 'Vocal de Capacitación de Junta Local'),
        (VOL, 'Vocal de Organización de Junta Local'),
        (VED, 'Vocal Ejecutivo de Junta Distrital'),
        (VSD, 'Vocal Secretario de Junta Distrital'),
        (VRD, 'Vocal del RFE de Junta Distrital'),
        (VCD, 'Vocal de Capacitación de Junta Distrital'),
        (VOD, 'Vocal de Organización de Junta Distrital'),
        (JOSA, 'JOSA'),
        (JMM, 'Jefe de Monitoreo a Módulos'),
        (JOCE, 'Jefe de Cartografía'),
        (RA, 'Rama Administrativa')
    )

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=40, unique=True)

    nombre = models.CharField(max_length=40, blank=True)
    paterno = models.CharField(max_length=40, blank=True)
    materno = models.CharField(max_length=40, blank=True)
    tagline = models.CharField(max_length=40, blank=True)

    is_admin = models.BooleanField(default=False)

    entidad = models.PositiveSmallIntegerField(default=29, choices=ENTIDADES)
    sitio = models.PositiveSmallIntegerField(choices=SITIOS, blank=True, null=True)
    puesto = models.CharField(max_length=4, choices=PUESTOS, blank=True, null=True)
    is_mspe = models.BooleanField(default=False)
    is_activo = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = PipolManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __unicode__(self):
        return self.email

    def get_full_name(self):
        return ' '.join([self.nombre, self.paterno, self.materno])

    def get_short_name(self):
        return self.nombre

```

Ahora vamos a ver un poco más a detalle este modelo.

```
    email = models.EmailField(unique=True)

    # ...

    USERNAME_FIELD = 'email'
```

El modelo `User` predeterminado de Django *necesita* un nombre de usuario. Este se utiliza para registrar el ingreso de los usuarios. Pero en el __cmi__ utilizaremos el correo institucional para este propósito.

Para indicarle a Django que utilice el correo como nombre de usuario en este modelo, establecemos el atributo `USERNAME_FIELD` como `email`. Este campo debe ser único, así que creamos el campo con el argumento `unique=True`.

Y aunque vamos a ingresar al __cmi__ con el correo, todavía necesitamos un nombre de usuario (o _username_) para mostrarlo en las metas o en la URL del perfil de usuario[^5], por lo tanto debe ser único.

```
    username = models.CharField(max_length=40, unique=True)
```

También vamos a colocar más información personal sobre nuestros usuarios. Pero para practicidad o para que los usuarios se sientan más confortables vamos a permitir que estos campos queden en blanco.

```
    nombre = models.CharField(max_length=40, blank=True)
    paterno = models.CharField(max_length=40, blank=True)
    materno = models.CharField(max_length=40, blank=True)
```

Como ya habíamos dicho, debemos establecer cierta información para ubicar a los usarios, por esta razón incluímos los siguientes campos.

```
    sitio = models.PositiveSmallIntegerField(choices=SITIOS)
    puesto = models.PositiveSmallIntegerField(choices=PUESTOS)
    is_mspe = models.BooleanField(default=False)
```

Y por razones de trazabilidad, agregamos dos campos en el perfil. El primero `created_at` guarda de forma automática la fecha de creación del usuario y `updated_at` guarda automáticamente la fecha y hora de la modificación más reciente.

```
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

La diferencia entre `auto_now_add` y `auto_now` es que una vez que se agrega información en `auto_now_add` ya no puede modificarse y `auto_now` se modifica cada vez que se edita el perfil.

Cuando queremos obtener una instancia de algún mode en Django, usamos una expresión tipo `Modelo.objects.get(**kwargs)`. El atributo `objects` es una clase `Manager` que por lo general se escribe como `<modelo>Manager`. En nuestro caso creamos la clase `PipolManager`, que veremos más adelante.

```
    objects = PipolManager()
```

Vamos a usar el nombre de usuario en muchos lados. También necesitamos saber _forzosamente_ el sitio y el puesto de los usuarios. Normalmente utilizaríamos el parámetro `required=True` pero como estamos reemplazando al modelo `User` necesitamos especificar los campos obligatorios:

```
    REQUIRED_FIELDS = ['username', 'sitio', 'puesto']
```

Cuando trabajamos en el shell, como veremos próximamente, la representación en texto de un objeto `Pipol` aparece como `<Pipol: Pipol>`, pero como hay muchas personas en el __cmi__ esto no resulta muy práctico.  Pero podemos sobreescribir el método `__unicode__()` para cambiar el comportamiento estándar. En el __cmi__ vamos a mostrar el correo electrónico de los usuarios, por lo que la representación del objeto `Pipol` se vería así: `<Pipol: javier@example.com`.

```
    def __unicode__(self):
        return self.email
```

Las funciones `get_full_name()` y `get_short_name()` están predeterminadas en Django. No las vamos a usar, pero de todos modos es una buena idea asegurarnos que funciones de una manera coherente con el __cmi__.

```
    def get_full_name(self):
        return ' '.join(self.nombre, self.paterno, self.materno)

    def get_short_name(self):
        return self.nombre
```

En el próximo artículo veremos como crear el administrador de objetos para el modelo `Pipol`.


### Actualización

> Tuve que hacer algunos cambios porque al probar el código no funcionó. Quería que `entidad`, `sitio` y `puesto` fueran obligatorios, pero no pude crear objetos así. Tuve que migrar el modelo para hacer estos campos opcionales. Además coloqué las constantes de `CHOICES` __dentro__ del modelo.

---

### Notas

[^1]: Creo que a través del puesto puedo determinar si es miembro del servicio profesional, pero como no he resuelto la forma de hacerlo, agregué un campo lógico.

[^2]: En adelante al *Cuadro de Mando Integral* lo llamaremos solo **cmi**.

[^3]: Yo uso [Atom](http://j.mp/1clPzBh), que es gratuito y libre.

[^4]: Creo que estoy usando otros nombres, pero la idea es la misma.
