Title: Funciones de primer orden II    
Date: 2017-05-09 19:29:25
Category: desarrollo
Tags: javascript, closures, patterns 
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