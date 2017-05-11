Title: Integrar el protocolo OpenGraph en Django
Date: 2013/11/28 22:13
Category: Desarrollo 
Tags: google, opengraph, facebook, social 
Slug: integrar-el-protocolo-opengraph-en-django
Author: Javier Sanchez Toledano
Summary: 

Ya vimos en el artículo anterior [como integrar el protocolo OpenGrap en Genesis Framework](/genesis/integrar-el-protocolo-opengraph-en-genesis/) y ahora veremos como hacer esto mismo en Django, algo que todavía más simple.

!!! note-success "El blog es **namespace.mx**"
    Este blog usa el código que te muestro a continuación, y puedes verlo funcionar al revisar el código fuente de esta misma página.

Vamos a agregar las mismas propiedades que en un blog con WordPress, así que agregamos directamente las propiedades en nuestra plantilla de páginas, y en algunas propiedades usamos variables y en otras constantes, por ejemplo en `og:site_name`, `og:locale`, `og:type`, al igual que en el artículo anterior.

Pero observa la forma en que generamos la propiedad `og:title`, mientras que en WordPress necesitamos `<?php echo the_title_attribute( 'echo=0' ); ?>` en Django basta con `{{entry.title}}`, veamos las dos líneas juntas:

```language-php
// En WordPress
<meta property="og:title" content="<?php echo the_title_attribute( 'echo=0' ); ?>" />
```

```language-django
{# En Django #}
<meta property="og:title" content="{{entry.title}}">
```

Este es un ejemplo de la eficiencia que puedes obtener al programar tu blog con Django.

Otro ejemplo es como generamos la imagen, que es la misma para todos los post[^1] y usamos la función `static` y le pasamos como parámetro la ruta del archivo, que Django busca y convierte en una URL correctamente formada.

```language-django
<meta property="og:image" content="http://namespace.mx{% static 'img/namespace.logo.png' %}">
```

Antes de presentar el código completo, debemos recordar que el código se escribe directamente en la plantilla, en lugar de procesarlo primero en un una función que es evaluada en cada solicitud, por lo que volvemos a ganar eficiencia en comparación con WordPress.

Ahora si, el bloque completo.

[^1]: Más adelante, en un ejemplo más avanzado veremos como obtener las imágenes de un post.


```language-xml
{% block metafacebook %}
  <meta property="og:site_name" content="namespace.mx - Programamos en Python, Django y WordPress">
  <meta property="og:locale" content="es_LA">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{{entry.title}}">
  <meta property="og:image" content="http://namespace.mx{% static 'img/namespace.logo.png' %}">
  <meta property="og:image:type" content="image/jpeg">
    <meta property="og:image:width" content="200">
    <meta property="og:image:height" content="200">
  <meta property="og:description" content="{{ entry.resumen|truncatewords_html:30|striptags|safe }}">
  <meta property="og:url" content="http://namespace.mx{{ entry.permalink }}">
{% endblock metafacebook %}
```

