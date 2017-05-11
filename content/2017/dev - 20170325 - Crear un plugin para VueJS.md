Title: Cómo crear un plugin para VueJS   
Date: 2017-03-25 13:37:46
Category: desarrollo 
Tags: vuejs, plugin, javascript, es6  
Summary: Los plugins en VueJS son una forma simple pero efectiva de crear funciones globales y facilitar la reutilización de código entre proyecto.

Crear un  _plugin_ para **VueJS** es una forma simple de aislar el código de una aplicación específica y hacerlo útil para cualquier otra de forma global. Lo importante es que no tenga en código dependiente de una aplicación en particular, sino que sea _agnóstica_.

Honestamente, la [documentación](https://vuejs.org/v2/guide/plugins.html) es muy parca, por no decir mala. Pero aún así, me las arreglé para hacer un pequeño plugin.

## Objetivo
El objetivo es hacer fácil el uso del espacio de almacenamiento de los navegadores, `localStorage` por ejemplo para poder almacenar información de manera persistente.

Este es un objetivo específico de uno general, que se trata de un conjunto de rutinas que verifiquen si existe un token de acreditación en el espacio de almacenamiento, y si existe, cargarlo en el almacén de Vuex (el almacenamiento central de VueJS) para que esté disponible para toda la aplicación. Si no está disponible, entonces mandar al usuario al /login/ cuando solicite una página protegida.

Este _plugin_ está enteramente basado en [`vue-localforage`](https://www.npmjs.com/package/vue-localforage) de [shuduanxia](https://www.npmjs.com/~shidianxia) que solo funciona para la versión 1.x de VueJS. La función que ofrece es la de ser un _wrapper_ una envoltura de otro plugin, [`localForage`](https://www.npmjs.com/package/localforage) que facilita la utilización del almacenamiento persistente, el cual fue creado por [tofumatt](https://www.npmjs.com/~tofumatt) .

Cabe destacar que no estoy desarrollando este plugin como un paquete de `npm`, pero lo haré junto con el respectivo artículo.

Entonces, empezamos en agregando al proyecto el paquete `localforage`.

```
yarn add localforage
```

Ya en el archivo de nuestro _plugin_ creamos la clase (¿o será un objeto?) `almacen`.

```
  let almacen = require('localforage')
```

Ahora creamos una variable que será la envoltura de las funciones de `localForage`  en nuestra aplicación de VueJS.

```
  let AlmacenCMI = {
  }
```

En esta envoltura vamos a agregar las funciones que ofrecerá el plugin.

```
  let AlmacenCMI = {
    getItem: (clave, llamada) => almacen.getItem(clave, llamada)
  }
```

Como ven, estamos usando una función _lambda_ por la sencillez de la función. Solo estamos pasando los argumentos del plugin a `localForage` usando funciones *fat arrow* de ES6.

Estas son las funciones y su utilidad.

* `getItem` - regresa la `clave` dada si la encuentra en el almacén o un error.
* `setItem` - almacena un `valor` dado en la `clave` indicada.
* `removeItem` - elimina la `clave` especificada del almacén.
* `clearStorage` - limpia el almacén.
* `lengthOfStorage` - devuelve el tamaño del almacén, contando el número de claves.
* `keyInStorage` - devuelve `true` si la clave existe en el almacén.
* `iterateStorage` - recorre el almacén para realizar operaciones con todas las claves.
* `setStorageDriver` - establece el tipo de almacenamiento persistente que se utilizará.
* `storageConfig` - establece opciones de configuración para el plugin.

Ahora creamos la función prototipo de VueJS que identificará al plugin.

```
  let almacenCMIPlugin = {
    install: function (Vue) {
      Vue.prototype.almacen = AlmacenCMI
    }
  }
```

Y por último lo hacemos dispoible.

```
  almacenCMIPlugin.version = '0.1.0'
  module.exports = almacenCMIPlugin
```

Este es el código completo del plugin.

```
/**
 * Created by javier on 23/03/17.
 */
(function () {
  'use strict'

  let almacen = require('localforage')

  almacen.config({
    driver: [almacen.LOCALSTORAGE],
    name: 'cmiSQL'
  })

  let AlmacenCMI = {
    getItem: (clave, llamada) => almacen.getItem(clave, llamada),
    setItem: (clave, valor, llamada) => almacen.setItem(clave, valor, llamada),
    removeItem: (clave, llamada) => almacen.removeItem(clave, llamada),
    clearStorage: () => almacen.clear(),
    lengthOfStorage: (llamada) => almacen.length(llamada),
    keyInStorage: (keyIndex, callback) => almacen.keyInStorage(keyIndex, callback),
    iterateStorage: (iteratorCallback, callback) => almacen.iterateStorage(iteratorCallback, callback),
    setStorageDriver: (driverName) => almacen.setDrive(driverName),
    storageConfig: (options) => almacen.config(options),
    _properties: {}
  }

  let almacenCMIPlugin = {
    install: function (Vue) {
      Vue.prototype.almacen = AlmacenCMI
    }
  }

  almacenCMIPlugin.version = '0.1.0'
  module.exports = almacenCMIPlugin
})()
```

Ahora, para poder usarlo en nuestra aplicación, debemos importarlo primero, y después activarlo.

```
import Vue from 'vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import App from './App'
import router from './router'
import { store } from './plugins/store'
import AlmacenCMI from './plugins/almacen'     // se importa

Vue.config.productionTip = false
Vue.use(VueAxios, axios)
Vue.use(AlmacenCMI)                           // se activa

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  template: '<App/>',
  components: { App }
})
```

Un ejemplo del uso en el componente principal es el siguiente:

```
<script>
import { mapState } from 'vuex'

export default {
  name: 'app',
  computed: mapState(['token']),
  created () {
    this.almacen.getItem('token')
      .then((payload) => {
        this.$store.state.token = payload
        this.$store.state.acreditado = true
      })
  }
}
</script>
```

Como podemos apreciar, lo usamos como una **promesa**. Primero solicitamos la clave y lo que devuelve lo hacemos disponible en el almacén, usando la función `getItem`.

En este otro ejemplo, al recibir el token, usamos la función `setItem` para enviarlo al almacenamiento persistente.

```
    methods: {
      login () {
        this.axios.post(this.loginURL, this.credenciales)
          .then(response => {
            this.almacen.setItem('token', response.data.auth_token)
          })
      }
    }
```

Por supuesto, pude haber usado nombres de funciones en español para hacerlo más fácil, pero como pienso convertirlo en un plugin y hacerlo público en realidad de pasarlo todo a inglés, documentarlo y agregarle algunas pruebas (_si supera como_).
