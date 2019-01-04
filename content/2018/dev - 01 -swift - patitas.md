Title: Cómo funciona Swift    
Date: 2018-05-05 21:28:39
Category: desarrollo
Tags: swift, server-side, vapor 
Summary: Creamos un proyecto completo en Vapor, un framework de Swift para crear aplicaciones web, microservicios y APIs.

## El proyecto Patitas
{{TOC}}

Nada mejor para aprender a usar **Vapor**, el *framework* de Swift del lado del servidor[^1], que creando sitios y APIs. En este primer proyecto vamos a crear un sitio muy simple para una veterinaria llamada *”Patitas”*.

[^1]: Server-side Swift

Para este proyecto suponemos conocimientos en el uso de HTML, CSS y en [Bootstrap](https://getbootstrap.com). Vamos a configurar nuestro proyecto con la caja de herramientas de Vapor, aprenderemos a crear rutas llegar a las diferentes partes de nuestro sitio y a separar el código de la presentación.

Vamos a comparar lo que hacemos en Vapor con lo que se hace con Django para comprender los conceptos y encontrar las similitudes y las diferencias entre los frameworks.

En la medida de lo posible, el proyecto usará herramientas que puedan usarse tanto en Ubuntu como en Mac, por lo que procuraremos indicar las alternativas para Linux[^2]

[^2]: Es que Xcode facilita enormemente el desarrollo con Swift.

Por último, si no tienes instalado Swift o Vapor, puedes seguir la guía en la [documentación](https://vapor.codes) oficial.

## Configuración del proyecto
Vamos a crear un directorio llamado `patitas` que va a contener nuestro proyecto. Así que en una terminal, nos ubicamos en la carpeta de proyectos y ahí ejecutamos el comando `vapor`.

> El comando `vapor` es el equivalente a `django-admin.py` de Django, aunque también tiene algunas cosas de `manage.py`, o sea que es una mezcla de los dos.

Para crear nuestro proyecto usaremos los siguientes comandos.

```bash
$ vapor new patitas --template=jstoledano/vapor-base
$ cd patitas
```

Lo que va a pasar es que se va a clonar un repositorio que es una plantilla para un proyecto mínimo, sin adornos y sin código superfluo que nos servirá para iniciar sin distracciones.

> A diferencia de Python, Swift es un lenguaje **compilado**, por lo que debemos construir el servidor antes de ejecutarlo. La primera ejecución consiste en descargar todos los paquetes que usa el servidor, algo equivalente al `pip -r requirements.txt` que hacemos en Django y Python.

Para ver como funciona inicialmente Vapor, vamos a ejecutar este comando:

```sh
$ vapor build
No .build folder, fetch may take a while...
Fetching Dependencies [Done]
Building Project [Done]
```

Esta instrucción descarga todas las dependencias que usa nuestro programa, incluyendo el propio código de Vapor. A continuación vamos a ejecutar el servidor con el siguiente programa.

```sh
$ vapor run
```

> Como podemos ver, la caja de herramientas de Vapor, es una mezcla del creador de proyectos de Django, del instalador de paquetes de Python `php` y del gestor del proyecto de Django `manga.py`, todo en uno.

Si todo sale bien, veremos la siguiente salida:

```sh
Running patitas ...
[ INFO ] Migrating 'sqlite' database (FluentProvider.swift:28)
[ INFO ] Preparing migration 'Todo' (MigrationContainer.swift:50)
[ INFO ] Migrations complete (FluentProvider.swift:32)
Running default command: .build/debug/Run serve
Server starting on http://localhost:8080
```

El servidor está ya escuchando solicitudes y esta listo para responder a las solicitudes que hagamos. Para terminar el servidor, tenemos que presionar <kbd>Ctrl</kbd> + <kbd>C</kbd>.

## Radriografía de Packages.swift
Lo que hace funcionar la caja de herramientas de Vapor es el Gestor de Paquetes de Swift. Es un programa similar al `pip` de Python o al `npm` de Node aunque menos desarrollado. 

Un paquete en Swift es una aplicación, en el caso de *”patitas”*, ese es nuestro paquete y el gestor de paquetes de Swift es el responsable de compilar, probar y, muy importante, mantener las dependencias obligatorias, es decir aquellos paquetes de terceros que necesitamos para funcione nuestro programa. Estas dependencias se especifican como repositorios remotos de Git y generalmente tienen su propio conjunto de dependencias, todas manejadas con el Gestor de Paquetes.

Nuestro paquete se describe enteramente dentro del archivo `Package.swift` que es, de hecho, código Swift. Si abrimos el archivo de nuestra aplicación veremos lo siguiente:

```swift
// swift-tools-version:4.0
import PackageDescription

let package = Package(
    name: "VaporApp",
    dependencies: [
        // 💧 A server-side Swift web framework.
        .package(url: "https://github.com/vapor/vapor.git", from: "3.0.0"),

        // 🔵 Swift ORM (queries, models, relations, etc) built on SQLite 3.
        .package(url: "https://github.com/vapor/fluent-sqlite.git", from: "3.0.0-rc.2")
    ],
    targets: [
        .target(name: "App", dependencies: ["FluentSQLite", "Vapor"]),
        .target(name: "Run", dependencies: ["App"]),
        .testTarget(name: "AppTests", dependencies: ["App"])
    ]
)
```

Hay que estar pendientes de la dependencia de **Vapor 3**. El framework está todavía en una etapa de desarrollo muy activo, por ejemplo el paquete `fluente-sqlute` apunta a la *tag* `rc-2.2` que significa *Candidato a Liberar 2.2*, es decir, esta versión es la que podría convertirse en la versión oficial si se libera, y esto puede ocurrir cuando todos los *bugs* queden arreglados. Pero una versiȯn `rc` es *casi* idéntica a la liberada y no deberíamos tener problemas.

Por otro lado, uno de los problemas del Gestor de Paquetes de Swift es que no tiene una forma ƒácil de agregar o modificar dependencias; literalmente tenemos que editar el código fuente del archivo `Package.swift` para añadir lo que necesitemos.

Para nuestro proyecto vamos a necesitar una segunda dependencia: el framework **Leaf**. Este es el motor de plantillas de Vapor, que permite desplegar de forma muy eficiente el código HTML.

> Pero como les decía, agregar dependencias no es algo sencillo, por ejemplo, cuando el nombre del paquete y del repositorio Git no coinciden.

Primero debemos agregar la siguiente línea a las dependencias:

```swift
// 🍃 Leaf framework, el motor de plantillas de Vapor
.package(url: "https://github.com/vapor/leaf.git", from: "3.0.0-rc.2.2")
```

Con esto le decimos al gestor de paquetes que debe descargar el código del repositorio de **Leaf** en Github.

Ahora, en apartado `App` de los `targets`, indicamos que `Leaf` es una de nuestras dependencias. Al final, nuestro archivo queda así:

```swift
import PackageDescription

let package = Package(
  name: "appName",
  dependencies: [
    .package(url: "https://github.com/vapor/vapor.git", from: "3.0.0"),
    .package(url: "https://github.com/vapor/leaf.git", from: "3.0.0-rc.2.2")
  ],
  targets: [
    .target(name: "App", dependencies: ["Vapor", "Leaf"]),
    .target(name: "Run", dependencies: ["App"]),
    .testTarget(name: "AppTests", dependencies: ["App"])
  ]
)
```

Ahora debemos guardar nuestros cambios y escribir `vapor update` para que se descargue el repositorio **Leaf**.

## Estructura del proyecto
Vamos a revisar rápidamente como está conformado nuestro proyecto.
