Title: Cómo insertar imágenes en DocBook
Date: 2013/11/22 16:02
Category: Desarrollo 
Tags: docbook, maquetacion 
Slug: como-insertar-imagenes-en-docbook
Author: Javier Sanchez Toledano
Summary: 

Bueno, no lo sabía. Pero por alguna razón no puedo usar imágenes PNG en 
DocBook. En un principio había pensado que se debía a problemas de rutas, pero 
no. Ahora sé bien que debo usa imágenes JPEG. Nada del otro mundo usando 
convert de ImageMagick.

    :::xml
    <mediaobject>
      <imageobject>
        <imagedatafileref="img/compilador-1-2.jpg" format="JPEG" scale="20" align="center"/>
      </imageobject>
      <imageobject>
        <imagedatafileref="img/compilador-1-2.eps" format="EPS"/>
      </imageobject>
    </mediaobject>


