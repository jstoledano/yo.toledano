Title: Definiendo relaciones entre modelos con LoopBack    
Date: 2017-03-29 13:28:37
Category: desarrollo
Tags: loopback, restful, mongodb, javascript  
Summary: 

Ya tenemos los dos modelos básicos para nuestra aplicación, `Sitio` y `Puesto`. Estos son necesarios para crear el modelo `Persona` que usa los modelos anterior como claves foráneas.

![Modelo Persona](http://media.toledano.org/images/2017/20170225-persona-model.png)

## La relación belongsTo
Una relación `belongsTo` crea una conexión que puede ser de uno a muchos o de uno a uno con otro modelo. En una relación de _uno a muchos_, cada instancia del modelo declarado **pertenece** a por lo menos una instancia de otro modelo, mientras que el modelo objetivo puede tener muchas instancias del modelo declarado.

Esto es así:

Hay solo tres sitios en el modelo `Sitio`, pero en cada _sitio_ puede haber _x_ cantidad de personas. Por otro lado, cada persona puede estar en uno y solo un sitio. Ahí vemos las dos características de este modelo

# El Modelo Persona
Primero tenemos que crear el modelo, con los campos necesarios usando `lb model` y este el archivo JSON resultante:

```
{
  "name": "Persona",
  "plural": "personas",
  "base": "PersistedModel",
  "idInjection": true,
  "options": {
    "validateUpsert": true
  },
  "properties": {
    "nombre": {
      "type": "string",
      "required": true
    },
    "paterno": {
      "type": "string",
      "required": true
    },
    "materno": {
      "type": "string",
      "required": true
    },
    "sitioId": {
      "type": "string",
      "required": true
    },
    "puestoId": {
      "type": "string",
      "required": true
    }
  },
  "validations": [],
  "relations": {},
  "acls": [],
  "methods": {}
}
```

Las claves foráneas son `sitioId` y `puestoId` y son tipo string porque la base es MongoDB que usa un tipo de objeto especial para el identificador, que al final es una cadena de texto.

## Definiendo las relaciones
Ahora vamos a definir la relación entre los modelos. Una vez más, vamos a usar el comando `lb` pero en esta ocasión, usaremos el subcomando `relation`.

```
> $ lb relation
? Select the model to create the relationship from: Persona
? Relation type: belongs to
? Choose a model to create a relationship with: sitio
? Enter the property name for the relation: sitio
? Optionally enter a custom foreign key: sitioId
```

Y para puesto, hago lo mismo.

```
> $ lb relation
? Select the model to create the relationship from: Persona
? Relation type: belongs to
? Choose a model to create a relationship with: puesto
? Enter the property name for the relation: puesto
? Optionally enter a custom foreign key: puestoId
```

Especificar la clave foránea es opcional, espero haberlo hecho bien.

Esto hace que la definición del modelo `Persona` se actualice, en la parte de `relations` que se ve así:

```
…
  "relations": {
    "sitio": {
      "type": "belongsTo",
      "model": "sitio",
      "foreignKey": "sitioId"
    },
    "puesto": {
      "type": "belongsTo",
      "model": "puesto",
      "foreignKey": "puestoId"
    }
  },
…
```

Vamos a ver como funcionan estas relaciones, agregando documento a nuestro modelo `Persona`.

```
{
  "nombre": "Fulano",
  "paterno": "de Tal",
  "materno": "x",
  "sitioId": "58a920b0bc35e1c8528e3747",
  "puestoId": "58b1fcbad2eb667a368cf76f",
}
```

Ahí podemos ver los identificadores de `sitioId` y de `puestoId` que corresponden a `Junta Local` y `Vocal del RFE`.

Esta es la respuesta del servidor, donde ya tenemos el `id` para esta `Persona`:

```
{
  "nombre": "Fulano",
  "paterno": "de Tal",
  "materno": "x",
  "sitioId": "58a920b0bc35e1c8528e3747",
  "puestoId": "58b1fcbad2eb667a368cf76f",
  "id": "58b1fd97d2eb667a368cf771"
}
```

Ahora podemos consultar las relaciones usando una URI de este tipo:

    http://localhost:3000/api/personas/58b1fd97d2eb667a368cf771/puesto

Y esta es la respuesta

```
> $ http :3000/api/personas/58b1fd97d2eb667a368cf771/puesto                                              
HTTP/1.1 200 OK
Access-Control-Allow-Credentials: true
Connection: keep-alive
Content-Length: 97
Content-Type: application/json; charset=utf-8
Date: Sat, 25 Feb 2017 22:00:46 GMT
ETag: W/"61-paFiafEU38WONZrzm6856g"
Vary: Origin, Accept-Encoding
X-Content-Type-Options: nosniff
X-Download-Options: noopen
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block

{
    "clave": "VRL",
    "id": "58b1fcbad2eb667a368cf76f",
    "orden": 3,
    "puesto": "Vocal del RFE de Junta Local"
}
```

Y ese es el comportamiento esperado.

Ahora si, tenemos todo lo necesario en el backend para tener funcionando una aplicación completa. La aplicación _”Base capINE”_ inicia con el catálogo de sitios, de puestos y de funcionarios. 

Vamos a crear la aplicación ahora en el front end.


[1]: https://strongloop.com/strongblog/defining-and-mapping-data-relations-with-loopback-connected-models/