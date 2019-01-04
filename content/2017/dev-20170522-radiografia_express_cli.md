Title: Radiografía del proyecto Express
Date: 2017-05-22 19:11:01
Category: desarrollo
Tags: express, es6, node
Summary: Es muy importante conocer como funciona Express.js en su expresión más simple. En este artículo analizamos línea por línea cada archivo del proyecto generado por Express.


Después de haber generado el proyecto y la refactorización
para usar la sintaxis de ES6 y Babel, vamos a revisar los
archivos que componen el proyecto y tratar de comprender el
papel que cada uno de ellos juega en el proyecto.

## El archivo `bin/server.js`

Este es el archivo que arranca el servidor cuando lo
llamamos desde el script de arranque. Debido a las funciones
de apoyo que utiliza, el arranque del servidor aparece al
final.

    :::javascript
    const port = normalizarPuerto(process.env.PORT || '3000')
    app.set('port', port)
    const server = http.createServer(app)
    server.listen(port)
    server.on('error', siHayError)
    server.on('listening', alEscuchar)

`const port = normalizarPuerto(process.env.PORT || '3000')`
La primera línea crea la constante `port`. El valor lo toma
de la variable de entorno `PORT` si existe, o lo establece
como el 3000 por omisión.

`app.set('port', port)`
La segunda línea usa el método [`.set()`][1] para almacenar
el valor del puerto en la tabla de propiedades de `app`, el
problema es que no veo que se use este valor en ningún lado.
No hay ningún `app.get('port')`. Pero bueno, después puedo
eliminar la constante y usar solo el _getter_.

`const server = http.createServer(app)`
Luego creamos un servidor, usando el método
`http.createServer(app)`. Este método pertenece al núcleo de
__Node.js__ y recibe como parámetro opcional un _escuchador
de solicitudes_ (`requestListener`) que automáticamente se
agrega al _request_ o solicitud.

Este método devuelve una nueva instancia de
[`http.Server`][2] que colocamos en la constante `server`.

`server.listen(port)`
El método `listen()` pertenece a `http`, pero lleva en la
solicitud la aplicación de __Express.js__. No me queda claro
por qué damos este rodeo, si según la documentación del
método [`app.listen()`][3] podemos usar como un atajo.
Sospecho que tiene que ver con el módulo `Debug`, pero más
adelante veremos como usar solo `app`.

> Ya investigué y resulta que `http` proporciona algunos métodos que
no proporciona `express`. Y dado que __Express.js__ es mucho más que
un servidor HTTP, delega estas funciones al vulgar y corriente
módulo `http`. El creador del servido, explica en un
[caso en GitHub][5] porque no es necesario.

En este momento, es cuando arranca el servidor e inicia el
_Node Event Loop_ o ciclo de eventos de __Node.js__ que es
lo que permite a nuestro proyecto que maneje múltiples
operaciones tras bambalinas. El [_event loop_][4] es un
concepto muy importante que revisaremos a fondo
próximamente.

Una vez que ha arrancado el servidor, activamos dos monitores, uno de ellos para el manejo de errores y otro para monitorear el arranque:

    :::javascript
    server.on('error', siHayError)
    server.on('listening', alEscuchar)

El primer monitor, escucha el evento `'error'` y cuando sucede lanza la función `siHayError` que veremos a continuación:

    :::javascript
    let siHayError = (error) => {
      if (error.syscall !== 'listen') throw error
      let bind = typeof port === 'string' ? `Pipe ${port}` : `Puerto ${port}`
      // manejamos los errores con mensajes amigables
      switch (error.code) {
        case 'EACCES':
          console.error(`${bind} requiere de mayores privilegios`)
          process.exit(1)
          break
        case 'EADDRINUSE':
          console.error(`El ${bind} ya está en uso`)
          process.exit(1)
          break
        default:
          throw error
      }
    }

Veamos como funciona.

    if (error.syscall !== 'listen') throw error 
En la primera línea verifica si el error _no es_ de escucha en cuyo caso, lanza el error al sistema.

    `let bind = typeof port === 'string' ? `Pipe ${port}` : `Puerto ${port}` 
Esta línea verifica si estamos mandado un número de puerto o un control de flujo o _pipe_. Si es un texto, es un _pipe_, sino, es un puerto.

Lo siguiente es un bloque de elección. Si el error es tipo `EACCES` significa que no tenemos permisos para usar ese puerto, por ejemplo el `80`. Si la dirección ya está en uso, el error sería `EADDRINUSE`. De nuevo, este monitor solo busca errores al iniciar el servidor.

Si el error no es alguno de esto, lo lanza sin procesar.

El siguiente monitor nos indica si el servidor está escuchando el puerto indicado.

    :::js
    let alEscuchar = () => {
      let address = server.address()
      let bind = typeof add === 'string' ? `el pipe ${address}` : `el puerto ${address.port}`
      debug(`Escuchando en ${bind}`)
    }

Verifica la dirección y el puerto del objeto que pasa el servidor, igual que la función `bind` del monitor anterior, determina si estamos usando un puerto o un control de flujo.

Estos dos monitores usan la función `debug` que busca que esté presente en las variables de entorno la clave `DEBUG` con el valor `aspases:server`.

## El archivo `app.js`

Este es el archivo del servidor __Express.js__ propiamente dicho. Las primeras líneas sirven para importar los módulos que ocuparemos en el proyecto.

Luego cargamos las rutas y preparamos la aplicación `app`. Configuramos el motor de plantillas. Primero el directorio y luego el tipo específico.

A continuación, cargamos los módulos en la aplicación. El que carga el _favicon_, la bitácora, el analizador de contenido y de _cookies_, el preprocesador de estilos y por último, las rutas.

Una pequeña funciono para capturar las solicitudes de páginas no encontradas. Y otra para los errores 500, que solo se muestra si estamos ejecutando el servidor con la bandera de `development`.

## Los archivos de rutas
Los archivos de rutas no son la gran cosa. El índice llama a la plantilla `index` y le pasa en el contexto la variable `title`.

La ruta `/users` solo imprime un mensaje _dummy_.

## Las plantillas

La plantilla base o `layout.hbs` es una página web mínima, con una variable `{{ title }}` y un bloque `{{{ body }}}`.

La plantilla `index` se dibuja sobre el bloque `body` y solo imprime la variable `title`. La plantilla error hace lo mismo, pero con el mensaje de error.

---
Esto es todo lo que hace el proyecto generado por la CLI de __Express.js__ y refactorizado para convertirlo con Babel en ES6.

Ahora si estamos listos para empezar con algo más serio.

[1]: https://goo.gl/bruiI9
[2]: https://goo.gl/pAC8ub
[3]: https://goo.gl/2emoUq
[4]: https://goo.gl/sznDdk
[5]: https://goo.gl/geB79A
