Title: Extraer audio de un archivo AVI
Date: 2013/11/20 16:57
Category: Desarrollo 
Tags: tools, media, audio 
Slug: extraer-audio-de-un-archivo-avi
Author: Javier Sanchez Toledano
Summary: 

Supongo que sirve para extraer audio de cualquier video, pero yo hice la prueba con un archivo `.avi`. Use la herramienta `mplayer`.

Muy simple todo, solo tengo que escribir en la línea de comandos lo siguiente:

    :::Bash
    mplayer -quiet -vc dummy  -vo null -ao pcm:waveheader:file=salida.wav entrada.avi

Una vez que termina, en realidad muy rápido en mi Pentium III a 1.6Ghz, lo convertimos a `.mp3` usando `lame`:

    lame salida.wav
