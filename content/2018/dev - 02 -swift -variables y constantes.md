Title:  Variables y constantes en Swift   
Date: 2018-05-05 19:33:53
Category: desarrollo
Tags:  swift, server-side
Summary: 

Cuando programamos algo, siempre llega el momento en que debemos almacenar algún tipo de datos y en **Swift** hay dos formas de hacerlo: con _variables_ y con _constantes_. Una variable es un dato almacenado que puede cambiar cuando sea necesario, por otro lado, las constantes son datos que nunca van a cambiar. 

Aunque puede parecer exagerado tener estas opciones (o sea, para que queremos tener un _“variable”_ si nunca a cambiar.  Una de las ventajas de separar es que **Xcode** nos puede ayudar cuando cometemos errores. Si decimos, por ejemplo _“esta fecha nunca va a cambiar, porque es un dato del pasado“_, luego 10 líneas mas abajo tratamos de cambiarla, Xcode se negará a compilar nuestra app.

Las constantes son importantes porque le permiten a Xcode tomar decisiones sobre como construir nuestra app. Si sabemos que un valor nunca va a cambiar, puede aplicar optimizaciones para que nuestro código funcione más rápido.

En Swift, podemos crear variables usando la palabra clave `var`, de la siguiente manera:

```swift
var nombre = “Javier Sanchez”
```

Si iniciamos una sesión en el intérprete interactivo de Swift podemos ver que es lo que pasa cuando escribimos ese comando.

```bash
Welcome to Apple Swift version 4.1 (swiftlang-902.0.48 clang-902.0.39.1). Type :help for assistance.
  1> var nombre = "Javier Sanchez"
nombre: String = "Javier Sanchez"
```

Y como es una variable, podemos cambiar cuando se nos antoje, con una condición: **solo podemos usar `var` una sola vez al crear la variable**. Veamos.

```swift
  1> var nombre = "Bruce Wayne"
nombre: String = "Bruce Wayne"
  2> print(nombre)
Bruce Wayne
  3> nombre = "Batman"
  4> print(nombre)
Batman
```

En la primera línea creamos la variable y le damos el valor inicial, en la segunda línea actualizamos la variable **`nombre`** para darle un nuevo valor, `"Batman"`.  Y podemos ver la salida que produce.

