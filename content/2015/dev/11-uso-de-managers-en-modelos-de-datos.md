Title: Uso de Managers en Modelos de Datos
Date: 2013/11/19 19:58
Category: Desarrollo 
Tags: patterns, models, managers 
Slug: uso-de-managers-en-modelos-de-datos
Author: Javier Sanchez Toledano
Summary: 

El nuevo indicador mide el tiempo que tarda nuestro producto en fabricarse. La producción implica una serie de pasos que generan un *timestamp*, es decir el registro de la fecha y hora exacta en la que el producto entró en un estado particular. Existen 27 pasos posibles y los controlamos todos.

Nos interesa saber inicialmente saber el tiempo que tarda desde que se recibe el pedido hasta que se pone disponible para el cliente[^1]. Dependiendo del sitio dónde se hace el pedido, pueden ser 14 o 18 días.

También nos interesa el tiempo que tarda el producto desde que se recibe el producto hasta que se autoriza su fabricación. Este lapso depende también del sitio y puede ser de 7 a 10 días.

El primer reto para este indicador, llamado *Disponibilidad* es que la identificación del sitio no está presente en los registros, sino incluída en el índice principal, el número de control. Este número de control esta formado por 13 dígitos, los dos primeros corresponden al año, luego siguen 6 dígitos que corresponden a la identificación del sitio, luego 5 dígitos para un consecutivo por sitio.

El problema es que tenemos que usar funciones de agregado de dominio con filtros, no podemos hacerlo con valores calculados. Por ejemplo, **contar cuántas solicitudes hay en el sitio 121**.

    :::python
    Disponibilidad.objects.filter(fuar[2:6]='121').count()

Aunque la idea es buena, no podemos usar claves en expresiones. La solución puede parecer complicada, pero es bastante elegante y muy pythonica.

## Manejadores de Modelos en Django

Un Manejador o *Manager* es una interface entre las operaciones de consultas de la base de datos y los modelos en Django. De hecho, todos los modelos tienen un manejador en automático llamado `objects`.

Lo que vamos a hacer es crear un Manejador que agregue el campo modulo a nuestro modelo y sobre este manejador hacer las consultas que necesitamos.

    :::python
    class ModuloManager (models.Manager):
        modulo = {'modulo':"SUBSTR(fuar, 3, 6)"}
        def get_query_set(self):
            return super(ModuloManager, self).get_query_set().extra(select={'modulo':"SUBSTR(fuar, 3, 6)"})

Lo que hacemos en este código es modificar las consultas a nuestro modelo para que agreguen este fragmento al SQL que generan:

    :::SQL
    SELECT SUBSTR(fuar, 3, 6) AS modulo

Para activar el manejador debemos agregar estas líneas a la definición de clase de nuestro modelo.

    :::python
    modulos = ModuloManager()
    objects = models.Manager()

Es decir, mantenemos el manejador por default y agregamos el nuestro que adiciona a las consultas el sitio.

### Consultas extra en el ORM de Django

Ya podemos visualizar el sitio, con el nombre de modulo, sin embargo sigue siendo una expresión calculada y no podemos usarla con filtros, pero podemos usar la empresión extra para crear una consulta más específica.

Ahora podemos usar este nuevo campo para hacer filtros en una *view*.

    :::python
    Disponibilidad.modulos.extra(where=['modulo = "290121"'])

[^1]: Nuestro compromiso es tener el producto en un tiempo especificado, pero el cliente puede ir por su pedido cuando quiera.
