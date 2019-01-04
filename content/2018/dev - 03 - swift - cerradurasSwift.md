Title: Cerraduras Swift    
Date: 2018-06-03 21:28:39
Category: desarrollo
Tags: swift, server-side, vapor 
Summary: 

# Cerraduras
Las cerraduras o _closures_ son bloques de funcionalidas autocontenidos que se pueden para y usar en nuestro código. Las _closures_ en __Swift__ son similares a los bloques en __C__ o en __Objective-C__ y a las _lambdas_ en otros lenguajes.

Las _closures_ pueden capturar y almacenar referencias a cualquier constante y variable del contexto en el que se definen. Esto se conoce como _”el cierre”_ de esas constantes y variables. Swift se encarga de gestionar toda la memoria de las capturas por nosotros.

> ### Nota
No te preocupes si no entiendes todavía el concepto de _**captura**_ lo veremos en un momento mas.

Las funciones globales y anidadas son, de hecho, casos especiales de _cerraduras_. Las _closures_ toman una de las sguientes tres formas:

- Las funciones globales son *cerraduras* que tienen un nombre y no capturan ningún valor.
- Las funcionens anidadas son cerraduras con nombre que capturan valores de la función que las encierra.
- Las *expresiones de cerradura* son cerraduras escritas en una sintaxis ligera que pueden capturar valores del contexto que las rodean.

Las *expresiones de cerradura* en Swift tienen un estilo limpio y claro con optimizaciones que fomentan una sintaxis breve y sin complicaciones en escenarios comunes. Entre estas optimizaciones se encuentran:

- Inferir parámetros y el tipo de los valores devueltos desde el contexto.
- Retornos implícitos en cerraduras de una sola expresión.
- Nombres de argumentos abreviados.
- Sintaxis de cierre finales.

## Expresiones de Cerraduras
Las funciones anidadas son una forma conveniente de definir bloques auto-contenidos de código como parte de funciones mas grandes. Sin embargo, a veces es útil escribir versiones mas cortas de las funciones sin nombre o una declaración completa. Esto es cierto cuando trabajamos con funciones o métodos que tiene funciones como argumentos.

Las expresiones de cierre son una forma de escribir cierres en línea con una sintaxis breve y enfocada. Las expresiones de cierre proporcionan varias optimizaciones de sintaxis para escribir *cerraduras* en una forma abreviada sin pérdida de claridad o intención. Los ejemplos de expresiones de cierre a continuación ilustran estas optimizaciones refinando un solo ejemplo del método `sorted(by:)` en varias iteraciones, cada una de las cuales expresa la misma funcionalidad de una manera más concisa.

### El método `Sorted`
La biblioteca estándar de Swift proporciona un método llamado `sorted(by :)`, que ordena una matriz de valores de un tipo conocido, en función del resultado de un *cerradura* para clasificación que nosotros proporcionamos. Una vez que completa el proceso de clasificación, el método `sorted(by:)` devuelve una nueva matriz del mismo tipo y tamaño que la anterior, con sus elementos ordenados en el orden correcto. La matriz original no se modifica.

Los siguientes ejemplos de expresiones de cerradura utilizan el método `sorted(by:)` para ordenar una matriz de valores de cadenas de texto en orden alfabético inverso. Aquí está la matriz inicial para ordenar:

```swift
let nombres: [String] = ["Chris", "Alex", "Ewa", "Barry", "Daniella"]
```

El método `sorted(by:)` acepta una *cerradura* que toma dos argumentos del mismo tipo que el contenido de la matriz y devuelve un valor `Bool` para indicar si el primer valor debería aparecer antes o después del segundo valor una vez que se hayan ordenado los valores. La *cerradura* de clasificación debe ser verdadera si el primer valor debe aparecer antes del segundo valor y, en caso contrario, falso.

Este ejemplo está ordenando una matriz de valores de cadena, por lo que el cierre de clasificación debe ser una función de tipo `(cadena, cadena) -> Bool`.

Una forma de proporcionar esta _cerradura de clasificación_ es escribir una función normal del tipo correcto y pasarla como argumento al método `sorted(by:)`:

```swift
func descendente(_ s1: String, _ s2: String) -> Bool {
    return s1 > s2
}

var nombresDescendentes = nombres.sorted(by: descendente)
// nombresDescendentes es igual a ["Ewa", "Daniella", "Chris", "Barry", "Alex"]
```

Si la primera cadena (`s1`) es mayor que la segunda cadena (`s2`), la función `descendente(_:_:)` devolverá `true`, lo que indica que `s1` debe aparecer antes de `s2` en la matriz ordenada. Para los caracteres en cadenas, _”mayor que”_ significa __*”aparece más adelante en el alfabeto que”*__. Esto significa que la letra `"B"` es _”mayor que”_ la letra `"A"`, y la cadena `"Tom"` es mayor que la cadena `"Tim"`. Esto da un orden alfabético inverso, con `"Barry"` colocado antes de `"Alex"`, y así sucesivamente.

Sin embargo, esta es una forma bastante larga de escribir lo que es, esencialmente, una función de expresión única (`a > b`). En este ejemplo, sería preferible escribir la cerradura de clasificación en línea, usando la sintaxis de expresión de cerradura.

### Sintaxis de Cerradura
La sintaxis de expresión de cerradura tiene la siguiente forma general:

```swift
{ (parámetros) -> tipo devuelto in
    declaraciones
}
```

Los _`parámetros`_ en la sintaxis de la expresión de cerradura pueden ser parámetros de entrada y salida, pero __no pueden tener un valor predeterminado__. Podemos usar parámetros __variadic__ si se nombra dicho parámetro _variadic_. Las tuplas también se pueden usar como tipos de parámetros y tipos de devolución.

El siguiente ejemplo muestra una versión de expresión de cerradura de la función `descendente(_:_:)` que vimos anteriormente:

```swift
nombresDescendentes = nombres.sorted(by: { (s1: String, s2: String) -> Bool in
    return s1 > s2
})
```

Hay que observar que la declaración de parámetros y los tipos devueltos para esta cerradura en línea son idénticos a la declaración de la función `backward(_:_:)`. En ambos casos, se escriben como `(s1: String, s2: String) -> Bool`. Sin embargo, para la cerradura en línea, los parámetros y el tipo devuelto están escritos _dentro_ de los corchetes y no fuera.

El inicio del cuerpo de la cerradura se marca con la palabra clave **`in`**. Esta palabra clave indica que ha terminado la definición de los parámetros y el tipo devuelto de la cerradura ya terminó y empezará el cuerpo de la cerradura.

Como el cuerpo de la cerradura es tan corta, se puede escribir en una sola línea:

```swift
nombresDescendentes = nombres.sorted(by: {(s1: String, s2: String) -> Bool in return s1 > s2})
```

Esto nos demuestra que, en general, la llamada al método `sorted(by:)` es siempre el mismo. Un par de paréntesis envuelven los argumentos están en un cerradura en línea.

### Infiriendo el tipo del contexto
Debido a que la cerradura para el ordenamiento se pasa como un argumento a un método, Swift puede inferir el tipo de sus parámetros en el tipo de sus parámetros y de los valores de regreso. El método `sorted(by:)` se llama sobre un arreglo de cadenas, por lo que será una función tipo `(String, String) -> Bool`. Esto significa que los tipos `(String, String)` y `Bool` no necesitan estar presentes como parte de la definición de la cerradura.