Title: Cómo integrar Django y React.js, Parte 1
Date: 2018-06-04 10:30
Category: desarrollo
Tags: django, reactjs
Summary: Existen diferentes formas de integrar Django y React.js, aqui presentamos una de estas, donde usamos React.js directamente en las plantillas de Django.

Cuando buscaba la forma de usar ReactJS junto con Django me enfrenté al problema que no sabía como manejar los _tokens_ del lado del cliente, dónde guardarlos, como recuperarlos, como usarlo usarlos, es decir nada.

Así que se me ocurrió usar las sesiones de Django y usar ReactJS __dentro de__ Django. Sin la posibilidad de usar las variables de Django encontré una técnica que me ha servido.

## La configuración en Django

Puede ser tu proyecto normal, uno nuevo por ejemplo, con los módulos que acostumbras usar, pero además, con este llamado [`django-webpack-loader`][1]
 que nos permite usar _Webpack de forma transparente_ en Django.

[1]: https://github.com/owais/django-webpack-loader

Requiere de una configuración adeicional en Django, pero es muy simple de verdad.

```python
WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': DEBUG,
        'BUNDLE_DIR_NAME': 'bundles/',
        'STATS_FILE': APPS_DIR.child('static', 'webpack-stats.json')
    }
}
```

Solo indicamos si usamos caché, el directorio del _bundle_, que es el archivo que crea WebPack y por último dónde encontramos el archivo `webpack-stats.json` que le dice a Django dónde está React.

## La configuración en React

Yo hice una configuración personalizada de WebPack, pero igual la que se crea con [`create-react-app`][2] puede servir, solo sigue las instrucciones de esa aplicación.

[2]: https://facebook.github.io/create-react-app/

Necesitamos un módulo de node llamado [`webpack-bundle-tracker`][3] que se encarga de crear el archivo `webpack-stats.json` que usamos en Django para ubicar a React. Instálalo como dependencia de desarrollo.

[3]: https://github.com/owais/webpack-bundle-tracker

Ahora debemos configurar WebPack, para esto necesitamos indicar, para mayor facilidad, la salida del _bundle_. Así que debemos agregar en `webpack.config.js` lo siguiente:

```js
  output: {
    path: path.resolve(__dirname, '../cerebro/apps/static/js'),
    filename: "[name]-[hash].js",
    publicPath: 'http://localhost:8080/static/bundles/'
  },
```

Y en la parte `plugins` indicamos que cargue el `BundleTracker`:

```
  plugins: [
    new BundleTracker({filename: '../cerebro/apps/static/webpack-stats.json'}),
  ]
```

Consulta la documentación de [WebPack][4] si tienes alguna duda sobre como configurarlo.

[4]: https://webpack.js.org/


## La vista

Primero necesitamos una vista que carga una plantilla. Es lo único que hacer, cargar la portada de la aplicación. 

Así que en mi aplicación tengo un archivo `views.py` que tiene esta vista:

```python
import json
from django.views import View


class Index(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        data = {
            'perimisos': json.dumps(
                sorted(list(request.user.get_all_permissions()))
            )
        }
        return render(request, self.template_name, data)
```

En el método `GET` de esta vista agrega una variable `data` que contiene de forma _serializada_ los permisos que tiene el usuario, igual podríamos agregar el usuario o cualquier otro dato, pero __debe estar en formato JSON__.


## La ruta
Esta vista se vuelve la portada en los patrones de búsqueda definidos en `urls.py`:

```python
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, re_path
from core.views import Index

urlpatterns = [
    path('ingresar/', auth_views.LoginView.as_view(), name='login'),
    path('salir/', auth_views.LogoutView, name='logout'),
    path('admin/', admin.site.urls),
    path('', Index.as_view(), name="index"),
    re_path(r'^(?:.*)/?$', Index.as_view())
]
```

Como pueden observar, con este método puedo definir rutas que quiero que atienda django, como `ingresar` o `admin`, pero también defino que la portada y todo lo demás sea atendido por `Index`. Esto es importante, la ruta __*catch all*__ sirve para pasar todas las rutas que no atienda Django a React. Por eso va al final, primero vemos si la atiende Django y si no, se la pasamos a React.

## La plantilla

La plantilla incluye la carga de las etiquetas especiales que `webpack_loader` pone a nuestra disposición.

Usamos la carga de las hojas de estilo que genera WebPack en el área del encabezado y la carga del JavaScript al final del archivo.

```html
{% load static %}
{% load render_bundle from webpack_loader %}

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Cuadro de Mando</title>
    {% render_bundle 'app' 'css' %}
    <script defer src="https://use.fontawesome.com/releases/v5.1.0/js/all.js"></script>
  </head>
  <body>

    <div id="app"></div>

    <script>
      window.django = {
        csrf: "{{ csrf_token }}",
        urls: {
          login: "{% url 'login' %}",
          logout: "{% url "logout" %}"        },
        user: {
          authenticated: {% autoescape off %}("True" === "{{ user.is_authenticated }}"){% endautoescape %},
          username: "{{ request.user.username }}",
          full_name: "{{ request.user.get_full_name }}",
          last_login: "{{ request.user.last_login }}",
          permissions: {% autoescape off %}JSON.parse('{{ permissions }}'){% endautoescape %}
        }
      };
    </script>

    {% render_bundle 'app' 'js' %}
  </body>
</html>
```

Lo interesante es que usamos en este archivo las variables de Django que usando JavaScript pasamos al objeto `window` del navegador y de esta forma están disponibles como __variables globales__ en React.

Aquí pueden agregar las variables que necesiten, siempre y cuando el resultado final sea un objeto JSON válido. En este ejemplo, le pasados la variable `csrf`, hacemos un objeto con algunas URLs y creamos el objeto `user` que le dice a React si en esta sesión estamos acreditados o no.

## Conclusión
Ahora solo tienes que iniciar tu proyecto de Django y tu proyecto de React y ambos estarán conectados.

El código fuente generado por Django se ve así:

```html



<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Cuadro de Mando</title>
    <link type="text/css" href="http://localhost:8080/static/bundles/css/cmi_styles.css" rel="stylesheet" />
    <script defer src="https://use.fontawesome.com/releases/v5.1.0/js/all.js"></script>
  </head>
  <body>

    <div id="app"></div>

    <script>
      window.django = {
        csrf: "VWuQ4KaN9ocP5N4abDWV8ZF7FpGbEXZCReKOzHCUEahQNHBR20jiECrZ1BwnwoiH",
        urls: {
          login: "/ingresar/",
          logout: "/salir/",
          staticRoot: "/assets/index.html",
        },
        user: {
          authenticated: ("True" === "False"),
          username: "",
          full_name: "",
          last_login: "",
          permissions: JSON.parse('[]')
        }
      };
    </script>

    <script type="text/javascript" src="http://localhost:8080/static/bundles/app-04f6b683ac4f718959ff.js" ></script>
  </body>
</html>
```

Y ahí aparece la llamada a React desde Django.