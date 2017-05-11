Title: Transparencia Referencial    
Date: 2017-05-05 19:50:52
Category: desarrollo
Tags: javascript, patterns,  
Series: Programación Funcional  
Summary: 

Ahora estoy aprendiendo algunos paradigmas de programación (_programming patterns_) y hay algunos que aunque al principio pueden parecer muy obvios son muy interesantes, como este que se llama **transparencia referencial**. O bueno, así le puse yo.

Dada la definición de función que dice:

> Una **función** es una pieza de código que puede llamarse por su nombre, tomar argumentos y regresar valores…  

la _transparencia referencial_ dice que **una función siempre regresará el mismo valor para el mismo argumento**.

Veamos esta simple función:

```js
let identidad = i => i
```

Lo único que hace esta función es regresar el valor que le pasamos como argumento. Por ejemplo, si le pasamos un `5`, regresa un `5`. Solo opera con el argumento que le pasamos, sin referencias al alcance global. Y por supuesto cumple con el principio de integridad referencial.

Ahora imaginemos que usamos la función `identidad` en otra función, como esta:

```javascript
suma(3, 4) + identidad(1)
```

Debido al principio de _integridad referencial_, podemos convertir la sentencia anterior en la siguiente:

```js
suma(3, 4) + 1
```

Este proceso se llama **modelo de sustitución** porque podemos sustituir el resultado de la función por su valor (básicamente porque no depende de otros valores). Esto nos lleva al código **en paralelo** y al **cacheo**.

No es poca cosa. Podemos ejecutar el código anterior en múltiples hilos que no necesitan estar sincronizados. O sea, la necesidad de la sincronización parte del hecho que los hilos no deben actual sobre datos globales cuando se ejecutan en paralelo. Las funciones que cumplen con el principio de Integridad Referencial solo dependen de los argumentos de entrada, por lo tanto, los hilos son libres de ejecutarse sin ningún mecanismo de bloqueo.

Luego, ya que la función va a devolver el mismo valor para el argumento dado podemos, de hecho, podemos guardarlo en una memoria cache. Por ejemplo, imaginemos que tenemos una función llamada `factorial` que hace lo que indica su nombre en un número dado. ¿Qué pasa cuando un usuario llama a la función con el argumento `5`? Sabemos que el factorial de `5` es `120`. ¿Qué pasa cuando llamamos a  `factorial(5)`  por segunda vez? Si nuestra función obedece al principio de **transparencia referencial**, sabemos que el resultado será `120` como antes (ya que solo depende de los argumentos de entrada). Con esta característica en mente, podemos almacenar en cache los valores de nuestra función `factorial` y regresar `120`  cuando la función se llame con el argumento `5` sin tener que hacer los mismos cálculos otra vez.

Como podemos apreciar, este sencillo principio tiene importantes implicaciones que iremos descubriendo en el aprendizaje con JavaScript.
