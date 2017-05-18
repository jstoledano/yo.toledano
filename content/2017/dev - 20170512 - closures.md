Title: Que son las closures    
Date: 2017-05-17 19:37:22
Category: desarrollo
Tags: javascript, patterns, es6
Summary:

La verdad no encontré una buena traducción de __*closure*__. Literalmente, significa _"cierre"_, pero no tiene mucho sentido en el contexto de la programación funcional. Es uno de esos conceptos que para comprenderlo hay que verlo o hacerlo.

Para explicarlo de forma simple, una _closure_ es una función interna, es decir, __una función *dentro* de otra función__. Algo asi:

    :::js
    function externa() {
      function interna() {
      }  
    }

La función `interna()` es una **closure**. Y la razón por la que las *closures* son tan importantes es porque tiene acceso al alcance **en cadena** (o al alcance en niveles). Me explico:

Técnicamente, una _closure_ tiene tres alcances:

1. El alcance de las variables declaradas __dentro__ de la definición de la función
1. El alcance de las variables **globales**
3. El alcance de las variables en __la función externa__

Vamos a revisar estos tres aspectos de forma independiente usando un ejemplo. Para empezar, tenemos el siguiente ejemplo:

    :::javascript
    function externa(){
      function interna(){
        let a = 5
        console.log(a)
      }
      interna()    // llamamos a la función interna
    }


que imprime en la consola el valor de `a` cuando se llama a `interna()`. Esto se debe al punto uno: una función _closure_ puede acceder a las variables declaradas en su propia definición.

Ahora vamos a modificar un poco el código anterior...

    :::javascript
    let global = "global"
    function externa(){
      function interna(){
        let a = 5
        console.log(global)
      }
      interna()    // llamamos a la función interna
    }


Ahora, cuando se ejecute la función `interna()` se imprimirá el valor de `global` (que también es `global`). Esto es porque las _closures_ pueden acceder a las variables globales (punto 2).

El punto 3, es muy interesante y lo vamos a ejemplificar con el siguiente fragmento.

    :::javascript
    let global = "global"
    function externa(){
      let externa = "externa"
      function interna(){
        let a = 5
        console.log(externa)
      }
      interna()    // llamamos a la función interna
    }

ahora la variable que se imprime es `externa`, como corresponde. Puede parecer muy simple, pero esta es una de las características más importantes de las `closures`.

!!! notice "Nota"
    Las _closures_ tienen acceso a las variables que se pasan como parámetros a la función externa. En el ejemplo desde la función `interna()` se tiene acceso a las variables que recibe `externa()` como parámetros.

### El contexto y las closures
Las _closures_ tienen otra característica importante: _recuerdan su contexto_. Veamos este ejemplo:

    :::js
    let fn = (arg) => {
      let externa = "Visible"
      let fnInterna = () => {
        console.log(externa)
        console.log(arg)
      }
      return fnInterna
    }

El código es, relativamente, simple. La función `fnInterna()` es una función _closure_ de `fn()` y `fn` regresa a `fnInterna` cuando se llama. Hasta aquí, nada nuevo. Pero veamos como funciona.

    :::js
    > let closureFn = fn(5)
    > closureFn()
    Visible
    5

Para entender mejor como es que al llamar a `closureFn()` se imprime `Visible` y `5` en la pantalla vamos ver que sucede tras bambalinas:

1. Cuando llamamos el código siguiente:

        :::javascript
        let closureFn = fn(5)

    llamamos a la función `fn` con el argumento `5`. Tal como está definida nuestra función, regresará `fnInterna()`.

1. En este momento ocurre lo interesante. Cuando se regresa la función `fnInterna`, la máquina virtual de JavaScript ve una _closure_ y establece su __alcance__ de forma adecuada. Y comovimos anteriormente, las _closures_ tienen acceso a los tres niveles de alcance. Estos tres niveles se __*encadenan*__ (los valores de `arg` y `externa` se establecerán en el alcance del nivel de `fnInterna`) cuando se regresa `fnInterna`. La función regresa se almacena en `closureFn`que recuerda a `arg` y `externa` porque están en el alcance encadenado.

1. Cuando finalmente llamamos a `closureFn` con

        :::javascript
        closureFn()

    imprime

        :::javascript
        Visible
        5

 Como podemos observar por la salida, `closureFn` recuerda su contexto (es decir el encadenamiento de los alcances, por ejemplo `externa` y `arg`) cuando es creada en el paso dos, por lo que el `console.log` funciona apropiadamente.

 Si se preguntan cuándo usar este tipo de funciones, la verdad es que ya lo hicimos en nuestra función `ordenarPor`.


### Revisando la función `ordenarPor`

Vamos a revisar rápidamente la función `ordenarPor` que definimos en un [artículo anterior](/desarrollo/funciones-de-primer-orden-ii.html#la-funcion-ordenarpor).


    :::javascript
    const _ordenarPor = (propiedad) => {
      return (a, b) => {
        let resultado = (a[propiedad] < b[propiedad]) ? -1 : (a[propiedad] > b[propiedad]) ? 1 : 0
        return resultado
      }
    }

Cuando llamamos a la función de esta forma:

    :::javascript
    ordenarPor("nombre")

esto es lo que pasa

1. `ordenarPor` regresa una nueva función que toma dos argumentos como estos:

        :::javascript
        (a, b) => { /* implementación */ }

1. Ahora que sabemos un poco mas acerca de las _closures_, estamos conscientes que la función devuelta tiene acceso a `propiedad` de la función `ordenarPor`. Ya que la función solo se devuelve cuando se llama a `ordenarPor`, el argumento `propiedad` se resuelve con un valor, por lo tanto, la función devuelta traerá el _contexto_ junto con ella.

        :::javascript
        // el alcance se anexa a las closure
        propiedad = "valorDevuelto"
        (a, b) => { /* implementación */ }


1. Ahora que la función devuelta lleva el valor de propiedad en su contexto, usará el valor regresado donde sea apropiado y cuando sea necesario.

Las _closures_ son una característica muy usada en JavaScript y conforme avancemos en el estudio del lenguaje y la programación funcional veremos más ejemplos que nos ayuden a dominar este concepto.
