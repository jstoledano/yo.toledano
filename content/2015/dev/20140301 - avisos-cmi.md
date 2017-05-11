Title: Implementación de un sistema de avisos
Date: 2014/03/01 13:31
Category: Desarrollo
Tags: cmi2014, blogging, patterns
Slug: sistema-de-avisos-01
Author: Javier Sanchez Toledano
email: javier@namespace.mx
Summary: Inicia la implementación del sistema de avisos para el cuadro de mando 2014.

La primera aplicación que agregamos al Cuadro de Mando 2014[^1] es `avisos`. La función es muy simple y es dar a conocer información relevante sobre el sistema de gestión de la calidad a los que visitan el sitio. Sin embargo, esta aplicación es subutilizada. No sabemos quiénes leyeron los mensajes y quien nunca han visitado la aplicación. Por lo tanto queremos darle más relevancia a los avisos.

[^1]: De ahora en adelante, lo vamos a llamar simplemente **CMI**.

Dentro de nuestro objetivo de aprender Django usando el CMI, la aplicación `avisos` será creada como un blog. Es decir, los avisos serán los _posts_, _entries_ o entradas, como quieran decirle. Nuestro primer objetivo es crear la aplicación que funcione como un blog, ya que solo tiene un título y el contenido. Un objetivo secundario, será crear los modelos usando _mixins_ de creación. Adicionalmente, como segundo objetivo secundario, vamos a utilizar __South__ para preparar nuestro aplicación para futuras migraciones.

El segundo objetivo es mejorar la aplicación, creando anuncios permantes, como _sticky post_ y anuncios importantes que solo estarán resaltados hasta una fecha determinada. Agregaremos dos campos, uno para marcar los _sticky post_ y otro de tipo fecha para indicar la fecha en la que estará disponible el anuncio.  Como la base de datos ya está creada, un objetivo secundario será aplicar migraciones a un modelo existente.

El tercer objetivo es crear un sistema de alertas para indicarle a los usuarios que hay avisos nuevos o no leídos, usando _badges_ o etiquetas en la barra de navegación y junto al perfil del usuario[^2]. Como objetivos secundarios, será aprender el uso de _cookies_ para establecer u obtener el estado de un usuario. Igualmente vamos a aprender como enviar notificaciones entre aplicaciones.

Una vez definido el _roadmap_ de nuestra aplicación y los _milistones_ para este proyecto vamos a empezar con el primer paso, que es es crear la aplicación `avisos`.

## Aplicación Avisos, primera parte

Al terminar este proyecto el Cuadro de Mando Integral contará con una aplicación que permita dar a conocer a los usuarios información y noticias relevantes para el Sistema de Gestión de la Calidad.

### Objetivos

1. Crear una aplicación tipo _blogging_
    1. Crear una aplicación tipo blogging
    3. Permitir la edición de anuncios usando __Markdonw__
    4. Crear vista para el archivo de avisos
2. Crear un modelo usando _mixins_ para creación, modificación y autor.
3. Sincronizar la base usando South para manejar las migraciones.

### Crear una aplicación con Django

Lo primero que tenemos que hacer es activar nuestro entorno de trabajo, usando el siguiente comando

    :::bash
    namespace:cmi javier$ workon cmi
    (cmi)namespace:cmi javier$

Ahora usamos `manage.py` para crear nuestra aplicación usando el comando `startapp`:

    :::bash
    (cmi)namespace:cmi javier$ python manage.py startapp avisos

Esto crea la estructura de la aplicación que tiene esta forma:

    :::bash
    (cmi)namespace:avisos javier$ ls -l
    total 32
    -rw-r--r--  1 javier  staff   0 Mar  1 14:07 __init__.py
    -rw-r--r--  1 javier  staff  63 Mar  1 14:07 admin.py
    -rw-r--r--  1 javier  staff  57 Mar  1 14:07 models.py
    -rw-r--r--  1 javier  staff  60 Mar  1 14:07 tests.py
    -rw-r--r--  1 javier  staff  63 Mar  1 14:07 views.py

Es muy importante, si creamos nuestra aplicación sin el auxilio de `manage.py` que nos aseguremos que tenemos un archivo `__init__.py` para indicarle a Python que el directorio es un __módulo__.

### Los Mixins

Los _mixins_, que podemos traducir como _mezcladores_, son fragmentos de código reutilizables que sirven como base para crear código más complejo utilizando la base que proporcionan.

