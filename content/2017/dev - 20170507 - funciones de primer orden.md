Title: Funciones de primer orden    
Date: 2017-05-07 14:53:30
Category: desarrollo
Tags: javascript, patterns, es6
Summary: 
Series: Programación Funcional

De manera general, podemos decir que las __Funciones de Primer Orden__[^1] son _abstracciones_ de problemas comunes. 

### Abstracciones

La Wikipedia[^2] nos dice que la **abstracción** consiste en aislar un elemento de su contexto. Es decir, hablado ya de funciones, el término hace énfasis en el _”que hace”_ y no en el “como lo hace”. La verdad, está mejor la definición en la versión en inglés:

> La **abstracción** es una técnica para organizar la complejidad de los sistemas informáticos. Funciona estableciendo un nivel de complejidad en el cual, se eliminan los detalles más complejos cuando una persona interactúa con el sistema. El programador trabaja con una interfaz idealizada (generalmente bien definida) y puede agregar niveles adicionales de funcionalidad que de otro modo serían demasiado complejos de manejar.

y pone como ejemplo lo siguiente:

> supongamos que un programador escribe un programa que involucra operaciones numéricas, pero puede que no esté interesado en la forma en la que los números se muestran debido al hardware (por ejemplo si es de 16, 32 o 64 bits), y como no le interesa, no incluye detalles sobre su presentación. Es decir, ha hecho una _abstracción_ dejando solo los números que es con lo que trabaja.

La abstracción nos permite trabajar en el objetivo sin preocuparnos con los conceptos subyacentes.

### Abstracción y las funciones de primer orden
Y las funciones de primer orden nos ayudan a lograr el concepto de abstracción. Vean por ejemplo esta función.

```js
const _cadaUno = (arreglo, fn) => {
  for (let i=0; i < arreglo.length; i++){
    fn(arreglo[i])
  }
}
```


Esta función es una forma de abstraer el concepto de _recorrer un arreglo_. El usuario de la API `cadaUno` no necesita comprender como está implementada en esta función el problema de recorrer el arreglo, por lo tanto se ha abstraído del problema.

!!! notice "Cómo funciona `cadaUno`"
    Dentro de la función, se llama a la función `fn` que le pasamos con un único argumento, en cada una de las vueltas que da con los datos del `arreglo`. Por ejemplo si le pasamos la función `consola`:
    

        cadaUno([1, 2, 3], consola)
   
    
    Veremos los números, uno en cada línea:

         > cerebro@0.1.0 start /Volumes/datos/Proyectos/cerebro
         > babel-node src/index.js

         Hola mundo
         1
         2
         3


Una función de primer orden para obtener las propiedades de un objeto se vería así:

```js
const _cadaPropiedad = (objeto, funcion) => {
  for (var propiedad in objeto) {
    if (objeto.hasOwnProperty(propiedad)) {
      // Llamamos a la funcion con la clave y valor
      // como argumentos
      funcion(propiedad, objeto[propiedad])
    }
  }
}
```

!!! notice "Como funciona `cadaPropiedad`"
    `cadaPropiedad` toma como primer argumento un objeto de JavaScript y como segundo argumento una función. Recorre el objeto usando el algoritmo anterior y llama a la `funcion` con la clave y el valor como argumentos.

```js
let objeto = {a: 1, b: 2}
cadaPropiedad(objeto, (k, v) => consola(`=> ${k}: ${v}`))
```   

Y funciona de la siguiente manera:
```bash
> $ npm start

> cerebro@0.1.0 start /Volumes/datos/Proyectos/cerebro
> babel-node src/index.js

=> a: 1
=> b: 2
```

Las funciones `cadaUno` y `cadaPropiedad` son funciones de primer orden que nos permiten trabajar en la tarea que nos ocupa, sin preocuparnos por la parte de recorrer los objetos o arreglos. 

También es posible crear funciones de primer orden para controlar flujos de programa. Por ejemplo, vamos a crear una función que se llame `soloSi`. Esta función tomo como argumento un `predicado` (que debe ser `true` o `false`) y _solo si_ es `false` llama a la función `fn` que le pasamos como segundo parámetro.

```js
const _soloSi = (predicado, fn) => {
  if (!predicado)
    fn()
}
```

Con esta función vamos a crear un pequeño código que busca números pares, por supuesto haciendo uso de las funciones de primer orden que hemos creado.
```js
cadaUno([1, 2, 3, 4, 5, 6, 7], (numero) => {
  soloSi((numero % 2), () => {
    consola(`${numero} es par`)
  })
})
```

Y al ejecutar nuestra función obtenemos el resultado esperado.
```js
> $ npm start

> cerebro@0.1.0 start /Volumes/datos/Proyectos/cerebro
> babel-node src/index.js

2 es par
4 es par
6 es par
```

Ahora, ¿qué pasaría si quisiéramos obtener los números pares, digamos que del 1 al 100? Podríamos usar la función `cadaUno` pero tendríamos que pasarle todo el arreglo con los 100 números. 

Mejor vamos a escribir una función de primer orden a la que vamos a llamar `tantasVeces`, a la llamaremos con dos argumento, un número y una función que se ejecutará _tantas veces_ como el número que le pasemos. 

```js
const _tantasVeces = (veces, fn) => {
  for (var i = 0; i < veces; i++) 
    fn(i)
}
```

Esta función es casi idéntica a la de `cadaUno`, solo que usa números en lugar de arreglos. Ahora la vamos a usar para resolver el problema de los números pares.
```js
tantasVeces(100, (n) => {
  soloSi(n % 2, () => consola(`${n} es par`))
})
```

Y la salida es la esperada
```js
> $ npm start

> cerebro@0.1.0 start /Volumes/datos/Proyectos/cerebro
> babel-node src/index.js

0 es par
2 es par
4 es par
6 es par
8 es par
10 es par
...
```

El código anterior es un conjunto de abstracciones que da como resultado funciones de primer orden simples y concisas.

Así se ve el archivo de `utilidades.js` que contiene todas las funciones que hemos visto hasta ahora:

```js
const _consola = (mensaje) => console.log(mensaje)

const _cadaUno = (arreglo, funcion) => {
  for (let i = 0; i < arreglo.length; i++) {
    funcion(arreglo[i])
  }
}

const _cadaPropiedad = (objeto, fn) => {
  for (var propiedad in objeto) {
    if (objeto.hasOwnProperty(propiedad)) {
      fn(propiedad, objeto[propiedad])
    }
  }
}

const _soloSi = (predicado, fn) => {
  if (!predicado)
    fn()
}

const _tantasVeces = (veces, fn) => {
  for (var i = 0; i < veces; i++)
    fn(i)
}

module.exports = {
  consola: _consola,
  cadaUno: _cadaUno,
  cadaPropiedad: _cadaPropiedad,
  soloSi: _soloSi,
  tantasVeces: _tantasVeces
}
```

Y así se usa en el último ejemplo:

```js
import {consola, soloSi, tantasVeces} from './lib/utilidades.js'

tantasVeces(100, (n) => {
  soloSi(n % 2, () => consola(`${n} es par`))
})
```


[^1]: También las llaman funciones de orden superior porque en inglés se llaman así: _High-Order Function_.
[^2]: https://es.wikipedia.org/wiki/Abstracción_(informática)
