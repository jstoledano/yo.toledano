Title: Crear plantillas modulares con Jinja2  
Date: 2014/02/16 12:17  
Category: Desarrollo  
Tags: jinja2, html5, python
Slug: jinja2-modular-templates  
Author: Javier Sanchez Toledano  
Summary: Como crear plantillas modulares con Jinja2  

[Jinja2][jinja] es un motor de renderizado de plantillas desarrollado en Python diseñado para ser flexible, rápido y seguro. Si conoces como usar las plantillas de [Django][django] entonces ya conoces lo suficiente para empezar a utilizar Jinja2. Este sistema de plantillas es también utilizado por [Pelican][pelican], el generador de contenido estático que utiliza este blog.


### Funcionamiento básico de Jinja2 con Pelican

La forma más simple de instalar **Jinja2** es usando el programa `pip`:

    :::bash
    (pelican)namespace:docs javier$ pip install jinja2

La forma más básica para usar Jinja2 es usando la clase `jinja2.Template`.

    :::Python
    In [1]: from jinja2 import Template
    In [2]: template = Template('Hola {{ nombre }}!')
    In [3]: template.render(nombre='Javier Sanchez')
    Out[3]: u'Hola Javier Sanchez!'

Las etiquetas de **Jinja2** se identifican con corchetes. Los corchetes dobles identifican variables `{{ variable }}`. Estas variables se encuentran en el *contexto* con el que se llama a la plantilla. Las expresiones se colocan entre corchetes y signos de porcentaje: `{% expresion %}`.

Vamos a ver un ejemplo mínimo de una plantilla o *template* y poco a poco iremos ampliando este ejemplo hasta terminar con la plantilla que usa este blog.

    :::jinja
    <!DOCTYPE html>
    <html lang="es_MX">
      <head>
        <title>namespace.mx - Hablamos de Desarrollo Web</title>
      </head>
      <body>
        <ul id="navigation">
          {% for opcion in menu %}
            <li><a href="{{ opcion.url }}">{{ opcion.titulo }}</a></li>
          {% endfor %}
        </ul>

        <h1>namespace</h1>
        {{ una_variable }}
      </body>
    </html>

**Pelican** pasa las variables a las plantillas para poder usarlas en la plantilla. Las variables en mayúsculas del archivo de configuración `pelicanconf.py` además de la lista de artículos, categorías y etiquetas. En el contexto de un artículo individual, también se incluye la variable artículo con las propiedades del encabezado del artículo y el contenido.

Podemos acceder a las propiedades de las variables usando la sintaxis de punto (`variable.propiedad`) o la sintaxis llamada *subscript* (`[]`). Por ejemplo los siguientes ejemplos hacen lo mismo.

    :::jinja
    {{ foo.bar }}
    {{ foo['bar']}}

!!! alert-info "Implementación"
    Aunque de hecho, ambas opciones hacen lo mismo, en la parte de Python el funcionamiento es ligeramente diferente. En el caso de  `foo.bar`:

    * si no lo hay, verifica si hay un *atributo* `bar` en `foo`,
    * verifica si existe un elemento `'bar'` en `foo`,
    * si no existe regresa un objeto indefinido

    Por otro lado, en el caso de `foo['bar']` aunque pasa básicamente lo mismo, ocurre en otro orden:

    * verifica si existe un elemento `'bar'` en `foo`,
    * si no lo hay, verifica si hay un *atributo* `bar` en `foo`,
    * si no existe regresa un objeto indefinido

    Esto es importante por si un objeto tiene un elemento y un atributo con el mismo nombre. Adicionalmente existe la función `attr` que busca atributos dentro de la variable.

## Uso de Jinja2 en Pelican

Lo primero que ocurre cuando Pelican inicia el procesamiento del sitio lee las variables del archivo de configuración, luego los archivos para extraer los metadatos, e inicia la generación del sitio utilizando las plantillas con Jinja2.

Para facilitar el procesamiento, usamos una plantilla básica que contiene la estructura común del sitio y los bloques que usamos en los diferentes tipos de plantillas.

Veamos entonces la primera plantilla de nuestro sitio.

### La plantilla base

Vamos a mostrar el archivo base, por partes para revisar detalladamente los bloques que contiene.

#### Encabezado

Este es el encabezado:

    :::jinja
    <!DOCTYPE html>
    <html lang="es_MX">
      <head>
        {# Mobile First #}
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        {# Meta informacion del sitio #}
        <title>{% block title %}{{ SITENAME }}{% endblock title %}</title>
        <meta name="description" content="{% block meta_description %}{{ DESCRIPCION }}{% endblock meta_description %}">
        <meta name="keywords" content="{% block metakeywords %}{{ METAKEYS }}{% endblock metakeywords %}">
        <meta name="author" content="{{ AUTHOR }}">

        {% block meta_header %}{% endblock meta_header %}

        {% block metagoogle   %}{% endblock metagoogle   %}
        {% block metafacebook %}{% endblock metafacebook %}
        {% block metatwitter  %}{% endblock metatwitter  %}
        {% block metaheader   %}{% endblock metaheader   %}

        {# El tema nspace que nos ocupa #}
        <link href="/assets/css/nspace.css" rel="stylesheet">

        {% include "modules/ie8.html" %}
        {% include "modules/icons.html" %}
        {% include "modules/feeds.html" %}
      </head>

Esta plantilla está codificada en HTML5, y podemos apreciar el uso de comentarios (`{# Mobile First #}`), que ayudan a comprender el código pero no son procesados por Jinja2.

También podemos observar el bloque `{% block title %}{{ SITENAME }}{% endblock title %}` que contiene la variable `{{ SITENAME }}`.

!!! alert-success "Los bloques"
    Los bloques son una de las funciones principales de las plantillas de **Jinja2** ya que nos permiten crear la *modularidad* que queremos para nuestro tema. Los bloques **marcan** lugares que podemos llenar con contenido. Los bloques pueden tener contenido predefinido y usarlos automáticamente.

    Su funcionamiento es similar al de los *hooks* o ganchos en otros sistemas de plantillas como WordPress. Marcamos los ganchos y los utilizamos con variables que dependen del contexto de la plantilla utilizada.


Al final de este segmento podemos apreciar la característica que complementa a nuestro tema modular, la _inclusión_ de archivos. De este modo un tema que puede ser muy grande y complejo se subdivide en partes más pequeñas y manejables.

Usando estos _includes_ y las variables globales podemos crear temas que nos sirvan para diferentes sitios cambiando solo algunas partes muy específicas.

Conforme avance nuestro estudio de __Pelican__ veremos estos módulos más a detalle.

[jinja]: http://j.mp/ns-jinja
[django]: http://j.mp/ns-django
[pelican]: http://j.mp/ns-pelican