En el cuadro de mando, tal como lo indica la Norma ISO 9001, debemos identificar los registros y permitir la trazabilidad. Por lo tanto, debemos agregar a todos los registros de nuestro CMI, el _timestamp_ de la creación y modificación del registro, así como el autor del mismo.

Todas las aplicaciones cuentan con estos tres datos, por lo tanto, resulta una buena práctica crear un modelo base que herede estos campos a todos los modelos del CMI, por lo que creamos el _mixin_ para cumplir con este objetivo.

Con respecto al usuario, vamos a usar una aproximación dependiente del modelo y del formulario, pero los campos de _timestamp_ son perfectos para este _mixin_.

Y ya que tenemos una aplicación que es de uso común, llamada `core`, vamos a crear ahí el _mixin_ del modelo `trazabilidad`.

    :::Python
    class Trazabilidad(models.Model):
        """
        Una clase abstracta que sirve de base para modelos.
        Actualiza automáticamente los campos ``creado`` y ``modificado``.
        """
        creado = models.DateTimeField(auto_now_add=True)
        modificado = models.DateTimeField(auto_now=True)
        class Meta:
            abstract = True

La característica principal de este modelo, es que se define como tipo abstracto, es decir, por si mismo, este modelo no puede crear una tabla, sino que usa como base para otros modelos. Es, por definición, un modelo __heredable__. Los campos se definen como `DateTimeField` lo que es equivalente al _timestap_. El campo `creado` se actualiza una sola vez, cuando se crea, pero el campo `modificado` se actualiza _cada vez_ que se modifica el registro.

Y este es precisamente el objetivo de este _mixin_. Heredar estos campos a todos los modelos, con lo que obedecemos el principio DRY de Django.

### Uso de _mixins_ en modelos de Django

Para usar este _mixin_ en nuestra aplicación de avisos, debemos importar este modelo, y usarlo como __constructor__ para nuestra clase `Aviso`.

    :::Python
    from django.db import models
    from core.models import Trazabilidad

    class Aviso(Trazabilidad):

De esta manera, tenemos disponibles todas las funciones de `models` y `Trazabalidad`. Por lo que ahora solo tenemos que ocuparnos del modelo en si mismo y dejamos la indentificación y trazabilidad que indica la norma ISO 9001 en manos de nuestro _mixin_.

### Markdown en modelos de Django

Para facilitar la redacción de los avisos, vamos a usar __Markdown__, un potente formateador de texto, pero a la vez simple de utilizar[^3].  Entonces, debemos instalar el paquete __Python-Markdown__ en nuestro entorno de desarrollo usando `pip`:

    :::Bash
    (cmi)namespace:aviso javier$ pip install markdown
    Downloading/unpacking markdown
      Downloading Markdown-2.4.tar.gz (260kB): 260kB downloaded
      Running setup.py egg_info for package markdown

    Installing collected packages: markdown
      Running setup.py install for markdown

      [... muchas líneas más ...]

        changing mode of /Users/javier/entornos/cmi/bin/markdown_py to 755
    Successfully installed markdown
    Cleaning up...

Markdown tiene una serie de extensiones o _plugins_ muy útiles, incluyendo extenciones que permiten colorear el código, trabajar más eficientemente con listas, con tablas, con las alertas, con notas al pie, etc.

Vamos a importar el módulo `markdown` a nuestro modelo `avisos` y a definir las extencioes que queremos usar.

    :::Python
    import markdown

    MD_EXT = ['meta', 'abbr', 'attr_list', 'def_list', 'fenced_code', 'footnotes', 'smart_strong', 'tables',
              'headerid', 'sane_lists', 'smartypants', 'toc', 'admonition']


### Sobreescribir el método `save()`  en un modelo

Tenemos todo lo necesario para definir nuestro modelo, así que vamos a revisarlo y a explicar como trabajaremos con Markdown.

    :::Python
    class Aviso(Trazabilidad):
        titulo = models.CharField(max_length=60)
        slug = models.SlugField()
        texto_md = models.TextField()
        texto_html = models.TextField()
        autor = models.ForeignKey(User, related_name='avisos', editable=False)

