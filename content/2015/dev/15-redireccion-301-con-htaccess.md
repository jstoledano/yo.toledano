Title: Redirección 301 con htaccess
Date: 2013/11/20 17:48
Category: Desarrollo 
Tags: admin, apache,  
Slug: redireccion-301-con-htaccess
Author: Javier Sanchez Toledano
Summary: 

Hoy le dije adios a PHP[^1] y regreso a simple y puro HTML. El cambio es mas o menos simple. Ahora en este sitio funciona la publicación programada, por lo que no hay mayor problema con reconstruir todo el sitio.

[^1]: Este artículo lo escribí en el 2007, creo, cuando usaba Movable Type.

Lo que tenía que evitar a toda costa es que Google considerara las nuevas páginas como contenido duplicado, por lo que tenía que redirigir las páginas anteriores a las nuevas páginas.

Este es el procedimiento:

La mejor forma de redigir el tráfico es usar redirecciones en el archivo .htaccess. Este método no genera ningún retraso porque antes de servir una página a los navegadores, el servidor verifica que exista un archivo `.htaccess`, si lo encuentra, la página anterior nunca se carga, en su lugar a los visitantes se les envía directamente la nueva página.

Si necesitas información más técnica, puedes consultar el [tutorial de Apache](http://httpd.apache.org/docs/1.3/howto/htaccess.html).

### Consideraciones importantes al trabajar con el archivo `.htaccess`.

* Siempre edita y sube tus archivos en modo ASCII, subirlos en modo binario puede provocar que deje de funcionar tu sitio
* El archivo `.htaccess` no funciona en servidores Windows
* Asegúrate de checar y rechecar los cambios que realices, borra el caché y verifica que los encabezados que envía el servidor sean 301 (lo que significa que los cambios son permanentes) y no 302 a menos que los cambios sean verdaderamente temporales.
* Algunos sistemas operativos no permiten crear achivos que empiecen con un punto, por lo que tal vez tengas que llamar el archivo htaccess.txt y luego renombrarlo cuando está en el servidor.
* Asegúrate que tu programa FTP puede visualizar los archivos `.htaccess`, puedes usar [Filezilla](http://sourceforge.net/projects/filezilla) que es *Open Source*.
* Recuerda cambiar `ejemplo.com` por tu propio servidor.

## Ejemplos de redirecciones con .htaccess

#### Para mover una sola página

Para mover una página sin problemas para los usuarios:

```htaccess
Redirect 301 /paginavieja.html http://www.ejemplo.com/nuevapagina.html
```

#### Para mover un sitio completo

Esto atrapará todo el tráfico de tu sitio anterior y lo redirigirá al índice de tu nuevo sitio. Si quieres redirigir cada página a su nueva ubicación, esta no es tu opción.

```apache
Redirect 301 / http://www.ejemplo.com/
```

#### Cómo cambiar la extensión de las páginas

Este ejemplo es exactamente lo que usa este blog para cambiar la extensión de las páginas de php a html. Busca cualquier página .php y la redirige a `.html` (por ejemplo `http://yo.toledano.org/index.php` lo redirige a `http://yo.toledano.org/index.html`). Debes tener mucho cuidado con esto, ya que redirige todas las páginas `.php`, asi que verfica tus cambios y vuélvelos a verificar.

```apache
RedirectMatch 301 (.*).php$ $1.html
```