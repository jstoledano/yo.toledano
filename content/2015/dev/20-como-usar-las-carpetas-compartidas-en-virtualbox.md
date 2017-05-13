Title: Cómo usar las carpetas compartidas en VirtualBox
Date: 2013/11/22 15:46
Category: Desarrollo 
Tags: tools, virtualbox 
Slug: como-usar-las-carpetas-compartidas-en-virtualbox
Author: Javier Sanchez Toledano
Summary: 

Instalaste tu linux usando VirtualBox, instalaste las «Guest Additions», 
configuraste las carpetas compartidas, pero ¡No las puedes usar! Asi me pasaba 
a mi. Instalé openSUSE en MS Windows 7, instalé las herramientas de huesped 
y configuré unas carpetas compartidas, pero no podía montarlas.

Aquí está la solución, pero parto de la premisa que las adiciones están 
instaladas y que ya has definido la o las carpetas compartidas que vas 
a utilizar. Puedes verificar que tu configuración funciona escribiendo la orden 
de montaje en tu consola.

    sudo mount -o fmask=0133,dmask=0022, -t vboxsf ssh win7

En el ejemplo, yo llamé `ssh` a mi carpeta compartida y `win7` al directorio en 
linux que va a contenerla. Los parámetros que paso indican los permisos que 
tendrán los archivos, ya que al ser una partición de Windows, todos los 
archivos quedan por default como ejecutables, es necesario este ajuste: `0133` 
en los archivos, le da a estos permisos `644` y en los directorios `0022`, se 
convierte en permisos `0755`. Algo ideal para trabajar con archivos sin 
peligros.

Si funciona, entonces podemos agregar los datos al arranque de openSUSE, ya 
para esto debemos crear un archivo en `/etc/init.d/` al que llamé `rclocal`. 
Seguramente verás en algunos tutoriales que lo llaman `rc.local`, pero openSUSE 
no permite esta nomeclatura y con `rclocal` no tendrás problemas.

Este es el contenido de mi archivo:

    ### BEGIN INIT INFO
    # Provides: rc.local
    # Required-Start: $network $syslog
    # Required-Stop: $network $syslog
    # Default-Start: 3 5
    # Default-Stop: 0 1 2 6
    # Description: Archivo de inicio personalizado para VBBienForjada
    ### END INIT INFO

    mount -o fmask=0133,dmask=0022,uid=1000 -t vboxsf ssh /home/javier/win7

Lo que sigue es darle permisos de ejecución con «chmod +x rclocal» y agregarlo 
al sistema de arranque con la orden

    chkconfig --add rclocal

De este modo, al reiniciar, las carpetas compartidas en VirtualBox estarán habilitadas.