Nuestro modelo tiene siete campos, cinco están definidos en el modelo y dos campos heredados del _mixin_ `Trazabilidad`. Pero de estos siete campos, cinco son automáticos y solo dos son editables por el usuario: `titulo` y `texto_md`. Los demás campos se calculan al momento de guardar el registro, sobreescribiendo el método `save()`.

!!! alert-info "Markdown: Conviértase antes de usar"
    Una forma tradicional de utilizar Markdown era mandar el texto directamente a la plantilla y usar un filtro para convertirlo. Este tenía que pasar cada vez que un usuario solicitaba la página. Evidentemente, el gasto era excesivo, por eso Django depreció los filtros a partir de la versión 1.5.

    La forma en la que se hace ahora resulta ser mucho más eficiente. Se almacena el texto en formato `markdown` en un campo y en otro campo el texto convertido en `html` que se actualiza automáticamente cada vez que el campo `markdown` cambia.

    La conversión a `html` puede ser lenta, pero se hace al momento de edición y no al momento de la presentación. A los usuarios se les envía el código `html` que es la forma más rápida de mostrar información en la web.

    Para convertir un texto `markdown` a `html`, usamos el método `markdown.markdown()` que toma como argumentos `texto_md` que es el campo que contiene el aviso, el formato de salida especificado como HTML5 en `output_format=html5`, `lazy_ol=True` para crear listas numeradas de forma sencilla y la lista de extenciones que ya habíamos creado en `extensions=MD_EXT`. El texto convertido se guarda en el campo `texto_html` que estará siempre listo para presentación sin pérdidas de tiempo en la conversión.

Ahora vamos a crear una método `save()` que sobreescribirá al método por default con las funciones que necesita nuestra aplicación de avisos, que son: la creación del _slug_ o nombre corto, la conversión del texto de `markdown` a `html`. Nos faltará una más para poblar el campo `autor`, pero eso se hará en la sección del panel de control de nuestra aplicación más adelante.

Este es el nuevo método `save()`:

    :::python
    def save(self, force_insert=False, force_update=False):
        self.texto_html = markdown.markdown(self.texto_md, output_format='html5', lazy_ol=True, extensions=MD_EXT)
        self.slug = slugify(self.titulo)
        super(Aviso, self).save(*args, **kwargs)

Con este método nos aseguramos que el texto está en `html` listo para ser presentado y que el aviso tiene un nombre corto para poder usarlo en la URL.

#### Métodos adicionales para el modelo `avisos`

Hay dos métodos más para nuestro modelo y una clase especial llamada `Meta` que sirve para darle información al _framework_ Django sobre nuestro modelo.

__`__unicode__`__
:    El método `__unicode__` define la forma en que nuestro modelo responde a las llamadas. Podemos formar una cadenda de texto de respuesta a la llamda de este método.

        :::Python
        def __unicode__(self):
            return self.titulo.decode('utf-8')

__`get_absolute_url`__
:   Este método devuelve la URL de nuestro aviso, de modo que podamos usarla en nuestra plantilla.

        :::Python
        def get_absolute_url(self):
            return "/aviso/%s/%s/" % (self.creado.strftime("%Y/%b/%d"), self.slug)

__`class Meta`__
:   En esta clase interna dentro de nuestro modelo de aviso, colocamos información que es visible dentro del panel de control del CMI, definimos como llamamos a nuestros registros en singular y en plurar y opciones de ordenación.

        :::Python
        class Meta:
            verbose_name = "Aviso"
            verbose_name_plural = "Avisos"
            ordering = ["-creado"]
            get_latest_by = 'creado'

Este es el código completo del modelo:

    :::Python
    # -*- coding: utf-8 -*-
    #    nombre: cmi.avisos.models
    #       app: cmi.avisos
    #      desc: Modelos para la apps de Avisos del Sistema

    from django.contrib.auth.models import User
    from django.db import models
    from django.template.defaultfilters import slugify
    from core.models import Trazabilidad


    class Aviso(Trazabilidad):
        '''
        La aplicación `aviso` crea post o entradas tipo blog, que funcionarán como
        avisos en el cuadro de mando. Y al igual que un blog, podrán mostrarse en una lista
        paginada o de forma individual. Se mantienen registros del autor del aviso y de la fecha y
        hora de creación y de la última modificación.

        El modelo tiene una propiedad `get_absolute_url` que devuelve la URL en forma de `aaaa/mm/dd/slug`.

        Los slugs o nombre corto deben ser exclusivos por día, es decir, en el mismo día no puede
        haber dos slugs iguales.
        '''
        titulo = models.CharField(max_length=60)
        slug = models.SlugField()
        texto_md = models.TextField()
        texto_html = models.TextField()
        autor = models.ForeignKey(User, related_name='avisos', editable=False)

        def __unicode__(self):
            return self.titulo.decode('utf-8')

        def save(self, *args, **kwargs):
            self.slug = slugify(self.titulo)
            super(Aviso, self).save(*args, **kwargs)

        def get_absolute_url(self):
            return "/aviso/%s/%s/" % (self.creado.strftime("%Y/%b/%d"), self.slug)

        class Meta:
            verbose_name = "Aviso"
            verbose_name_plural = "Avisos"
            ordering = ["-creado"]
            get_latest_by = 'creado'

