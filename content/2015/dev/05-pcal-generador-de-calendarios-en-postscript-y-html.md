Title: pcal – Generador de calendarios en PostScript y HTML
Date: 2013/11/18 19:14
Category: Desarrollo 
Tags: tools, 
Slug: pcal-generador-de-calendarios-en-postscript-y-html
Author: Javier Sanchez Toledano
Summary: 

Recientemente redescubrí `pcal`. Un programa que genera archivos `ps` o `html` con un calendario. Este calendario puede estar vacío o puede tener la información que quieras incluir en un archivo especial. El calendario puede ser vertical (_portrait_) u horizontal (_landscape_ ) y estar en una variedad de idiomas, entre ellos el español.

La sintaxis del archivo de calendario no es fácil, pero una vez que la dominas, puedes incluir incluso imágenes. Mira un ejemplo del archivo de calendario, llamado `~/.calendar`.

    input-language es  # define el idioma en el que escribes los días
    opt -P letter  # define el tamaño de la hoja
    opt -m  # muestra un iciono de la la fase lunar
    opt -a es  # define el idioma de impresión (en este caso, español)
    opt -J   # agrega el dia juliano a los dias
    opt -E  # utiliza el estilo de fechas europeo (dd/mmm/aaa)
    opt -r Latin1  # define la codificacion de salida
    opt -Y-50   # mueve el calendario 50 puntos abajo (para engargolarlo)
    opt -y .90   #escala el calendario al 90% (para engargolarlo)

    # Pone el número de la semana en cada lunes
    all lun in all  Semana %w

    # El día 15 o el día hábil próximo anterior escribe "Días de Quincena"
    workday on_or_before all 15 Dias de Quincena

    # Mi cumpleaños
    3 dic Mi cumple

Por último con esta línea generas el calendario para todo el 2006, imprimiendo un mes por hoja, en un archivo llamado `2006.ps`.

    pcal -o 2006.ps  2006

!!! alert-info "¡Precaución!" 
    Esta entrada se publicó originalmente el 23 de enero de 2006 en el blog <strong>«Yo, Toledano»</strong>. Su contenido podría no estar actualizado.
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTEyOTQ1MDEwMjldfQ==
-->