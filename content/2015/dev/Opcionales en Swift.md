Title:  Opcionales en Swift   
Date: 2017-12-26 07:19:35
Category: desarrollo
Tags: lvlBasico, swift
Summary: 


En este artículo continuamos viendo, ahora con mayor profundidad, el concepto de __opcionales__, que recordemos, es un tipo de datos especial de Swift que pueden representar no solo un valor, sino también *la ausencia* de un valor. El objetivo es entender mejor por qué necesitamos los opcionales y como usarlos de forma segura.

## El tipo `nil`

A veces es útil tener un valor que represente *nada*. Imagina un escenario donde necesitas referirte a la información que identifica a una persona; por ejemplo, almacenamos el nombre, apellidos, fecha y entidad de nacimiento, clave de elector. Obvio que el nombre, apellidos y datos de nacimiento todos tenemos, pero si alguien no está inscrito en el Padrón Electoral, tenemos que hacer algo para manejar la ausencia de la clave de elector.

Si no supiéramos nada acerca de los *opcionales*, así es como podríamos representar los datos de la persona:

```swift
var nombre = "Javier"
var paterno = "Sanchez"
var clave = "ABECID11223344H555"
```

Pero imagina que estás registrando datos en una escuela donde algunos estudiantes no tienen edad para obtener su credencial para votar. Entonces sería bueno poder usar algo que indique la ausencia de clave de elector. 

¿Podríamos usar una cadena vacía? Si, *si podríamos*, pero los **opcionales** son una mejor opción. En seguida veremos porque.

### Valores centinelas

Un valor válido que representa una condición especial, por ejemplo la ausencia de datos, se conoce como **valor centinela**. Eso sería la cadena vacía en el ejemplo anterior.

Let’s look at another example. Say your code requests something from a server, and you use a variable to store any returned error code:

Veamos otro ejemplo. Digamos que tu código muestra datos de un servidor, y usas una variable para almacenar el código de error:

```swift
var errorCode = 0
```

En caso de éxito, representas la ausencia de errores con un vero. Eso significa que `0` es un valor centinela.

Al igual que con la cadena vacía para la clave de elector, esto funciona, pero podría confundir a otros programadores. `0` podría se un código de error válido, o podría serlo en el futuro, si el servidor cambia la forma en que responde. O en todo caso, no podrías asegurar que el servidor regresa algo siempre en esa variable.

En estos dos ejemplo, sería mucho mejor si hubiera un tipo especial que pudiera representar la ausencia de valor. De este modo podríamos expresar de forma explícita cuando existe un valor y cuando no.

La ausencia de un valor recibe el nombre de **`nil`**. Y ahora veremos como lo incorpora Swift, de una forma bastante elegante, por cierto.

Otros lenguajes de programación simplemente usan valores centinelas. Algunos como Objetive-C, tienen el concepto de `nil`, pero es solo un sinónimo de cero. Es solo otro valor centinela.

Swift tiene un nuevo tipo de datos, `optional`, que tiene la posibilidad de contener un valor o ser `nil`. Si estás usando un tipo de datos no opcional con valores obligatorios, como el caso de `nombre` o `apellido`, tienes la seguridad que estos campos siempre tendrán un valor y no necesitarás preocuparte por la existencia de un valor válido. Por otro lado, si usas un tipo opcional, entonces debes manejar el caso `nil`. Esto remueve la ambigüedad de usar valores centinela.

## Los opciones
Los **opcionales** son la solución de Swift al problema de representar *al mismo tiempo* un valor y la ausencia de un valor. Un tipo opcional tiene permitido hacer referencia a un valor o a `nil`

Piensa en un opcional como si fuera una caja: lo mismo puede contener algo que estar vacía. Cuando no contiene un valor, se dice que contiene `nil`. La caja siempre existe; siempre está ahí para ti cuando la abras y mires que contiene.

![Fig. 1 Cajas con Opcionales](https://media.toledano.org/images/2018/001-cajas_opcionales.png)

Por otro lado, una cadena o un entero, no necesitan una caja como esta, porque siempre tienen un valor, como `"hola"` o `42. Recuerda, los tipos no opcionales, garantizan que siempre tienen un valor.

!!!notice "Nota"
    Tal vez hayas escuchado hablar del gato de Schrödinger. Los opcionales son un poco como eso, excepto que no es cuestión de vida o muerte para ningún gato.
    
Para declarar una variable opcional, usamos la siguiente sintaxis:

```swift
var codigoerrork: Int?
```

La única diferencia entre esta y una declaración estándar es el signo de interrogación al final del tipo. En este caso `codigoError` es un _"opcional Entero"_. Esto significa que la variable tiene una caja que puede contener un `Int` o un `nil`.



