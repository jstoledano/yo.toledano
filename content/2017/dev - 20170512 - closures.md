Title: Que son las closures    
Date: 2017-05-12 14:00:00
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


Ahora, cuando se ejecute la función `interna()` se imprimerá el valor de `global` (que también es `global`). Esto es porque las _closures_ pueden acceder a las variables globales (punto 2).

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
