Title: Invocación de Funciones en JavaScript  
Date: 2014/03/18 22:42  
Category: Desarrollo  
Tags: this, funciones, patterns  
Slug:  
Author: Javier Sanchez Toledano  
email: javier@namespace.mx  
Summary:  

La invocación de funciones en JavaScript siempre ha causado confusión. En particular, mucha gente se queja que la semántica para invocar a la función `this` es confusa.

En mi opinion<sup>1</sup> mucha de esta confusión se soluciona al entender la invocación primaria de funciones en JavaScript, y luego viendo otras maneras de realizar esta invocación pero con más "adornos". De hecho, así es como el estándar ECMAScript especifica que debe hacerse. Este post es una simplificación de ese estándar.

### La invocación primitiva

Primero, veamos como hacer una invocación  a una función primitiva, al método `call` de una función. El método `call` es relativamente sencillo.

1. Se hace una lista de argumentos (àrgList`) desde el parámetro 1 hasta el último.
2. El primer parámetro es `thisValue``
3. Se llama a la función con `this` establecido como `thisValue`y a `argList` como lista de argumentos.

Por ejemplo:

```
function hola(cosa) {
  console.logout(this + " dice hola " + cosa);
}

hola.call("Javier", "mundo");  // --> Javier dice hola mundo
```

Com podrás ver, invocamos el método `hola` con `this`establecido como "Javier" y un solo argumento, "mundo". Esta es la forma primitiva de invocación de funciones en JavaScript. Es válido, entonces, pensar que todas las otras formas de llamar a una función son _variaciones_ a esta forma primitiva. 

### Invocación simple de funciones

Evidentemente, invocar a las funciones con el método `call` puede llegar a ser bastante molesto, por eso JavaScript permite llamar a las funciones usando la sintaxis de paréntesis (`hola("mundo")`). Cuando lo hacemos así, la invocación se simplifica.

```
function hola(cosa) {
  console.logout(this + " dice hola " + cosa);
}

hola("mundo");

// se convierte en
hola.call(window, 'mundo');
```

Este comportamiento cambia en el estándar ECMAScript 5, solo cuando se usa el modelo estricto.

```
// esto:
hola("mundo");

// se convierte en esto:
hola.call(undefined, "mundo");
```

> __Simplificando:__ la invocación de una función como `fn(…args)` es lo mismo que `fn.call(window, …args)` o según el estándar EMACScript 5 `fn.call(undefined, …args)`.
> 
Esto también aplica para las funciones declaradas en línea: `(function() {})()` es lo mismo que `(function() {}).call(window)`.