Title: Cómo subir un directorio con FTP
Date: 2013/11/18 19:24
Category: Desarrollo 
Tags: ftp, tools 
Slug: como-subir-un-directorio-con-ftp
Summary: 

<p>Si el único acceso que tienes a tu sitio web es con <span class="caps">FTP</span> y quieres subir un directorio, puedes usar el comando mput para subir múltiples archivos. Pudes hacerlo de manera automática o puedes autorizar cada trasnferencia.</p>

<p>Para autorizar cada transferencia sigue estos pasos:</p>

    ftp servidor.com     # Te concectas al servidor
    cd directorio        # para cambiarse al directorio
    mput *.*             # para subir todos los archivos

<p>Para transferir los archivos sin que el programa solicite autorización:</p>

    ftp -i servidor.com    # Te concetas al servidor
    cd directorio          # para cambiarse al directorio
    mput *.*               # para subir todos los archivos

<p>Esas son las dos opciones.</p>

<p class="alert alert-error">Esta entrada apareció orignalmente en el blog <em>«Yo, Toledano»</em> el 10 de junio de 2007. Su contenido <strong>podría</strong> estar desactualizado.</p>
