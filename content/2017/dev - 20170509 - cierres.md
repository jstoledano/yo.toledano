Title: Funciones de primer orden II    
Date: 2017-05-09 19:29:25
Category: desarrollo
Tags: javascript, patterns 
Summary: 


Creo que es muy importante comprender correctamente qué son y el papel de las funciones de primer orden en la programación funcional. Vamos a seguir revisando este paradigma de programación con funciones cada vez más concretas y con aplicación en el día a día.

### La función `todos`

Es frecuente que, cuando programamos, tengamos que verificar si un arreglo contiene números, un objeto o alguna otra cosa (pensemos en los _requisitos_ de las metas). Lo que haríamos sería un ciclo `for` para resolver este problema. Pero también podemos hacer una abstracción usando nuestra función `todos`. La función `todos` recibe dos argumentos: una arreglo y una función. Lo que hace es verificar si todos los elementos del arreglo se evalúan como `true` por la función que le pasamos como argumento. La implementación se ve así:

    :::javascript
    const _todos = (arr, fn) => {
      let resultado = true
      for (let i = 0; i < arr.length; i++)
        resultado = resultado && (fn(arr[i]))
    }

Simplemente es un ciclo que recorre todo el arreglo y llama a la función `fn` con cada valor. Ahora bien, la función `fn` __debe__ regresar un valor _Booleano_, porque con este hacemos una prueba lógica `&&` para asegurar que el contenido del arreglo obedece al criterio dado por `fn`.

Para verificar el funcionamiento de nuestra función, vamos a pasarle un arreglo de valores `NaN` y la función `isNaN()` como argumento para que verifique si el número dado es `NaN` o no.

    :::bash
    consola(todos([NaN, NaN, NaN], isNaN))
    > true
    consola(todos([NaN, NaN, NaN, 4], isNaN))
    > false

La función `todos` es una típica función de primer orden que ademas de ser fácil de implementar es realmente útil. Antes de pasar a la siguiente, vamos a _refactorizar_ nuestra función para aprovechar el nuevo ciclo `for..of` de la implementación ES6 para recorrer los elementos del arreglo.

    :::js
    const _todos = (arr, fn) => {
      let resultado = true
      for(const valor of arr)
        resultado = resultado && fn(valor)
      return resultado
    }


### Función `algunos`
Muy similar a la función `todos`, tenemos esta función llamada `algunos`, aunque funciona de forma un poco diferente porque esta devuelve `true` solo si la función regresa `true` para _algunos_ de los elementos del arreglo. Para poder implementar esta función usaremos `||` en lugar de `&&`.

    :::js
    const _algunos = (arr, fn) => {
      let resultado = false
      for (const valor of arr)
        resultado = resultado || fn(valor)
      return resultado
    }

> Antes de continuar, ya sé que estas implementaciones son muy ineficientes. `todos` debe recorrer el arreglo hasta el primer elemento que no cumpla con el criterio y `algunos` recorre el arreglo hasta la primera coincidencia. Para arreglos muy grandes sería muy ineficiente. Pero como el objetivo es entender los conceptos de las funciones de primer orden, le daremos preferencia a la parte didáctica.

Vamos a ver como funciona nuestra función `algunos`.

    > consola(algunos([NaN, NaN, 4], isNaN))
    true
    > consola(algunos([3, 4, 4], isNaN))
    false

Todavía nos falta un ejemplo más complejo que involucra el concepto de __abstracción__, pero seguiremos en el siguiente artículo.

### La función `ordenarPor`
En ECMAScript 6 existe una función interna `sort()` en el prototipo de Array que se usa de la siguiente manera. Supongamos que necesitamos ordenar una lista de frutas.

    :::js
    let frutas = ['sandias', 'peras', 'manzanas'] 

podemos usar la función `sort()` que contiene el prototipo, simplemente haciendo esto:

    :::javascript
    > frutas.sort()
    [ 'manzanas', 'peras', 'sandias' ]

Es así de simple. `sort()` es una función de primer orden que toma una función como argumento y que usa como criterio de ordenación. En términos simples, podemos describir la función `sort()` de la siguiente forma:

    :::javascript
    arreglo.sort([funciónCriterioOrdenación])

Aquí la función `funciónCriterioOrdenación`  es opcional. Si no se proporciona, los elementos para ser ordenados se convierten en cadenas que se comparan por medio de su código Unicode. No tenemos que preocuparnos por la conversión a Unicode en este momento, así que la dejamos de lado. Lo que importa es que para poder ordenar los elementos usando nuestro propio criterio, necesitamos pasar nuestra función `funciónCriterioOrdenación()`. En este sentido, podemos ver la flexibilidad que tienen las funciones de primer orden.

Para poder crear nuestra función `criterioOrdenacion` debemos cumplir con las características especificadas aquí: https://developer.mozilla.org/es/docs/Web/JavaScript/Referencia/Objetos_globales/Array/sort

    función criterioOrdenacion(x, y) {
      si (x es menor que y de acuerdo al criterio) {
        regresar -1
      }
      si (x es mayor que y de acuerdo al criterio) {
        regresar 1
      }
      // si x es igual a y
      regresar 0
    }


