Title: Encontrar archivos en Linux con find
Date: 2014/01/10 02:59
Category: Desarrollo 
Tags: linux, tools 
Slug: encontrar-archivos-en-linux-con-find
Author: Javier Sanchez Toledano
Summary: 

Seguramente te has enfrentado al problema de que subes un directorio a tu servidor y resulta que todos los permisos están incorrectos. O peor aún, solo los permisos de los archivos PHP o de los directorios.

Bueno, pues aqui está la solución, simple y elegante: usar el comando `find`. Dejo algunos ejemplos:

#### Cambiar los permisos de todos los directorios a 775:

Aplica los permisos especificados (`chmod 755`) a todos los directorios (`-type d`) encontrados en la ruta.

    find . -type d -exec chmod 775   {} \;

#### Cambiar el dueño de todos los directorios:

En el mismo sentido que el ejemplo anterior, aplica el comando especificado (`chown usuario:grupo`) a los directorios (`-type d`):

    find . -type d -exec chown usuario:grupo   {} \;

#### Cambiar los permisos de todos los archivos a 664:

El objetivo ahora es contrar todos los archivos (`-type f`) que se encuentran debajo del directorio actual y cambiarles los permisos (`chmod 644`)

    find . -type f -exec chmod 644 {} \;

<div style="max-width:360px; margin: 25px auto;">
<!-- cyberia.336x289.01.top -->
<ins class="adsbygoogle"
style="display:inline-block;width:336px;height:280px"
data-ad-client="ca-pub-9466828947698623"
data-ad-slot="8590866557"></ins>
<script>
(adsbygoogle = window.adsbygoogle || []).push({});
</script>
</div>
<div style="clear:both;"></div>

#### Cambiar los permisos de todos los archivos con extensión PHP a 664:

    find . -type f -name '*php' -exec chmod 664  {} \;

Este comando se lee de la siguiente manera.

* `.` El punto indica el directorio actual. `find` busca en todos los subdirectorios a partir del lugar donde se ejecuta.
* `-type f` Indica que las coincidencias deben ser tipo archivo o `file`.
* `-name '*php` Indica que las coincidencias deben ser cuando la terminación sea `php`
* `-exec comando {} \;` Indica que el comando se ejecutará agregando las coincidencias al final. El punto y coma sirve para que regrese `0 (cero) si tuvo éxito. Y la diagonal es para _escapar_ el punto y coma.
