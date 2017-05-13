Title: Vistas Basadas en Clases
Date: 2013/11/27 15:43
Category: Desarrollo 
Tags: patterns, python, views, django
Slug: vistas-basadas-en-clases
Author: Javier Sanchez Toledano
Summary: 

Cuando Django se actualizó a la versión 1.5, reescribí las vistas del blog[^1] para pasarlas al tipo CBV (*Class Based Views*) o **Vistas Basadas en Clases**, por lo menos las que generaban listas (archivo; por día, mes y año; por categoría y por etiqueta) y la de entradas individuales.

[^1]: En ese tiempo el blog era ConxB, que ya no está operativo. Nada está perdido, __namespace.mx__ recibirá todo el contenido del blog anterior.

Las CBV son geniales porque simplifican la forma en que operamos nuestro código, por ejemplo, la siguiente es la CBV para las entradas individuales.

```python
class EntradaIndividual(DateDetailView):
    date_field ="pub_date"
    model = Entry
    slug_field = 'slug'
    template_name = 'blog/single.html'
```

Pero hay muchas CBV genéricas y conviene que las conozcas todas, por lo que a continuación encontrarás una lista. Recuerda que todas pertenecen a `django.views.generic` y debes incluir ese _namespace_ al importarlas.

|Nombre|Descripción                              |Ejemplo de Uso   |
|------|-----------------------------------------|-----------------|
|`View`|Base genérica que puede usarse para todo|Página de archivo|
|`RedirectView`|Redirecciona al visitante a otra página|Un acortador de direcciones|
|`TemplateView`|Muestra una plantilla|Una página estática, como 'politicas.html'|
|`ListView`|Lista de objetos en un `queryset`|Una página de categorías|
|`DetailView`|Muestra un objeto|Un artículo individual|
|`FormView`|Clase para enviar formularios|Un formulario de contacto|
|`CreateView`|Crea un objeto|Formulario para crear un artículo|
|`UpdateView`|Actualiza un objeto|Actualizar un artículo en el blog|
|`DeleteView`|Borra un objeto|Borrar un registro en la base de datos|
|Vistas genéricas basadas en fechas|Para mostrar artículos basados en fecha|En un blog basado en fechas|

La portada de este blog usa una `ListView` muy simple pero a la vez muy poderosa, porque con solo tres líneas son necesarias para crear la portada con todo y paginación:

```python
class BlogArchivo(ListView):
    queryset = Entry.objects.order_by('-pub_date', 'id')
    paginate_by = 6
    template_name = 'portada.html'
```

Por otro lado, las categorías también utilizan esta vista `ListView` pero algo más compleja, porque utilizan una variable para generar el `queryset`:

```python
class CategoriaList(ListView):
    paginate_by = 5
    template_name = "categoria.html"
    make_object_list = True
    context_object_name = 'categoria_list'

    def get_queryset(self):
        self.cat = get_object_or_404(Categoria, slug=self.args[0])
        return Entry.objects.filter(category=self.cat).order_by('-pub_date', 'id')

    def get_context_data(self, **kwargs):
        context = super(CategoriaList, self).get_context_data(**kwargs)
        context['cat'] = self.cat
        return context
```

En artículos posteriores veremos en detalle cada una de estas clases.
