Title: Mixin con Vue    
Date: 2017-03-27 21:55:41
Category: desarrollo 
Tags: vuejs, javascript 
Summary: Un plugin mínimo, completo, funcional y verificable que permite realizar actvidades de acreditación en VueJS

Mientras me resuelven la pregunta en [Stackoverflow en Español](http://es.stackoverflow.com/questions/58142/obtener-el-valor-de-una-promesa) sigo avanzando con mi plugin de acreditación.

El objetivo del mixin es ofrecer a la aplicación las acciones:

- _login_ para obtener el token, 
- _logout_ para eliminar cualquier dato de acreditación del servidor, del local storage y del state, 
- que agregue los datos del usuario al _state_,
- que agregue el _token_ al _local storage_ y al _state_,
- que agregue el token al encabezado `Authorization` de todas las peticiones.

## Dependencias del mixin

El mixin tiene varias dependencias, como [Vue](https://vuejs.org/), [Vuex](https://vuex.vuejs.org/en/), [Axios](https://github.com/mzabriskie/axios) y [localForage](https://localforage.github.io/localForage/) .

```javascript
import Vue from 'vue'
import { mapState } from 'vuex'
import axios from 'axios'
import VueAxios from 'vue-axios'
import { store } from '../plugins/store'
import AlmacenCMI from '../plugins/almacen'
```

## Login
El _login_ es un _método_ que recibe las credenciales del usuario, es decir, el nombre del usuario y las contraseñas y las envía al _endpoint_ de la API para obtener un token. Una clave especial que sirve para demostrarle al servidor API que el usuario está acreditado para realizar operaciones u obtener información de la API.

Esta función la usa un formulario de de ingreso, que le manda un objeto con dos propiedades, `username` y `password`. 

```
function _login () {
  axios.post(_loginURL, this.credenciales)
    .then(response => {
      let _token = response.data.auth_token
      this.almacen.setItem('token', _token)
      store.state.token = _token
    }).catch(e => console.log(`${e}`))
}
```

Este objeto le pasa al método `post` la URL de login y las credenciales de un usuario. Esta es una promesa que una vez que se resuelve de forma favorable, crea una variable local `_token` para almacenar los datos que devuelve el servidor y guarda los datos tanto en el almacén local como en la variable de estado. Por el momento, el único control de errores es mostrarlo en la consola.

## Control de Acceso
Este método se ejecuta en el componente principal de la aplicación en el momento de [*montar*](https://vuejs.org/v2/guide/instance.html#Lifecycle-Diagram) la instancia Vue[^1]. 

[^1]: También podría ser al momento de crearla, pero no estoy seguro. En la próxima revisión lo veremos.

```
function _getAccessToken () {
  this.almacen.getItem('token').then((_token) => {
    store.state.token = _token
    this.axios.defaults.headers.common['Authorization'] = 'Token ' + _token
    _me()
  })
}
```

Se trata de convertir al _store_ de **Vuex** en la única fuente de verdad, así que toma el token del almacén persistente y lo coloca en el _state_. También cambia la configuración de Axios para que incluya en todas las peticiones que haga el token. Para finalizar, llama al método `me()`.

## Método me()
Este método copia el usuario, el identificador y el corre electrónico en un objeto en el state, para que sea usado como fuente principal de datos.

```
function _me () {
  axios.get(_authURL + 'me/', {})
    .then((_me) => { store.state.me = _me.data })
}
```

## Método destroy()
Este método elimina los datos de acreditación, tanto en el servidor, en el estado  y el almacén persistente.
```
function _destroy () {
  axios.post(_authURL + 'logout/')
    .then(() => {
      this.almacen.removeItem('token')
      store.state.token = null
      store.state.me = {}
      store.state.fuera = true
      this.axios.defaults.headers.common['Authorization'] = ''
    })
}
```

Llamo al /endpoint/ `logout` y cuando se resuelve la promesa se elimina el token del almacenamiento persistente, luego el token, la variable `me` y `fuera` del estado y se elimina la configuración de Axios.

## Conclusión
El _mixin_ expone tres variables y tres métodos, para que estén disponibles en los componentes donde usen.

```
export default {
  computed: {
    ...mapState(['token', 'fuera', 'me'])
  },
  methods: {
    getAccessToken: _getAccessToken,
    login: _login,
    destroy: _destroy
  }
}
```

Este es el código completo del _mixin_.

```
/**
 * Created by javier on 25/03/17.
 */

import Vue from 'vue'
import { mapState } from 'vuex'
import axios from 'axios'
import VueAxios from 'vue-axios'
import { store } from '../plugins/store'
import AlmacenCMI from '../plugins/almacen'

Vue.use(VueAxios, axios)
Vue.use(AlmacenCMI)

const _baseURL = 'http://localhost:8000/'
const _authURL = _baseURL + 'auth/'
const _loginURL = _authURL + 'login/'

/**
 * Dadas las credenciales, autentifica al usuario
 * @author Javier Sanchez Toledano <js.toledano@me.com>
 * @see Axios
 */
function _login () {
  axios.post(_loginURL, this.credenciales)
    .then(response => {
      let _token = response.data.auth_token
      this.almacen.setItem('token', _token)
      store.state.token = _token
    }).catch(e => console.log(`${e}`))
}

/**
 * Coloca el token en el almacen de vuex, al montar un componente
 * @author Javier Sanchez Toledano <js.toledano@me.com>
 * @see localForage
 */
function _getAccessToken () {
  this.almacen.getItem('token').then((_token) => {
    store.state.token = _token
    this.axios.defaults.headers.common['Authorization'] = 'Token ' + _token
    _me()
  })
}

/**
 * Trae los datos del usuario, disponibles en el estate
 * @private
 * @return me
 * @see _getAccessToken
 */
function _me () {
  axios.get(_authURL + 'me/', {})
    .then((_me) => { store.state.me = _me.data })
}

/**
 * Se elimina el token y los datos en local storage y el state.
 * O sea, sale de la aplicación
 * @private
 */
function _destroy () {
  axios.post(_authURL + 'logout/')
    .then(() => {
      this.axios.defaults.headers.common['Authorization'] = 'Token ' + this.token
      this.almacen.removeItem('token')
      store.state.token = null
      store.state.me = {}
      store.state.fuera = true
      this.axios.defaults.headers.common['Authorization'] = ''
    })
}

// const _sessionVersion = '0.1.0'

export default {
  computed: {
    ...mapState(['token', 'fuera', 'me'])
  },
  methods: {
    getAccessToken: _getAccessToken,
    login: _login,
    destroy: _destroy
  }
}
```

