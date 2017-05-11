Title: Verificación de Token en VueJS    
Date: 2017-03-25 21:15:40
Category: desarrollo
Tags: vuejs, acreditacion, mixins 
Summary: Una primera aproximación a un servicio para verificar que existe un token de acreditación con VueJS.

Hace unos meses intenté hacer la aplicación del Cuadro de Mando Integral, el CMI, usando AngularJS. Aunque hice algunos avances, realmente nunca logré entenderlo del todo[^1].

[^1]: O tal vez lo abandoné muy pronto.

Logré hacer un servicio para la acreditación de usuarios en AngularJS y ahora trato de replicarlo en VueJS. Y de hecho, ya lo logré de manera muy burda.

En el componente principal de mi aplicación tengo el siguiente código:

```javascript
import { mapState } from 'vuex'

export default {
  name: 'app',
  computed: mapState(['token', 'fuera']),
  created () {
    this.almacen.getItem('token')
      .then((payload) => {
        this.token = payload
        this.fuera = false
      })
  }
}
```

Usa el plugin `almacen` que vimos en el [artículo anterior](https://yo.toledano.org/desarrollo/como-crear-un-plugin-para-vuejs.html) y lo primero que hace es _mapear_ los elementos del almacén general al almacen de Vuex. Específicamente las claves `token` y `fuera`. Esta última es una variable _booleana_ que al inicio es `true`.

Entonces buscamos el `token` en el almacen, con `this.almacen.getItem('token')` y una vez que tenemos la respuesta de la promesa hace dos cosas, primero almacena la clave en el almacen de Vuex con `this.token = payload` y cambia la variable `fuera` a `false`.

En la aplicación de AngularJS, se hace de la siguiente manera.

```javascript
(function(angular){
  'use strict';

  angular
    .module('cmi')
    .service('session', sessionService);

  sessionService.$inject = ['$log', 'localStorage'];

  function sessionService($log, localStorage){
    // jshint validthis: true
    var self = this;

    // API Pública
    self.getUser = getUser;
    self.setUser = setUser;
    self.getAccessToken = getAccessToken;
    self.setAccessToken = setAccessToken;
    self.destroy = destroy;

    var _user = JSON.parse(localStorage.getItem('session.username'));
    var _accessToken = JSON.parse(localStorage.getItem('session.accessToken'));

    function getUser(){
      return _user;
    }     // getUser()

    function setUser(user){
      _user = user;
      localStorage.setItem('session.username', JSON.stringify(user));
      return _user;
    }     // setUser()

    function getAccessToken(){
      return _accessToken;
    }     // getAccessToken()

    function setAccessToken(token){
      _accessToken = token;
      localStorage.setItem('session.accessToken', JSON.stringify(token));
      return _accessToken;
    }     // setAccessToken()

    function destroy(){
      setUser(null);
      setAccessToken(null);
    }     // destroy()
  }
})(angular);
```

Este es un _servicio_, pero en VueJS no existen, así que debemos encontrar una manera de replicarlo.

## Mixins

Los _mixins_ son una forma flexible de distribuir funcionalidades reutilizables en componentes de Vue. Un objeto _mixin_ puede contener cualquier opción de un componente. Cuando un componente usa un mixin, todas las opciones de este mixin se _"mezclan"_ con las del propio componente.

Esta podría ser la solución para lo que buscamos.

Vamos a crear la carpeta de _mixins_ y vamos a convertir la función que tenemos en `created()` en su equivalente `getAccessToken` de AngularJS.


El _mixin_ para que pueda ser exportado debe tener esta estructura.

```javascript
export default {
    // propiedades calculadas,
    // métodos,
    // data,
    // ganchos de montaje
    // etc.
}
```

Y en el componente donde _importamos_ el mixin, se hace así.

```javascript
import unNombreParaMiMixin from '/la/ruta/del/mixin'
```

Es decir, que es posible llamar al mixin de diferentes maneras en cada componente. No tendría mucho sentido hacer eso, pero es posible.

Ahora veamos el contenido del mixin.

Lo primero que hice fue agregar `mapState` como una dependencia.

    import { mapState } from 'vuex'

Luego, _mapeo_ dos variable, el `token` y `fuera`[^2].

    computed: mapState(['token', 'fuera']),

[^2]: Creo que no necesito esta variable, porque basta con comprobar que `token` tenga información.

Cuando se mezcle el mixin con los componentes, estas dos variables estarán disponibles.

Ahora agrego un método que lee el token de `localStorage` y si existe lo coloca en el almacen de Vuex (en `token`) y cambia la variable `fuera` a `false`. En caso que no exista el `token`, `fuera` queda en `true`. Asi se verifica si el usuario está acreditado en la aplicación.

```javascript
  methods: {
    getAccessToken: function () {
      this.almacen.getItem('token')
        .then((payload) => {
          if (payload) {
            this.$store.state.token = payload
            this.$store.state.fuera = false
          } else this.$store.state.fuera = true
        }).catch((e) => console.log(`Error ${e}`))
    }
  },
```

Por último, agregué un gancho a `created()` y llama a esta función `getAccessToken`.

```javascript
  created () {
    this.getAccessToken()
  }
```

Ahora bien, creo que no debería usar este gancho, porque entonces si uso este _mixin_ en más de un componente, la función sería llamada cada vez, aunque no sea necesario. 

Lo más conveniente será que la use el componente principal únicamente, y en el componente haré esto mismo.

```javascript
import sessionService from './mixins/session.mixin'

export default {
  name: 'app',
  mixins: [sessionService],
  created () {
    this.getAccessToken()
  }
}
```

Primero se llama al mixin, y luego a los ganchos.

El código completo se ve así.

```javascript
import { mapState } from 'vuex'

export default {
  computed: mapState(['token', 'fuera']),
  methods: {
    getAccessToken: function () {
      this.almacen.getItem('token')
        .then((payload) => {
          if (payload) {
            this.$store.state.token = payload
            this.$store.state.fuera = false
          } else this.$store.state.fuera = true
        }).catch((e) => console.log(`Error ${e}`))
    }
  }
}
```