Para facilitar la comprensión, pensemos en el siguiente ejemplo:
```javascript
const personas = [
  {nombre: "aaaNombre", paterno: "cccPaterno"},
  {nombre: "cccNombre", paterno: "aaaPaterno"},
  {nombre: "bbbNombre", paterno: "bbbPaterno"},
]
```

Necesitamos ordenar `personas` por la clave `nombre`, por lo que vamos a pasarle a la función `sort()` nuestra función que sirva como criterio de ordenación:

```javascript
> personas.sort((x, y) => {
...   return (x.nombre < y.nombre) ? -1: (x.nombre > y.nombre) ? 1 : 0
... })
```
lo que da como resultado:
```javascript
[ { nombre: 'aaaNombre', paterno: 'cccPaterno' },
  { nombre: 'bbbNombre', paterno: 'bbbPaterno' },
  { nombre: 'cccNombre', paterno: 'aaaPaterno' } ]
```

Ahora si queremos usar como criterio de ordenación el apellido paterno, entonces debemos hacer lo siguiente:
```javascript
personas.sort((x, y) => {
  return (x.paterno < y.paterno) ? -1: (x.paterno > y.paterno) ? 1 : 0
})
```

que nos regresa el resultado esperado:

```javascript
[ { nombre: 'cccNombre', paterno: 'aaaPaterno' },
  { nombre: 'bbbNombre', paterno: 'bbbPaterno' },
  { nombre: 'aaaNombre', paterno: 'cccPaterno' } ]
```

Vamos a regresar un momento a nuestro algoritmo de ordenación:

    función criterioOrdenacion(x, y) {
      si (x es menor que y de acuerdo al criterio) {
        regresar -1
      }
      si (x es mayor que y de acuerdo al criterio) {
        regresar 1
      }
      // si x es igual a y
      regresar 0
    }

Ahora que ya vimos como funciona, ¿podemos mejorarlo? El lugar de escribir la función `criterioOrdenacion` cada vez, ¿podríamos abstraer la lógica en una función de primer orden? Como pudimos observar el código para comparar el nombre o el apellido paterno es idéntico, solo cambiaba la clave o propiedad. 

Nuestra función de primer orden no va tomar como argumento una función, sino que _va a devolver una función_. Vamos a llamar a esta función `ordenarPor`, que permite ordenar un arreglo de objetos usando como criterio de ordenación la propiedad que le pasemos como argumento.

```javascript
const _ordenarPor = (propiedad) => {
  return (a, b) => {
    let resultado = (a[propiedad] < b[propiedad]) ? -1 : (a[propiedad] > b[propiedad]) ? 1 : 0
    return resultado
  }
}
```

La función `ordenarPor` toma como argumento a `propiedad` y regresa una función que toma dos argumentos:

```js
...
  return (a, b) => { }
...
```

Esta función lo que hace es usar la lógica que vimos en el algoritmo de `criterioOrdenacion`:

```js
    let resultado = (a[propiedad] < b[propiedad]) ? -1 : (a[propiedad] > b[propiedad]) ? 1 : 0
```

Imaginemos que llamamos a la función `ordenarPor` usando la propiedad `nombre`. Lo que pasaría es que `propiedad` será reemplazado por `nombre` y se convertiría en:

```js
    let resultado = (a[nombre] < b[nombre]) ? -1 : (a[nombre] > b[nombre]) ? 1 : 0
```

Y eso es lo que hicimos cuando escribimos _manualmente_ la función. Veamos como funciona:

```javascript
> consola(personas.sort(ordenarPor('nombre')))

> cerebro@0.1.0 start /Volumes/datos/Proyectos/cerebro
> babel-node src/index.js

[ { nombre: 'aaaNombre', paterno: 'cccPaterno' },
  { nombre: 'bbbNombre', paterno: 'bbbPaterno' },
  { nombre: 'cccNombre', paterno: 'aaaPaterno' } ]

Process finished with exit code 0
```

Y para ordenar por apellido `paterno`

```js
> consola(personas.sort(ordenarPor('paterno')))
> cerebro@0.1.0 start /Volumes/datos/Proyectos/cerebro
> babel-node src/index.js

[ { nombre: 'cccNombre', paterno: 'aaaPaterno' },
  { nombre: 'bbbNombre', paterno: 'bbbPaterno' },
  { nombre: 'aaaNombre', paterno: 'cccPaterno' } ]

Process finished with exit code 0
```

En este ejemplo usamos varias funciones de primer orden: `consola` para mostrar el resultado, `sort()` una función interna para ordenar y `ordenarPor` para definir el criterio de ordenación. Y de eso se tratan las funciones de alto nivel, de abstracción.

Antes de terminar, debemos notar que la función `ordenarPor` es una función que se pasa como parámetro a la función `sort()`, pero lleva el argumento `propiedad` que le pasamos. ¿Cómo es posible? Gracias a los _cierres_ o __*closures*__ que empezaremos a ver en el siguiente artículo.