## El panel de control de `avisos`

Cuando creamos nuestra aplicación se creó también un archivo llamado `admin.py` cuya función es configurar la parte administrativa de nuestra aplicación[^4]. Para nuestra aplicación de avisos, el módulo de administración es muy simple, como verán a continuación:

    :::Python
    # -*- coding: utf-8 -*-
    #    nombre: cmi.avisos.admin
    #       app: cmi.avisos
    #      desc: Clases para la administración de avisos

    from django.contrib import admin
    from avisos.models import Aviso

    class AvisoAdmin(admin.ModelAdmin):
        prepopulated_fields = {"slug": ("titulo",)}
        search_fields = ["titulo"]

        def save_model(self, request, obj, form, change):
            obj.autor = request.user
            obj.save()

    admin.site.register(Aviso, AvisoAdmin)

El módulo `django.contrib.admin` conecta nuestro modelo con la parte administrativa del _framework_. Al crear la clase indicamos dos propiedades importantes, la primera es `prepopulated_fields` son campos que se rellenan automáticamente. El diccionario indica que el campo `slug` se crea con el `titulo`. Tamién indicamos que queremos buscar los avisos usando el `titulo`.

También definimos un nuevo método `save_model` que se activa, como su nombre lo dice al guardar el modelo. Lo creamos para tomar la solicitud o _request_ y guardar el autor tomando el `request.user` o sea, el usuario registrado.

## Vistas para la aplicación `avisos`

Para cubrir el primer objetivo de esta iteración vamos a crear la vista que muestre los anuncios más recientes. En los artículos siguientes de esta serie, para mejorar la presentación de los anuncios, haremos una vista para presentar los anuncios individuales y crearemos la paginación para el archivo. En la tercera iteración, crearemos los formularios para editar y crear avisos.

Para facilitarnos el trabajo con vistas, nos vamos a apoyar del paquete `django-annoying`[^5] que tiene un decorador o _decorator_ que facilita enormemente la vida. Solo tenemos que invocarlo con el nombre del dominio y regresar la vista con los diccionarios de datos.

Miren lo que les digo

    :::Python
    from annoying.decorators import render_to
    from avisos.models import Aviso

    @render_to('avisos/index.html')
    def index(request):
        avisos = Aviso.objects.all().order_by("-creado")
        return {'avisos':avisos}

Incluso, podemos colocar en el `return` el _QuerySet_ directamente, con lo que nos ahorramos incluso esa línea.

Esta simple vista nos permite crear la lista de anuncios, con la observación que todos los avisos aparecen en una sola página.

Para terminar con la vista, vamos a crear el patrón de búsqueda que URL que nos permita llamar a esta función. Para esto usaremos el archivo `urls.py`.

    :::Python
    from django.conf.urls import patterns, url

    urlpatterns = patterns('avisos.views',
       url(r"^$", "index", name="avisos"),
    )

## La plantilla para `avisos`

La última parte de esta primera iteación de la aplicación `avisos` consiste en crear una plantilla. Nos vamos a concentrar en crear únicamente la plantilla para avisos porque en este mismo blog puedes encontrar la serie sobre las plantillas modulares.

