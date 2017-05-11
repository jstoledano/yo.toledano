Title: Angular para Djangonautas    
Date: 2016-10-22 21:21:31
Category: desarrollo
Tags: angular, django 
Series: Angular para Djangonautas
Summary: 

La verdad es que no encontré mucha información que me ayudará a comprender como funcionaba __AngularJS__. Tengo poca experiencia en JavaScript, así que cometí el error de evitar usarlo.

### Qué es AngularJS
Es un marco de trabajo, como Django, pero para lo que se llama el _frontend_, es decir, para la parte que interactúa con el cliente. Está escrito en JavaScript y permite modificar la página web, el DOM para presentar y manipular información de forma muy eficiente.

La forma de usar las funciones de Angular es idéntica a la de Django: `{{ }}` por lo tanto hacen cortocircuito. Mi primera opción fue cambiar estos delimitadores en AngularJS para poder usar las plantillas de Django, pero después me di cuenta que **es innecesario**. AngularJS, desde el punto de vista de Django, se sirve como archivos estáticos.

### Un proyecto aparte
Entender que AngularJS se debe tratar como estáticos es toral para un mejor manejo del _framework_.

De hecho, es incluso mejor manejar los proyectos por separado: por un lado la aplicación del lado de servidor con Django, es decir el __backend__ y por otro la aplicación del lado del cliente, o sea, el __frontend__.

Una de las razones mas importantes para separar el _backend_ de Django en un proyecto aparte es que este __debe ser agnóstico__, es decir, no debe estar programado para un _frontend_ específico, sino para cualquiera.

Esto es así: Django ofrece una API, una interface programática de la aplicación para que cualquiera, literalmente __cualquier__   _frontend_ pueda interactuar con ella, _consumirla_. 

Acostumbrado  como estoy a usar siempre las plantillas de Django, este paradigma fue un cambio total.

### La API de Django
Una interface programática de aplicaciones o API por sus siglas en inglés es como el menú de los restaurantes, expone a los clientes los productos que se pueden consumir. No te explica como los hacen, solo te muestran el resultado final. 

Cuando escribimos una API en Django, debemos saber __que estamos ofreciendo__ antes de poder servirlo. Generalmente son operaciones comunes (como en los restaurantes, la mayoría tienen un menú): las operaciones que llaman CRUD por sus siglas en inglés Create (_crear_), Read (_leer_), Update (_actualizar_) y Delete (_borrar_).

Para generar API, el protocolo más común es [REST](https://es.wikipedia.org/wiki/Representational_State_Transfer), un protocolo para realizar operaciones bien definidas sobre datos __sin estado__, donde cada mensaje tiene toda la información necesaria, incluyendo autenticación y autorización.

Para Django, el paquete mas común para crear API REST es [Django REST Framework](http://www.django-rest-framework.org) que de forma realmente muy simple permite crear APIs con todos los verbos que usa una API: GET, POST, PUT, DELETE, etc.

Esta API va en el servidor _backend_, por lo que en el _frontend_ va otro servidor. De ahí que tener dos proyectos independientes tenga mucho sentido.

### AngularJS y Django
AngularJS es un framework a toda regla, que funciona del lado del cliente. Junto a una aplicación de AngularJS, las plantillas de Django son verdaderamente tontas, y así deben de quedarse. Pero ¿para que seguir hablando de las plantillas de Django si ya no las volveremos a usar?

AngularJS permite traer los datos que sirve la API[^1] de Django y presentarlos de forma dinámica, con características que son al mismo tiempo simples pero muy potentes.

Pero funcionan de forma independiente de Django. Así como Django puede crear una API sin importar quién la consuma, así también AngularJS puede consumir APIs sin importar quien la sirva. Un argumento más para separar los proyectos.

En esta serie, intentaré registrar mis intentos por crear una aplicación con AngularJS y Django. Estén pendientes.

[^1]: En el argot se dice _"consumir"_.
