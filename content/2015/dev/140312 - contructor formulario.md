Title: Excluir el campo de un formulario al llamarlo
Date: 2014/03/12 10:23
Category: Desarrollo
Tags: django, python, forms
Slug: excluir-campo-formulario
Author: Javier Sanchez Toledano
email: javier@namespace.mx
Summary: Como excluir el campo de un formulario al llamarlo desde una vista

Este es mi problema. Hice un formulario para editar los usuarios y al mismo tiempo crear un registro en otro modelo. Es que no encontré otra forma para manejar los permisos de la aplicación `metas` del Cuadro de Mando.

Este es el modelo para los usuarios que usan las metas:

```python
class Pipol(models.Model):
    perfil = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='pipol', editable=False)
    sitio = models.IntegerField(choices=SITIO)
    puesto = models.CharField (choices=PUESTOS, max_length=5)
    activo = models.BooleanField(default=True)

    def __unicode__ (self):
        return str(self.perfil)

    def get_sitio (self):
        return SITIO[self.sitio][1].upper()

    def is_mspe(self):
        if self.puesto == "RA":
            return False
        else:
            return True

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'
```

Como pueden ver, usa una clave foránea que enlaza a los usuarios del sistema para controlar grupos y permisos.

Entonces, cuando se trata de agregar a los usuarios uso un formulario que toma ciertos campos para el modelo `django.contrib.auth.models.Users`y estos campos en este modelo `Pipol`.

Entonces debo agregar un constructor para que cuando se trate de agregar a un usuario se agreguen los campos `password1` y `password2` y cuando se edite, estos campos se exluyan.

El constructor es como esto:

```python
def __init__ (self, *args, **kwargs):
    edit = kwargs.pop('edit', None)
    super (PipolForm, self).__init__(*args, **kwargs)
    if edit:
        del self.fields['password1']
        del self.fields['password2']
```

De forma que tendría que llamar a mi formulario el parámetro `con_clave=False` para que no aparezcan las contraseñas.

La llamada en la vista es como sigue:

```python
form = PipolForm (request.POST, initial=inital, edit=True)
```

No funciona como yo quiero, así que seguiré investigando.
