Fichas de proceso con Python
============================

:date: 2015-08-21 21:08:47 GMT-5
:tags: python, procesos, iso9001
:category: Desarrollo
:slug: fichas-de-proceso-con-python
:cover: https://media.toledano.org/images/dev/ficha-procesos.jpg
:summary: Cómo crear fichas de proceso rápidas y fáciles usando yaml y python.
:status: draft

Un proceso es un conjunto de actividades relacionadas *ordenadas de forma lógica* que transforman elementos de entrada en resultados.

La norma ISO 9001 nos pide describir los procesos requeridos por el sistema, su secuencia y sus interacciones, precisamente porque esta norma promueve el enfoque basado en procesos, que entre otras cosas nos ayuda a tener un control continuo sobre los vículos entre los procesos individuales, así como su combinación con otros procesos de la organización.

Enfoque de procesos
-------------------

Es por eso que dentro de los requisitos generales, la norma establece que se deben determinar los procesos necesarios para el sistema de gestión de la calidad, su secuencia e interacción, los métodos de control, los recursos para apoyar su operación, el seguimiento y la medición de los mismos y la toma de acciones para corregir su desempeño o sus resultados.

La organización donde trabajo ha decido crear un manual de operación que contiene todos los procesos que utilizamos, y para hacerlo más fácil programe un pequeño guión (o *script*) que haga esta rápida y eficientemente.

La plantilla YAML
-----------------

El formato **YAML** es un formato para transportar datos de forma legible por las personas. El nombre es un acrónimo que significa *"YAML Ain't Another Markup Language"* que significa *YAML no es otro lenguaje de marcado*.

Es un lenguaje de marcado bastante ligero, no tiene etiquetas de cierre y una estructura estricta. Permite crear listas y diccionarios para formar algo así como *árboles* de datos agrupados en *bloques*. Miren un ejemplo tomado de la wikipedia:

.. code-block:: yaml

    --- # Películas favoritas, formato de bloque
    - Casablanca
    - Viridiana
    - Psicosis
    --- # Lista de la compra, formato en línea
    [leche, pan, huevos]

Estos archivos pueden ser procesados por muchos lenguajes y producir documentos en una gran variedad de formatos. En nuestro caso, vamos a utilizar Python y producir una salida en HTML.

La plantilla YAML
-----------------

Esta es la plantilla YAML usada para describir los procesos.
