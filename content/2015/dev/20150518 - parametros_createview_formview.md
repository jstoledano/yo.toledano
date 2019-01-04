Title: Pasar parámetros con CreateView y ModelForm en Django
Date: 2015-05-18 9:20:48
Category: Desarrollo
Tags:  django, views, patterns, forms
Author: Javier Sanchez Toledano
Summary: Como pasar un parámetro para prellenar el formulario con CreateView y ModelForm.

Estoy re-escribiendo el código de Control de Documento, para asegurar además del cumplimiento de la Norma ISO 9001:2008 y de la 9001:2015, la migración a la versión 1.8 de Django que tiene soporte extendido[^1] y a Python3.

Entonces tomé la decisión de utilizar, cuando sea posible, vistas genéricas basadas en clases. Por ejemplo la `CreateView` y las `ModelForm`.

Para el control de documentos, necesitamos controlar las versiones de los documentos para asegurar que se cuenta con las más actualizadas.

## ModelForm
Lo primero que hice fue crear el formulario a partir del modelo aprovechando la clase `ModelForm`[^2], por ejemplo, para el control de las revisiones, esta es la clase `ModelForm`:


```python
class RevisionForm(forms.ModelForm):
    class Meta:
        model = Revision
        exclude = ('creacion', 'acutaliza', 'autor')
        widgets = {
            'f_actualizacion': forms.TextInput(attrs={'class': 'col s4 datepicker'}),
            'revision': forms.TextInput(attrs={'class': 'input-field col s2'}),
            'cambios': forms.Textarea(attrs={'class': 'materialize-textarea'}),
        }
```

Simplemente agregué los campos que no iba a utilizar, que son solo tres y agrego algunas clases para darle formato al formulario en HTML. Esto simplifica realmente la creación del formulario.

## CreateView
Para gestionar el formulario, use otra función genérica, en este caso es `CreateView`[^3]. Su forma básica es así:

```python
class CrearRevision(CreateView):
    model = Revision
    template_name = 'docs/add_revision.html'
    form_class = RevisionForm
```

Solo tengo que especificar el modelo a utilizar en `model`; la plantilla que quiero utilizar con `template_name`, aunque si no especifico este parámetro podría llamar a mi plantilla `revision_form`. Por último, también especifico que voy a usar la `ModelForm` definida anteriormente, con `form_class`.

Pero también utilizo algunas funciones para ajustar mi formulario.

### Funciones auxiliares

Hayn un campo `documento` que necesito que esté pre-seleccionado para minimizar los errores[^4], para esto utilizo la función `get_initial`:

```python
	def get_initial(self):
	    return {'documento': self.kwargs['num']}
```

También quiero capturar el identificador del documento para utilizarlo en el formulario, y lo obtengo del contexto que se envía a la función:

```python
    def get_context_data(self, **kwargs):
        ctx = super(CrearRevision, self).get_context_data(**kwargs)
        ctx['num'] = self.kwargs['num']
        return ctx
```

Por último, debo agregar el usuario que creo la revisión. Este campo esta desactivado en la `ModelForm`, pero el campo es obligatorio. Le asignamos el valor cuando el formulario sea válido, sobreescribiendo la función `form_valid`:

```python
    def form_valid(self, form):
        from django.core.urlresolvers import reverse
        revision = form.save(commit=False)
        revision.autor = self.request.user
        revision.save()
        return HttpResponseRedirect(reverse('detalle',
            kwargs={'num': self.kwargs['num']}
            )
        )
```

Como pueden ver, las funciones genéricas ahorra mucho trabajo. En el siguiente artículo veremos un ejemplo más extremo con la función `UpdateView`.


### Notas

[^1]: Se dice **LTS** que en inglés es _Long Term Support_.  
[^2]: `django.forms.ModelForm`
[^3]: `django.views.generic.edit.CreateView`
[^4]: Tendría que estar seleccionado y desactivado, pero no he podido desactivarlo con el CSS Framework que estoy utilizando.

