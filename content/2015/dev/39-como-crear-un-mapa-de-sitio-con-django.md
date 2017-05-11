Title: Como crear un mapa de sitio con Django
Date: 2013/12/27 03:12
Category: Desarrollo 
Tags: views, sitemap, templates 
Slug: como-crear-un-mapa-de-sitio-con-django
Author: Javier Sanchez Toledano
Summary: 

Inspirado en un artículo anterior sobre como [crear mapas de sitio con WordPress](http://conxb.com/19sblkG) me dispongo a crear la página equivalente para **namespace.mx** que utiliza [Django](/django/). El mapa del sitio es un archivo que contiene enlaces a todas las categorías, a todos los años y meses que contenga el blog, y a las 100 entradas más recientes.

### Definiendo la URL

Empiezo definiendo la <abbr class="initialism" title="Uniform Resource Locator">URL</abbr> del mapa del sitio, y preciso que se encuentre escribiendo `/mapa/` en la barra de direcciones, así que en mi archivo `urls.py` agrego la línea con la expresión regular, la función y nombre para usarla más fácilmente.

    url(r'^mapa/$', 'conxb.views.mapa', name='mapa'),

Agrego un patrón de búsqueda formado por `r('^mapa/$')`, donde la `r` indica que es una cadena `raw`, es decir, sin formato, el símbolo `^` indica en sintaxis <abbr class="initialism" title="RegEx o Expresiones Regulares">regex</abbr> el inicio del patrón y el símbolo `$` indica el fin del dicho patrón de búsqueda.

La función que será llamada cuando se encuentre el patrón es `conxb.views.mapa`, sin argumentos. Tiene atajo, definido en `name='mapa'` que permite usar este atajo con la función `reverse` en una vista o la función `url` en una plantilla o _template_.

### La vista para el mapa

Recordemos que Django funciona bajo un esquema <abbr title="Model-View-Controler o Modelo-Vista-Presentación" class="initialism">MVC</abbr> que separa la definción del objeto, la lógica y la plantilla. En este caso, el modelo es la `Entrada` que ya está definida y debemos generar la _view_ o vista, es decir, la programación que enviaremos a la plantilla.

#### La lista de páginas

Django proporciona un modelo similar a las páginas en [WordPress](/wordpress/) que se llama `flatapages` o páginas simples. Debemos hacer una consulta para saber con qué páginas simples cuenta nuestro blog.

Entonces el primer paso es importar el modelo, que se llama `FlatPage` del módulo `django.contrib.flatpages`, y hacer una consulta para extraer todas las páginas.

    from django.contrib.flatpages.models import FlatPage
    flats = FlatPage.objects.all()

#### La lista de categorías

Repetimos el procedimiento para las categorías, importamos el modelo y creamos una variable con el `queryset` o consulta.

    from blog.models import Categoria
    cats = Categoria.objects.all()

#### Archivos mensuales

Para crear los archivos mensuales usamos el modelo `Entry` que defines las entradas en este blog y obtenemos los meses en los que existen entradas agrupando los resultados. 

Para esto [Django](/django/) proporciona un _manager_ o administrador de consultas muy útil que se llama `dates`. Toma como argumentos el campo que contiene la fecha, que en este caso es `pub_date`; el campo de ordenación, que puede ser anual (`year`), mensual (`year`) y diario (`diario`) y un tercero que es opcional para indicar la ordenación (`order='DESC'`)

    from blog.models import Entry
    meses = Entry.objects.dates('pub_date', 'month', order='DESC')

#### La lista de artículos

Para obtener los 100 posts más recientes, hacemos una nueva consulta al modelo `Entry`, especificando este límite.

La consulta pide que los resultados se ordenen por fecha descendentemente, de ahí el signo menos (`-pub_date`) y dentro por índice de las entradas (`id` o `pk`). Limitamos el número de resultados con notación _slice_.

    entries = Entry.objects.all().order_by('-pub_date','id')[:100]

#### La vista completa

Con estos datos terminados la consulta,  que queda de la siguiente manera. Observa que uso un decorardor `@render_to` de la app `annoying` que ahorra un montón de código.

    # Modulos del blog
    from blog.models import Entry
    from django.contrib.flatpages.models import FlatPage
    from blog.models import Categoria
    # Decorador de views
    from annoying.decorators import render_to

    @render_to('indice/mapa.html')
    def mapa(request):
        flats = FlatPage.objects.all()
        cats = Categoria.objects.all()
        meses = Entry.objects.dates('pub_date', 'month', order='DESC')
        entries = Entry.objects.all().order_by('-pub_date','id')[:100]
        return {'flats': flats, 'cats':cats, 'meses':meses, 'entries':entries}

Y con estos datos pasamos a la plantilla.

### La plantilla del mapa

Para asegurar la consistencia en la presentación de la información y para asegurar una experiencia de usuario coherente con el resto del sitio, iniciamos extendiendo el archivo base y generamos nuestras columnas.

La primera columna, igual que en el ejemplo de [WordPress](/wordpress/) contiene las listas de páginas, categorías y meses.

Usamos ciclos `for` para crear la lista de páginas, como se muestra a continuación, para las páginas. La función `get_absolute_url()` es un estándar en [Django](/django/) para este tipo de vistas. Pero como verás a continuación, yo uso una propia llama `permalink`, aunque su función es la misma.

    <!-- listado de páginas -->
    {% for page in flats %}
    <li><a href="{{page.get_absolute_url}}">{{page.title}}</a></li>
    {% endfor %}

En realidad, todos los listados son iguales, como el de categorías:

    {% for cat in cats %}
      <li><a href="{{cat.permalink}}">{{cat.title}}</a></li>
    {% endfor %}

En el caso de los meses, debemos convertir la fecha en una <abbr class="initialism" title="Uniform Resource Locator">URL</abbr> correcta y usamos el filtro `date` de las plantillas de [Django](/django/).

    {% for mes in meses %}
        <li><a href="{{mes|date:'/Y/m/'}}">{{mes|date:"F \d\e\l Y"}}</a></li>
    {% endfor %}

Y con esto terminamos la columna izquierda de nuestro mapa. 

La columna derecha se forma con el listado de artículos, de forma idéntica a las listas anteriores.

    {% for entry in entries %}
    <li><a href="{{entry.permalink}}">{{entry.title}}</a></li>
    {% endfor %}

El resultado final lo puedes ver en [**el mapa del sitio**](/mapa/).
