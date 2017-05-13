Title: Dividiendo las rutas en VueJS    
Date: 2017-04-02 00:17:06
Category: desarrollo 
Tags: javascript, vuejs, es6, patterns
Summary: 

Pregunté en [Stackoverflow en Español](http://es.stackoverflow.com/questions/59572/unir-dos-routers-en-vuejs) como dividir mis rutas, tal como lo hacen en Django y aunque hay una excelente respuesta, no se relaciona con mi pregunta de forma directa. 

Así que pregunté en los foros de VueJS y resolvieron mi duda de la mejor manera posible.

Preguntaba si podía tener dos objetos `Router`, la respuesta es __no__, no se puede. 

Sin embargo la alternativa es muy elegante.

Hace uso de un operador de [_destructuración_](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Destructuring_assignment) identificado por tres puntos `...` (que había usado sin entenderlo cabalmente).

Este operador devuelve los elementos __*restantes*__ de un array, es decir, aquellos que no han sido asignados en una _destructuracion_.

- Primero, hacemos un _array_ o arreglos de objetos que podamos pasarle al objeto _Router_. 

    Además de la ruta y el componente, podemos indicar un nombre y propiedades. O mejor aún, como sugiere atinadamente [__@Gustavo García__](http://es.stackoverflow.com/a/59651/638), usar vistas anidadas. Por el momento, usaremos estas rutas sencillas.

        import rechazosIndex from './rechazos.index'
        import conjuntoIndex from './conjuntos.index'
        import conjuntoDetail from './conjuntos.detail'
    
        export default [
          {path: '/rechazos', component: rechazosIndex},
          {path: '/rechazos/conjuntos/', component: conjuntoIndex, name: 'conjuntoIndex'},
          {path: '/rechazos/conjuntos/:id', component: conjuntoDetail, name: 'conjuntoDetail', props: true}
        ]
    El operador `...` hace que los elementos que no han sido asignados en una reestructuración previa, es decir, el resto o __los elementos restantes__ (en este caso, _todos_) pasen al array padre, que en el ejemplo es `routes`.

- Hacemos lo mismo para la ruta de la portada y para las rutas usadas en la acreditación.

    En `portada.routes.js` tenemos:

        import portadaIndex from './portada.index'

        export default [
          {path: '/', name: 'portadaIndex', component: portadaIndex}
        ]

    Y en `index.routes.js` podemos ver: 
        import Login from './Login'

        export default [
          {path: '/login', name: 'Login', component: Login}
        ]

Estos archivos y los que resulten en el desarrollo del proyecto, los usaremos en el `Router` usando este operador de desestructuración, que tomará estos arrays y los agregará al router.

De este modo, pasé de tener esto:

```javascript
import Vue from 'vue'
import Router from 'vue-router'
import portadaIndex from '../components/portada.index'
import Login from '../components/login/Login'
// import rechazosRouter from '../components/rechazos/rechazos.router'

import rechazosIndex from '../components/rechazos/rechazos.index'
import conjuntoIndex from '../components/rechazos/conjuntos.index'
import conjuntoDetail from '../components/rechazos/conjuntos.detail'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {path: '/', name: 'portadaIndex', component: portadaIndex},
    // Rechazos
    {path: '/rechazos/', name: 'rechazosIndex', component: rechazosIndex},
    {path: '/rechazos/conjuntos/', component: conjuntoIndex, name: 'conjuntoIndex'},
    {path: '/rechazos/conjuntos/:id', component: conjuntoDetail, name: 'conjuntoDetail', props: true},
    // Login
    {path: '/login', name: 'Login', component: Login}
  ]
})
```

A tener esto:

```javascript
import Vue from 'vue'
import Router from 'vue-router'

import portadaRoutes from '../components/portada.routes'
import rechazosRoutes from '../components/rechazos/rechazos.routes'
import authRoutes from '../components/login/auth.routes'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    ...portadaRoutes,
    ...rechazosRoutes,
    ...authRoutes
  ]
})
```

La diferencia es verdaderamente notable.

Gracias a [lcdss](https://forum.vuejs.org/users/lcdss/activity) por la respuesta. 
