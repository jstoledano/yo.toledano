Title: Acreditación y Autorización en VueJS  
Date: 2017-04-08 20:14:50
Category: desarrollo
Tags: vuejs, cmi, javascript  
Summary: 

No sé exactamente que fue lo que pasó, pero los métodos que había escrito para la autorización y la acreditación dejaron de funcionar.

Eran muy simples y primitivos, pero funcionaban. Pedían el *token*, lo guardaban en el `localStorage` y luego de ahí lo pasaban al _state store_ para usarlo en toda la aplicación. 

Así que ahora vamos a probar hacer esto usando librerías. 

## Vue Authenticate
[__vue-authenticate__](https://github.com/dgrubelic/vue-authenticate) se anuncia como una solución fácilmente configurable que proporciona métodos de _login_ y _logout_ y proveedores de registro con redes sociales de Github, Facebook, Google y Twitter usando OAuth.

La mejor parte de esta librería es que no tiene que acoplarse forzosamente con librerías de manejo de estado. O sea que podemos usar la librería que mejor nos convenga.

Tiene dos formas de uso, la primera y por default es usando [vue-resource](https://github.com/pagekit/vue-resource) y la segunda es usando [axios](https://github.com/mzabriskie/axios) (por medio del plugin [vue-axios](https://github.com/imcvampire/vue-axios)).


## Implementación
Como `vue-ressource` está algo así como discontinuada y me gustó mucho Axios, este es el que vamos a usar.

    yarn add vue-authenticate axios vue-axios

Y los agregamos al archivo de la aplicación `main.js`.

```javascript
import Vue from 'vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import VueAuthenticate from 'vue-authenticate'

Vue.use(VueResource)
```

Ahora viene una parte muy importante que es la configuración. 

```javascript
Vue.use(VueAuthenticate, {
  baseUrl: 'http://sgc-server.dev',
  loginUrl: '/auth/login/',
  tokenName: 'auth_token',
  requestDataKey: 'data',
  responseDataKey: 'data',
  tokenType: 'Token',

  bindRequestInterceptor: function () {
    this.$http.interceptors.request.use((config) => {
      if (this.isAuthenticated()) {
        config.headers['Authorization'] = [
          this.options.tokenType, this.getToken()
        ].join(' ')
      } else {
        delete config.headers['Authorization']
      }
      return config
    })
  },

  bindResponseInterceptor: function () {
    this.$http.interceptors.response.use((response) => {
      this.setToken(response)
      return response
    })
  }
})
```

Veamos cada clave, porque todas son importantes

- `baseUrl: 'http://sgc-server.dev'` - corresponde a la dirección del servidor. A partir de aquí podemos ir sumando rutas.
- `loginUrl: '/auth/login/'` - esta es la ruta del login. Como yo uso Djoser, así se genera y esta opción se suma a `baseUrl`.
- `tokenName: 'auth_token'` - esta es muy importante y depende de cada API, en Djoser así se llama.
- `requestDataKey: 'data'` - Axios manda los datos en `data`, al contrario de Vue-Resource que manda los datos en `body`. Si no colocamos bien esta opción, nunca nos registramos.
- `responseDataKey: 'data'` - Igual que el anterior, la respuesta se coloca en `data`.
- `tokenType: 'Token'` - Para la autorización, se envía el encabezado `Authorization` con el token. En algunas APIs se llama `Bearer`, pero en Djoser se llama `Token`. Si no se coloca bien, no funciona.

Debido a que `vue-authentication` usa Fue Resource por omisión, hay que hacer dos adecuaciones para adaptarla a Axios, que se refieren a interceptar las solicitudes para agregarles el encabezado de autorización:

```javascript
  bindRequestInterceptor: function () {
    this.$http.interceptors.request.use((config) => {
      if (this.isAuthenticated()) {
        config.headers['Authorization'] = [
          this.options.tokenType, this.getToken()
        ].join(' ')
      } else {
        delete config.headers['Authorization']
      }
      return config
    })
  }
```

Y la segunda intercepta la respuesta[^1].

```javascript
  bindResponseInterceptor: function () {
    this.$http.interceptors.response.use((response) => {
      this.setToken(response)
      return response
    })
  }
```

En el componente donde esté el formulario de ingreso, llamamos a las funciones que necesitemos, por ejemplo:

```javascript
methods: {
    login: function () {
      this.$auth.login(this.credentials)
        .then(_payload => {
          alert(`Identificado correctamente`)
        })
        .catch(_error => {
          console.log(_error.response)
        })
    }
  }
```

Que simplemente lanza una alerta cuando se obtiene el token.

## Métodos disponibles
Estos son los métodos proporcionados:

- `isAuthenticated()` - devuelve `true` si encuentra un token en el almacenamiento local especificado. Puede manejar tokens tipo JWT[^2].
- `getToken()` - devuelve el token desde el almacén local especificado.
- `setToken()` - guarda el token en el almacén. Esta función es interna y no hay ninguna razón para llamarla desde un método.
- `getPayload()` - yo creo que esta función se usa para decodificar un token JWT.
- `login()` - esta función realiza la solicitud de Token. Usa un objeto con el usuario y la contraseña. Si el ingreso es exitoso, ejecuta `setToken`. Devuelve el token.
- `register()` - Registra al usuario. Se le envía un objeto con el usuario, la contraseña y el correo electrónico. Si es exitoso el registro se ejecuta `setToken`. Devuelve el token.
- `logout()` - Envía la petición de salida a la API y elimina el token del almacén local. No devuelve nada, creo.
- `authenticate()` - Creo que esta función es para llamar a los proveedores de OAuth: GitHub, Facebook, Twitter, Google, Instagram, Bitbucket[^3]. 

Bueno, pues ya está. En el repositorio hay un ejemplo de como usar Vuex para las funciones de registro… Me gusta la idea, pero será en otra ocasión.

[^1]: A esta no le entiendo.

[^2]: Si no saben que es un token JWT, no me pregunten a mi porque yo tampoco sé.

[^3]: A duras penas puedo usar un token simple, ya mero voy a poder usar estos de OAuth… pero algún día.
