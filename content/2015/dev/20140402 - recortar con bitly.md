Title: Recortar URL con Bitly
Date: 2014/04/02 10:44
Category: Desarrollo
Tags: tools
Slug: recortar-url-con-bitly
Author: Javier Sanchez Toledano
email: javier@namespace.mx
Summary: Cómo recortar direcciones URL usando Bitly en Django

<img src=“https://s3.amazonaws.com/nspace.mx/assets/img/django.jpg alt="Django" title="Django">

[bitly.com][1] es un servicio de acortador de URL o direcciones, lo que significa que una dirección web puede compartirse fácilmente a través de redes sociales o mensajes de texto. **bitly** además características realmente impresionantes:

* Puedes usar tu propio dominio para los enlaces.
* Puedes usar su potente interface de programación.
* Genera detalladas estadísticas del uso de tus enlaces.

Por ejemplo, la dirección de este artículo es `https://namespace.mx/django/recortar-url-con-bitly/` puede acortarse `http://bitly.com/1lCdYEN` o incluso a `http://j.mp/1lCdYEN` lo que significa una reducción de 51 caractéres a __solo 19 caracteres__, esto es: _62% menos_. Si tienes un límite de caracteres como en Twitter, este ahorro es muy importante.

## Usar Bitly en Django

Para usar la API de Bitly en Django, seleccioné el módulo [`python-bitly`][2] que permite aprovechar todo el potencial de la API en tu sitiio web. Las posibilidades son enormes, pero en esta ocasión solo veremos como recortar las URL de nuestro artículo al momento de guardar.

## Configurando `python-bitly`

Para configurar el módulo necesitamos primero una cuenta de __bitly.com__ y un clave para usar su API. Esta clave la obtenemos en este enlace `https://bitly.com/a/oauth_apps`. Una vez que tenemos nuestra cuenta y nuestra clave, debemos instalar el módulo, con `pip`:

    :::Bash
    (nspace)namespace:~ javier$ pip install django-bitly
    Downloading/unpacking django-bitly
      Downloading django-bitly-0.7.tar.gz
      Running setup.py egg_info for package django-bitly

    Installing collected packages: django-bitly
      Running setup.py install for django-bitly

    Successfully installed django-bitly
    Cleaning up...

Una vez instalada, debemos guardar esta clave en una variable de entorno o en nuestro archivo de configuración, para poder usarlo más adelante.

## El modelo `Entry`

Nuestro modelo requiere de una actualización para agregar un nuevo campo `bitly` que es de la clase `URLField`. No queremos editarlo, todo es automático, por lo que no aparece siquiera en los formularios.

    :::Python
    bitly = models.URLField(editable=False, blank=True)

También debemos asegurarnos que en nuestro modelo exista la función `gent_absolute_url()` porque el módulo `python-bitly` la usa automáticamente. Yo la definí de esta manera:

    :::python
    def get_absolute_url (self):
        return "https://namespace.mx/%s/%s/" % (self.category.slug, self.slug)

Ahora, debemos de modificar el método `save()` de nuestro modelo para que cuando se guarde una entrada, se actualice la URL recortada.

### Crear una conexión con Bitly

Lo primero que tenemos que hacer es crear una conexión con bitly. El código para crear el objeto, es como sigue

    :::Python
    import bitly_api
    access_token = os.getenv(BITLY_ACCESS_TOKEN)
    bitly = bitly_api.Connection(access_token=access_token)

Es decir, primero importamos el módulo, luego ponemos la clave de la API en una variable local y a continuación creamos el objeto `bitly` con el método `Connection`.

Ahora podemos crear la URL corta usando la propiedad `get_absolute_url` que, haciendo la sustición respectiva, es algo como esto:

    :::Python
    data = bitly.shorten("https://namespace.mx/%s/%s/" % (self.category.slug, self.slug))

Esta variable `data` la guardamos en nuestra entrada, en el campo bitly, que ya creamos y podemos usarla en nuestro sitio muy fácil y rápidamente:

    :::Jinja2
    <link rel="shortlink" type="text/html" href="{{ article.bitly }}">

[1]:http://bitly.com
[2]:http://j.mp/ns-bitly_api
