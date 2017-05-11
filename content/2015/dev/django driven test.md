Title: Pruebas con Django  
Date: 2015-04-24 9:33:07  
Category: Desarrollo  
Tags:  django, test  
Author: Javier Sanchez Toledano  
Summary: Como desarrollar un conjunto de pruebas con Django.



Las pruebas automáticas son una herramienta muy poderosa para eliminar errores de programación, utilizada en los entornos de desarrollo web modernos. Puedes usar una colección de pruebas, -- una _test suite_ -- para corregir o prevenir problemas.

- Cuando programas algo por primera vez, puedes usar las pruebas para validar que el código funcione como se espera.
- Cuando estás reescribiendo o modificando programas ya hechos, puedes usar una batería de pruebas para asegurar que los cambios que haz realizado no afecten a tu aplicación de formas inesperadas.

Crear una batería de pruebas para una aplicación web es una tarea compleja, porque una aplicación de este tipo está hecha de varias capas de lógica, desde el manejo de solicitudes a nivel HTTP, validación y procesamiento de formularios, hasta la presentación de las plantillas. Con el marco de trabajo de ejecución de pruebas de Django y sus utilerías asociadas, puedes simular solicitudes, insertar datos de prueba, inspeccionar la salida de tu aplicación y en general verificar que tu código funcione como se espera.

Lo mejor de todo es que es muy fácil.

La mejor práctica a la hora de escribir pruebas en Django es usar el módulo `unittest` de la biblioteca estándar de Python, que veremos con todo detalle en el siguiente artículo de esta serie.

También puedes usar otros 

You can also use any other Python test framework; Django provides an API and tools for that kind of integration. They are described in the Using different testing frameworks section of Advanced testing topics.