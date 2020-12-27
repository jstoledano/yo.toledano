Title: Llenado de formularios HTML con Python
Date: 2013/11/18 19:20
Category: Desarrollo 
Tags: python, librerias 
Slug: llenado-de-formularios-html-con-python
Summary: 

El problema que trato de resolver es el siguiente:

> Quiero verficar en una página web que se genera automáticamente si aparece cierta cadena de texto, si no aparece ejecutar ciertas acciones que hacen que la cadena de búsqueda aparezca.

Para poner un ejemplo, según leo en **Enchilame** que es posible hacer trampa en **blogsmexico**[^1] y ponen un ejemplo que usa `wget`. Es muy fácil, pero como aquí se trata de aprender haremos esto mismo en un guión de Python.

_Debo aclarar que no estoy de acuerdo con este tipo de prácticas, pero es evidente que algunos blogueros la usan de manera constante, apareciendo en la portada de manera injusta._

[^1]: Ambos sitios, enchílame y blogsmexico ya murieron por la patria.

El problema es de blogsmexico y está en sus manos la solución (poniendo _captchas_, por ejemplo) y en tanto no lo arreglen, usuarios sin escrúpulos seguirán explotándolo. Aquí esta la solución para combatir estas malas prácticas: _competir en igualdad de circunstancias_.

Y bueno, también quiero probar mi generador de código coloreado basado en Geshi:

```python
#!/usr/bin/env python
#-*- coding: utf-8 -*-
import urllib

bmexico = 'http://blogsmexico.com'
titulo = 'Yo, Toledano'
url="http://yo.toledano.org/"
ping ="http://www.blogsmexico.com/hacerping.php?"

data = urllib.urlencode({"titulo" : titulo, "url" : url})
f = urllib.urlopen(bmexico).read().find('toledano')
if f > 0:
    print 'Estás en la portada'
else:
f = urllib.urlopen(ping+data)
```

El plugin se llama **Transcode**, está escrito en Perl y usa PHP para comunicarse con Geshi, fue escrito por Ben Artin de Periodic Kigdom.

Para usarlo lo único que tenemos que hacer es colocar el filtro `transcode="1"` a la marca `MTEntryBody` en cada uno de las plantillas en las que aparezca este código. Y al colocar el código usando las marcas `<pre>` y `<code>` agregar a continuación `transcode-language:` y el nombre del lenguaje, algo asi:

```html
<pre><code>transcode-language: python
print 'Hola Mundo'

</pre></code>
```

<div data-alert class="alert-box">Esta entrada apareció orignalmente en el blog «Yo, Toledano» el 4 de septiembre de 2006. Su contenido podría estar desactualizado.</div>