La plantilla, lo único que hace es usar un ciclo `for` para recorrer la lista de avisos. Veamos como queda:

    :::HTML
    {% block contenido %}
    <div class="page-header">
      <h1>Avisos del Sistema</h1>
    </div>
    <!-- avisos  -->
    <div class="avisos">
      {% for aviso in avisos.object_list %}
      <div class"entry">
        <h2>{{ aviso.titulo }}</h2>
        <div class="meta">
          <i class="icon-calendar"></i>
            {{ aviso.creado }}
          <i class="icon-user"></i>
            {{aviso.autor.first_name}} {{aviso.autor.last_name}}
          {% if user.is_authenticated %}
            <a href="/avisos/editar/{{aviso.id}}/">
            <i class="icon-pencil-2"></i>
              Editar</a>
          {% endif %}
        </div><!-- ./meta -->
        <p>
          {{ aviso.texto|safe }}
        </p>
        <hr />
      </div><!-- ./entry -->
      {% endfor %}
    </div><!-- ./aviso -->
    {% endblock content %}


Lo que vemos es que, efectivamente, la plantilla trata a los avisos como un blog y nos prepara para la siguiente fase de mejora: la presentación de entradas individuales y la edición de los avisos.

## Sincronización de la tabla `avisos`

Por último, igualmente en preparación de la segunda y tercera fase de mejora, vamos a sincronizar nuestra tabla `avisos` y a prepararla con `South`[^6] para migrarla a nuevas configuraciones conforme lo requiera la mejora.

Además de instalarla con `pip` con el entorno virtual activado, hay que agregar `south` a la lista de aplicaciones instaladas en nuestra configuración.

Recordemos que es la primera sincronización que vamos a hacer, así que veremos este proceso completo, por primera _y única_ vez. Y también por única vez lo haremos __sin nuestro modelo activado__.

Empezamos sincronizando la base de datos y creando el usuario administrador. Esta es la salida de este comando:

    :::Bash
    (cmi)namespace:cmi javier$ python manage.py syncdb
    Syncing...
    Creating tables ...
    Creating table django_admin_log
    Creating table auth_permission
    Creating table auth_group_permissions
    Creating table auth_group
    Creating table auth_user_groups
    Creating table auth_user_user_permissions
    Creating table auth_user
    Creating table django_content_type
    Creating table django_session
    Creating table south_migrationhistory

    You just installed Django's auth system, which means you don't have any superusers defined.
    Would you like to create one now? (yes/no): yes
    Username (leave blank to use 'javier'): javier
    Email address: javier@namespace.mx
    Password:
    Password (again):
    Superuser created successfully.
    Installing custom SQL ...
    Installing indexes ...
    Installed 0 object(s) from 0 fixture(s)

    Synced:
     > django.contrib.admin
     > django.contrib.auth
     > django.contrib.contenttypes
     > django.contrib.sessions
     > django.contrib.messages
     > django.contrib.staticfiles
     > south

    Not synced (use migrations):
     -
    (use ./manage.py migrate to migrate these)

Ahora, agregamos la aplicación `avisos` a la lista de aplicaciones instaladas y realizamos la migración inicial. Veamos que es lo que hace este comando:

    :::Bash
    (cmi)namespace:cmi javier$ python manage.py schemamigration avisos --initial
    Creating migrations directory at '/Users/javier/Documents/Proyectos/cmi/cmi/avisos/migrations'...
    Creating __init__.py in '/Users/javier/Documents/Proyectos/cmi/cmi/avisos/migrations'...
     + Added model avisos.Aviso
    Created 0001_initial.py. You can now apply this migration with: ./manage.py migrate avisos

Crea el directorio y los scripts de migración para nuestra aplicación. Este comando (`python manage.py schemamigration aplicacion --initial`) es el que vamos a ejecutar cada vez que agreguemos nuevos modelos al CMI.

En la tercera mejora de `avisos` veremos como aplicar los cambios de nuestros modelos a la base de datos.

## Conclusión

Crear la primera aplicación, un blog, es relativamente sencillo. En las mejoras programadas para esta aplicación iremos conociendo nuevos patrones de programación aplicados al Cuadro de Mando.

También empezaremos la aplicación `metas` que es la más compleja del sistema. Y veremos como representar gráficos estadísticos con Django.

[^2]: Como el número que sale en Google Chrome junto a la campanita, o el contador de mensajes no leídos en los clientes de correo.

[^3]: Puedes consultar la ayuda para usar Markdown directamente en el sitio de su creador, [Daring Fireball](http://j.mp/ns-ayuda-markdown).

[^4]: La referencia oficial: http://j.mp/ns-doc-django-admin

[^5]: http://j.mp/ns-django-annoying

[^6]: http://j.mp/ns-django-south
