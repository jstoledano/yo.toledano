Title: Configurar suPHP y userdir en Ubuntu
Date: 2013/11/21 19:02
Category: Desarrollo 
Tags: admin, php, apache 
Slug: configurar-suphp-y-userdir-en-ubuntu
Author: Javier Sanchez Toledano
Summary: 

Configurando mi laptop con Ubuntu 12.04, tocó el turno de instalar una copia de WordPress para trabajar de manera local, así que procedí a instalar Apache2, PHP, phpMyAdmin y MySQL. Todo iba bien hasta que para evitar modificar permisos en el sitio por default, decidí trabajar desde mi directorio, ya saben, con la ruta `http://localhost/~javier`.

Apache2 funciona con su propio usuario y grupo especial, llamado `www-data`, que por su bajo ID tiene al mismo tiempo privilegios y permisos de ejecución especiales. Por otro lado, `phpmyadmin` usa por defecto `mod_php` para ejecutar al intérprete.

Usar `mod_php` le da mucha velocidad a la ejecución de *scripts* o guiones PHP, a cambio obliga a Apache2 a cargar al intérprete en memoria para cada hilo de ejecución del daemon `htttd` y restringe su ejecución al usuario `www-data`.

Esto se hace notar de inmediato, en la instalación de WordPress ya que al intentar crear el archivo `wp-config.php`, el intérprete carece de los permisos necesarios y la instalación se detiene. Incluso creando a mano el archivo de configuración, nuestros problemas seguirían ya que no tendríamos cache o la posibilidad de instalar temas, extensiones o *plugins* o subir archivos multimedia.

La solución por la que me decanté era usar los directorios personales y PHP con permisos de usuario. La pérdida de velocidad es insignificante para mi, que uso una copia local de Cyberia.MX en mi laptop, así que no me importó.

### Cómo instalar userdir para Apache2 en Ubuntu

Esta parte es muy sencilla, solo tenemos que escribir los siguientes comandos en una consola:

```language-bash
a2enmod userdir
sudo service apache2 restart
```

El comando `a2emod` habilita cualquiera de los módulos que se encuentran en este directorio `/etc/apache2/mods-available`, creando un enlace simbólico a la carpeta `/etc/apache2/mods-enabled`. El comando que hace exactamente lo contrario es `a2dismod`.

El segundo comando reinicia el *daemon* `apache2`, deteniéndolo y arrancándolo de nuevo, lo que hace que se cargue toda la configuración.

Pero para que pueda ejecutar guiones de PHP, `userdir` necesita una configuración especial. Necesitamos habilitar el motor del intérprete, este es mi archivo de configuración de `userdir`: `/etc/apache2/mods-available/userdir.conf`.

```language-apache
 <IfModule mod_userdir.c>
  UserDir public_html
  UserDir disabled root

  <Directory /home/*/public_html>
    AllowOverride FileInfo AuthConfig Limit Indexes
    Options MultiViews Indexes SymLinksIfOwnerMatch IncludesNoExec
    <Limit GET POST OPTIONS>
      Order allow,deny
      Allow from all
    </Limit>
    <LimitExcept GET POST OPTIONS>
      Order deny,allow
      Deny from all
    </LimitExcept>
  </Directory>
</IfModule>
```

### Cómo instalar suPHP en Ubuntu

El siguiente paso es instalar suPHP, cuya función es ejecutar el intérprete en el espacio de un usuario, con los permisos y restricciones del propio usuario, es decir, ejecuta PHP como el usuario.  Así es como funcionan los principales proveedores de hosting, como HostGator y GeekStorage.

Para poder usar este módulo, necesitamos instalar el paquete `libapache2-mod-suphp`, y configurarlo adecuadamente. A continuación verás mi archivo de configuración ubicado en `/etc/apache2/mods-available/suphp.conf`:

```language-apache
<IfModule mod_suphp.c>
    AddType application/x-httpd-suphp .php .php3 .php4 .php5 .phtml
    suPHP_AddHandler application/x-httpd-suphp

    <Directory />
        suPHP_Engine on
    </Directory>

    # By default, disable suPHP for debian packaged web applications as files
    # are owned by root and cannot be executed by suPHP because of min_uid.
    #<Directory /usr/share>
    #    suPHP_Engine off
    #</Directory>

# # Use a specific php config file (a dir which contains a php.ini file)
#    suPHP_ConfigPath /etc/php4/cgi/suphp/
# # Tells mod_suphp NOT to handle requests with the type <mime-type>.
#    suPHP_RemoveHandler <mime-type>
</IfModule>
```

Observa que las líneas 11, 12 y 13 están comentadas y esto es importante para poder ejecutar phpMyAdmin, como veremos más adelante.

También es necesario editar el archivo `/etc/suphp/suphp.conf`, y tomar en cuenta las siguientes líneas:

```language-apache
;Path all scripts have to be in
docroot=/var/www:${HOME}/public_html:/usr/share/phpmyadmin

;Path to chroot() to before executing script
;chroot=/mychroot

; Security options
allow_file_group_writeable=true
allow_file_others_writeable=true
allow_directory_group_writeable=true
allow_directory_others_writeable=true

;Check wheter script is within DOCUMENT_ROOT
check_vhost_docroot=false
```

Para permitirle a PHP la posibilidad de crear archivos y directorios, para evitar que busque la raíz de un virtual host y para agregar al directorio de phpMyAdmin a la lista de rutas permitidas.

Verifica que tu archivo contenga estas líneas.

### Configurar phpMyAdmin en Ubuntu con suPHP

Ahora toca el turno de configurar a phpMyAdmin, que supongo que ya instalaste y configuraste.

Lo importante en este archivo `/etc/apaches/conf.d/phpmyadmin.conf` es agregar al inicio del archivo, las siguientes dos líneas:

```language-apache
ServerAdmin webmaster@localhost
DocumentRoot /usr/share/phpmyadmin
```

Con esto nos aseguramos que sea identificado por `suPHP` como uno de los directorio de ejecución definidos.

Volvemos a reiniciar el servidor y estamos listos para usar `suPHP` y `userdir` en Ubuntu.
