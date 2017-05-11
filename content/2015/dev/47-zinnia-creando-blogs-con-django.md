Title: Zinnia, creando blogs con Django
Date: 2014/01/13 05:58
Category: Desarrollo 
Tags: krypton, zinnia, paas, webdev 
Slug: zinnia-creando-blogs-con-django
Author: Javier Sanchez Toledano
Summary: 

Este es el quinto artículo de una serie dedicada a la creación de una aplicación web usando Django en [Nitrous.IO][nitro]. En el primero aprendimos [como crear una caja en Nitrous.IO](http://conxb.com/ns-nitro01) para ejecutar nuestra aplicación. En el según [como crear una base de datos en Heroku](http://conxb.com/ns-nitro02). En el tercero [cómo usar entornos virtuales en Python](http://conxb.com/ns-nitro03) y en el cuarto artículo de la serie como [usar configuraciones específicas en Django](http://conxb.com/ns-nitro04).

Ahora vamos a terminar la configuración de nuestro blog, instalándolo y dejándolo listo para empezar a utilizarlo. 

## Zinnia, la elección del proyecto Krypton

[Zinnia][zinnia] es una simple pero poderosa aplicación para manejar blogs dentro de un sitio web desarrollado en Djanjo. Entre sus características podemos mencionar las siguientes: sistema de comentarios, *sitemaps*, vistas de archivo, entradas relacionadas, entradas privadas, fuente de noticias RSS, etiquetas y categorías para las entradas.

Cuenta también con un avanzado motor de búsqueda; programación de la publicación y expiración de entradas; plantillas personalizadas; edición con Markdown, protección anti-spam; widgets de entradas populares; panel de administración; soporte para Twitter, Bit.ly, Gravatar, directorio de Pings, Windows Live Writer... es decir es un blog bastante completo.

## Configuración de Zinnia

Recordemos que ya habíamos instalado [Zinnia y sus dependencias](https://namespace.mx/django/configurar-un-blog-con-zinna-y-django-en-nitrousio/#zinnia-la-eleccion-del-blog) pero no habíamos tocado nada más. En esta ocasión vamos a instalar las tablas en nuestra base de datos y a realizar la configuración del blog.


## URL personalizadas en Django

Voy a instalar el blog en la raíz del dominio, y con este dato vamos a colocar en el archivo `urls.py` de la aplicación `krypton` los patrones de búsqueda para que funcione el blog.

Zinnia tiene un paquete de patrones de búsqueda ya configurado, lo podemos activar agregando la línea `url(r'^weblog/', include('zinnia.urls')),` a la lista `urlpatterns`. Son solo tres líneas las que necesitamos para tener nuestro blog funcionando.

Este es el archivo de `urls.py` con la configuración específica del proyecto krypton.

    urlpatterns = patterns('', 
        url(r'^', include('zinnia.urls')),
        url(r'^comments/', include('django.contrib.comments.urls')),
        url(r'^cp/', include(admin.site.urls)),
    )

Los archivos estáticos los maneja con el módulo `django.contrib.staticfiles` y los vamos a presentar usando nuestro servidor Nginx, por lo que nuestro blog no tiene que preocuparse estos. Y, desde luego, en modo de desarrollo, el miniservidor de `runserver` se encarga de servir los estáticos sin problemas.

## Migración de base de datos en Django

De manera rápida les diré que las migraciones de las bases de datos es la forma en la que una base de datos cambia, de una versión a la siguiente. `South` es la aplicación con la que vamos a adminsitrar y controlar las migraciones a la base de datos, en lo que llega la nueva versión de Django, que incorpora esta característica en el núcleo.

Sin embargo, `South` merece un artículo aparte, por lo que para esta ocasión solo vamos a crear nuestras tablas, usando `migrate` y luego veremos el poder y la importancia de `South`.

Mientras tanto, agregamos la aplicación `south` a nuestra lista de aplicaciones instaladas en la configuración base `krypton.settings.base`.

<div style="max-width:360px; margin: 25px auto;">
<!-- cyberia.336x289.01.top -->
<ins class="adsbygoogle"
style="display:inline-block;width:336px;height:280px"
data-ad-client="ca-pub-9466828947698623"
data-ad-slot="8590866557"></ins>
<script>
(adsbygoogle = window.adsbygoogle || []).push({});
</script>
</div>
<div style="clear:both;"></div> 

## Creación de las tablas del Proyecto Krypton

Estamos listos para crear nuestras tablas. Pasamos a la consola del IDE en [Nitrous.IO][nitros] y ejecutamos la orden que crea nuestro blog. Recuerden que debemos tener nuestro entorno virtual activado con `workon krypton`.

    python manage.py syncdb --migrate

Y esta es la salida de nuestro comando:

    (krypton)javier@krypton:~/proyecto_krypton/krypton$ python manage.py syncdb --migrate
    Syncing... 
    Creating tables ... 
    Creating table auth_permission
    Creating table auth_group_permissions
    Creating table auth_group 
    Creating table auth_user_groups 
    Creating table auth_user_user_permissions
    Creating table auth_user 
    Creating table django_admin_log
    Creating table django_site 
    Creating table django_comments
    Creating table django_comment_flags
    Creating table django_session
    Creating table django_content_type 
    Creating table tagging_tag
    Creating table tagging_taggeditem 
    Creating table south_migrationhistory  

Como es la primera vez que sincronizamos[^2] nuestra aplicación nos va a preguntar si queremos crear al usuario administrador, algo que es necesario.

    You just installed Django's auth system, which means you don't have any superusers defined.                                                                    
    Would you like to create one now? (yes/no):   

Después de crear el usuario, con nuestros correo y contraseña (que no debemos olvidar) se crean las tablas de permisos y las migraciones.

Al final veremos el resultado de la sincronización/migración:

    Synced:                                                                  
     > django.contrib.auth
     > django.contrib.admin
     > django.contrib.sites
     > django.contrib.comments
     > django.contrib.sessions
     > django.contrib.messages 
     > django.contrib.staticfiles
     > django.contrib.contenttypes
     > tagging 
     > mptt 
     > south

     Migrated:
      - zinnia

Y eso es todo.

Ya podemos arrancar nuestro servidor de pruebas y verificar el funcionamiento de Zinnia.

En el próximo artículo, veremos los ajustes finos para proceder a crear nuestra plantilla y pasar nuestro blog a producción.


[zinnia]: http://django-blog-zinnia.com/
[nitro]: http://conxb.com/ns-nitro

[^1]: No estoy seguro que todavía exista, pero lo dejamos para hacer pruebas.

[^2]: Creo que ahora se deben llamar *”migraciones”*.
