Title: Annoying, un básico para tus proyectos
Date: 2014/03/14 22:48
Category: Desarrollo
Tags: models, patterns, django, modules
Slug: annoying-basico-para-proyectos
Author: Javier Sanchez Toledano
email: javier@namespace.mx
Summary: Un módulo para facilitarte la vida en Django.

 

Hasta antes de la versión 1.6 de **Django**, configurar los archivos estáticos era un gran problema para mí, porque creo que nunca había entendido como funcionaba. Entonces me encontré con módulo excelente llamado [`django-annoying`][annoying] contiene algunas funciones que hacen que el trabajo sea mucho más fácil. 

La verdad no soy bueno usando **decorators**, ya que no los entiendo, pero hay uno de _django-annoying_ que me gusta mucho usar porque hace que usar las plantillas sea muy sencillo. Pero tiene muchas características más.

### Características

* `render_to_decorator` - Facilita la escritura de vistas o _views_ y reduce el tiempo de escritura. Este es el decorador que más me gusta, más abajo veremos como se usa.
* `signals_decorator` - Dicen que permite usar señales como decorador. Nunca he usado las señales, así que no entiendo como funciona.
* `ajax_decorator` - Regresa un objeto `JsonResponse` con un diccionario como contenido. Nunca lo he usado.
* `get_config` - Es una **función** que regresa una variable de configuración de `django.settings`, si es que existe o bien un valor por default. Nunca la he usado, pero me parece útil.


Miren, para que vean como lo uso, les mostraré una vista simple escrita sin este módulo y luego la misma pero con `annoying`.

    :::Python
    def main(request):
        """Main listing."""
        avisos = Aviso.objects.all().order_by("-creacion")
        paginator = Paginator(avisos, 5)
    
        try: 
            page = int(request.GET.get("page", '1'))
        except ValueError: 
            page = 1
    
        try:
            avisos = paginator.page(page)
        except (InvalidPage, EmptyPage):
            avisos = paginator.page(paginator.num_pages)
    
        return render_to_response("avisos/lista.html", 
            {'avisos':avisos, 'title':'Avisos'},
            context_instance=RequestContext(request) )

Ahora esta misma fista con `annoying` se ve así.

    :::Python
    from annoying.decorators import render_to
    
    @render_to('index.html')
    def main(request):
        """Main listing."""
        avisos = Aviso.objects.all().order_by("-creacion")
        paginator = Paginator(avisos, 5)

        try: 
            page = int(request.GET.get("page", '1'))
        except ValueError: 
            page = 1

        try:
            avisos = paginator.page(page)
        except (InvalidPage, EmptyPage):
            avisos = paginator.page(paginator.num_pages)

        return {'avisos':avisos, 'title':'Avisos'}
        
Como pueden ver la magia ocurre en el momento de regresar el resultado de la vista. El contexto y la plantilla pasan automáticamente gracias a nuestro decorador. Solo tenemos que preocuparnos por los datos de nuestra vista.

¿Qué les parece?


[annoying]: http://conxb.com/ns-annoying
