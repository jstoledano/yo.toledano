Title: Login con Flask
Date: 2015-06-06 17:07:53
Category: Desarrollo
Tags:  flask, openid,
Author: Javier Sanchez Toledano
Summary: Cómo funciona el registro de usuarios en Flask

Esta es la traducción de la quinta parte del megatutorial de **Flask** hecho por Miguel Gringberg[^1]. La aplicación tiene por nombre `microblog` y se trata de crear una aplicación similar a  **Twitter**, aumentando la complejidad de cada capítulo.

## Configuración

Al igual que hicimos en capítulos previos, empezaremos configurando las extensiones de Flask que vamos a usar. Para el sistema de usuarios usaremos dos extensiones: `Flask-Login` y `Flask-OpenID`. La primera maneja a los usuarios registrados, mientras que `Flask-OpenID` se encarga de la _autenticación_. Estas extensiones se configuran en el archivo `app/__init__.py`:

```python
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from config import BASEDIR

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
oid = OpenID(app, BASEDIR.child('tmp'))
```

La extensión `Flask-OpenID` requiere una ruta a un directorio temporal para almacenar archivos. Por eso debemos especificar la ubicación del directorio temporal `tmp`, y a diferencia del tutorial del autor, yo utilicé el módulo `Unipath` con el que estoy más acostumbrado, simplemente defino la constante `BASEDIR` en el archivo `config.py`

```python
from unipath import Path
BASEDIR = Path(__file__).ancestor(1)
```

Y a partir de ahí tengo un objeto con el que puedo definir, crear, verificar o borrar rutas y archivos.

## Compatibilidad con Python 3

Debes asegurarte que la versión de `Flask-OpenID` sea la 1.2.4 o superior. Para verificarlo, ejecuta el siguiente comando:

```
pip freeze
```

Si obtienes una inferior a la mencionada, debes desinstalar la versión actual e instalar la nueva.

```
$ pip uninstall flask-openid
$ pip install git+git://github.com/mitsuhiko/flask-openid.git
```

> Toma en cuenta que debes tener instalado el programa `git`.

## Revisando el modelo User

La extensión `Flask-Login` necesita que se implementen ciertos métodos en la clase `User`, pero no hay ningún requisito especial sobre _como_ implementarlos.

Aquí está la clase `User` tal como aparece en el archivo `app/models.py`:

```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<Usuario %r>' % (self.nickname)
```

El método `is_authenticated` tiene un nombre un tanto confuso. En general este método debe regresar `True` a menos que el objeto que representa al usuario no esté autenticado por alguna razón.


El método `is_anonymous` suele retornar `True` solo si los usuarios no están registrados en el sistema.

Finalmente, el método `get_id` regresa el identificador único del usuario en formato unicode. Usamos el identificador generado por la base de datos. Debido a la diferencia en el manejo de unicode entre Python 2 y 3 se proporcionan alternativas para ambas versiones.

## Llamando al cargador de User

Ahora estamos listos para implementar el sistema de ingreso usando las extensiones Flask-Login y Flask-OpenID.

Primero vamos a escribir una función que cargue los usuarios desde la base de datos. Esta función será utilizada por Flask-Login en el archivo `app/views.py`:

```python
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))
```

Hay que hacer notar que esta función se registra con Flask-Login usando el decorador `lm.user_loader`. Y también es importante tener presente que los identificadores de usuario que proporciona Flask-Login son siempre cadenas unicode, así que debemos convertirlos en enteros antes de enviar el `id` a `Flask-Alchemy`.


## La función `login`

Ahora vamos a actualizar la función `login()` en el mismo archivo `app/views.py`:

```python
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from .forms import LoginForm
from .models import User

@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    return render_template(
        'login.html',
        title='Sign In',
        form=form,
        providers=app.config['OPENID_PROVIDERS']
    )
```
Para esta función utilizamos varios módulos, que explicaremos mas tarde.

Los cambios con respecto a nuestra función anterior son muy pequeños. Hemos agregado un nuevo decorador a nuestra función, `oid.loginhandler` que le dice a `Flask-OpenID` que esta la función que maneja el ingreso de usuarios.

Al principio del cuerpo de la función vemos que `g.users`  se asigna a un usuario _autenticado_, y en su caso lo redirigimos a la página inicial. La idea es que si es un usuario ya registrado no lo mandemos de nuevo a la página de _login_.

El objeto global `g` lo proporciona Flask como un lugar para almacenar y compartir datos durante toda la vida de una solicitud (o `request`, como lo llamaremos de ahora en adelante). Y como seguramente habrán adivinado, lo usaremos para almacenar a los usuarios registrados.

La función `url_for` la usamos en la llamada `redirect` definida por Flask como una forma limpia de obtener la URL de una vista dada. Si quieres redireccionar a la página inicial, podemos usar `redirect('/index)` pero hay muy buenas razones para que Flask construya las URL por nosotros[^2].

