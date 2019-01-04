Title: Cómo encontrar archivos con Python
Date: 2014/01/05 04:03
Category: Desarrollo 
Tags: tools, python, scripts 
Slug: como-encontrar-archivos-con-python
Author: Javier Sanchez Toledano
Summary: 

Este es el problema: Tengo muchos archivos de karaoke que vienen en pares de archivos `mp3` y `cdg`, el primero tiene la música y el segundo tiene las letras de las canciones. Pero son varios cientos de canciones distribuidas en muchos directorios.

Lo que yo quería era crear una lista de los archivos cdg para poder usarla con el programa de *karaokes*, por lo que use `fnmatch` que hace esto mucho más fácil, en solo una línea.

Primero vamos a importar dos módulos necesarios para hacer esta búsqueda, el primero es `os` que contiene el generador `walk` para recorrer los directorios y el segundo es `fnmatch` para encontrar coincidencias.

    import os
    import fnmatch

Y vamos a crear una lista donde almacenaremos todas las coincidencias.

    coincide=[]

A continuación vamos a recorrer el directorio en cuestión con la función `os.walk` para tener los nombres de los archivos. Cuando un archivo coincida con nuestra búsqueda, colocamos la ruta completa en la lista `coincide`. Usamos la función `fnmatch.filter` que toma dos argumentos, el primero es el archivo y el segundo es la coincidencia que buscamos.

    for root, dirnames, filenames in os.walk('\Karaoke'):
      for filename in fnmatch.filter(filenames, '*.cdg'):
          coincide.append(os.path.join(root, filename))
      
Cuando el filtro encuentra una coincidencia se ejecuta la última instrucción que es agregar a la lista el archivo con la ruta completa.

Esto imprime los resultados en la pantalla, pero unas líneas más permite guardar la lista en un archivo:

    i = 1
    f = open ('granlista.txt', 'w')
    for m in matches:
        f.write('F%s=..\..\..%s\n' % (i, m))
        i+=1
        
Y con eso tenemos una lista de archivos con la terminación deseada.
