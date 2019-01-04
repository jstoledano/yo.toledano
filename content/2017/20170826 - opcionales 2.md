Title: Opcionales en Swift II   
Date: 2017-08-26 20:17:57
Category: desarrollo
Tags: swift, opcionales, 
Summary: En este artículo veremos más a fondo el concepto de opciones, un tipo de datos especial de Swift, que representa la ausencia de un valor.

## El valor `nil`
Algunas veces es útil tener un valor que no represente nada. Por ejemplo, cuando necesitamos hacer referencia a un trámite, tiene número de folio y fecha de trámite, pero no necesariamente tiene datos de credencial recibida, así que necesitamos manejar esta ausencia de información.

Si no supiéramos de los opcionales, así se vería un trámite, folio, fecha de trámite y fecha de disponible:

```swift
var folio = "1729060401234"
var fecha_tramite = "2017-08-15"
var fecha_disponible = "2017-08-25"
```

Pero, ¿qué pasa si no hemos recibido la credencial? Es aquí cuando entendemos lo útil de referirnos a la ausencia de un valor. Obvio que podemos usar una cadena vacía, pero los opcionales son una mejor opción, veamos por qué.

### Valores centinelas
Un valor válido que representa una condición especial tal como la ausencia de un valor es llamado **valor centinela**. Eso es lo que sería `fecha_disponible` en nuestro ejemplo anterior.

Veamos otro ejemplo. Digamos que ejecutamos alguna solicitud de un servidor, y usamos una variable para almacenar cualquier código de error que obtengamos.

```swift
var errorCode = 0
```

En caso de éxito, usaríamos el cero como la ausencia de error. Esto es que el `0` es el valor centinela.

Al igual que la fecha vacía en el caso de `fecha_disponible`, esto funciona, pero es una fuente potencia de confusión para el programador. `0` puede ser un código de error válido -- o puede serlo en el futuro, si el servidor cambia la forma en la que responde. O sea que no podemos asegurar que el servidor no regresó un código de error.

