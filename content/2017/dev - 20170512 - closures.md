Title: Que son las closures    
Date: 2017-05-12 14:00:00
Category: desarrollo
Tags: javascript, patterns 
Summary: 

La verdad no encontré una buena traducción de __*closure*__. Literalmente, significa _"cierre"_, pero no tiene mucho sentido en el contexto de la programación fun&shy;cional. Es uno de esos conceptos que para comprenderlo hay que verlo o hacerlo.

Para explicarlo de forma simple, una _closure_ es una función interna, es decir, __una función *dentro* de otra función__. Algo asi:

    :::js
    function externa() {
      function interna() {

      }  
    }