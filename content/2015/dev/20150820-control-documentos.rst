Control de Documentos para la norma ISO 9001 con Django
############################################################

:date: 2015-08-20 20:34:45 GMT-5
:tags: iso9001, django, calidad
:category: Desarrollo
:slug: control-documentos-iso9001-django
:summary: Cómo controlar los documentos de un sistema de gestión de la calidad ISO 9001 usando Django

La norma ISO 9001 pide que controlemos la documentación que requiere el sistema de gestión de la calidad, incluídos los procesos relacionados, la información creada para que la organización opere y la evidencia de los resultados alcanzados. En este artículo trataremos de explicar como usamos Django para dar cumplimiento a la norma ISO 9001:2008

La documentación en la norma ISO 9001
=====================================

Con la nueva versión de la norma ISO 9001, la 2015, ha habido un cambio en los requisitos relacionados con la documentación del sistema de gestión. Básicamente los *procedimientos generales* que eran obligatorios ahora ya no existen como requisito. Esto hace más fácil la implementación de la norma, pero puede acarrear algunos problemas al portar un sistema a la nueva versión ya que es la organización quien ahora define qué información documentada necesita para operar.

En este caso, mi recomendación es seguir usando los procedimientos actuales, ya que **la norma ISO 9001:205 elimina la obligación, pero no la necesidad**. Si la organizción considera que es necesario seguir usando un procedimiento de control de documentos, lo debe establecer así.

Por lo tanto, este ejercicio es válido tanto para la versión 2008 como para la 2015 de la norma ISO 9001.

Requisitos relacionados con la documentación
============================================

Son varios los requisitos relacionados con la documentación de un sistema de gestión de la calidad, empezando con la disponibilidad de la información [#fn1]_ necesaria para la operación y el seguimiento de los procesos necesarios para el SGC.

La versión 2015 es más abierta en este sentido y nos dice que la organización debe mantener la información documentada en la medida necesaria.

Y entre otras cosas que debemos mantener como información documentada (en una mezcla entre ambas versiones) tenemos el alcance, la política y objetivos de la calidad, el manual de la calidad, los procedimientos generales obligados por la versión 2008 y cualquier otro que la organización considere necesario.

Uno de estos procedimientos *generales* obligatorios es el de control de documentos, y pide que en este, la organización se asegure que los documentos se aprueban, se identifican los cambios, que las versiones correctas estén disponibles, etc.

Un poco de historia
-------------------

La versión ISO 9001:2000 tenía un enfoque basado en procedimientos, decían entonces: *hay un procedimiento para todo*. Y pedían estos procedimientos documentados. Era una norma documental que tendía hacía la burocracia. Entonces una fórmula que encontraron las organizaciones para cumplir con los requisitos fue hacer listas.

Había listas de documentos, de procedimientos, de formatos, de documentos externos, de registros, de copias controladas, de distribución, ¡de todo! Y caundo se cambiaba un documento se tenían que actualizar las listas respectivas de todos los usuarios.

La publicación electrónica ayudó un poco: se publicaban los documentos en formato PDF y se impedía la impresión. Pero la actualización de las dichosas listas seguía siendo una molestia. Y los auditores se dedicaban a cazar listas de documentos desactualizadas.

Con este enfoque iniciamos nuestro sistema de gestión de la calidad [#fn2]_ y un tiempo después decidimos cambiar nuestra estrategia de control de documentos.

Distribución electrónica de documentos
======================================

La decisión de distribuir electrónicamente los documentos fue estratégica, no solamente publicabamos los documentos, creamos un sistema que asignaba códigos de identificación, controlaba las versiones, creaba listas de documentos y permitía la consulta e impresión de los documentos.

Aprovechando el núcleo del cuadro de mando, implementamos esta distribución electrónica usando Django. De modo que el control de usuarios y el tema es heredado del núcleo, lo que permitió acelarar el desarrollo y ayudó a los usuarios a tener una experiencia consolidada con el resto del sitio.

Organización de documentos
--------------------------

Uno de los primeros requisitos de la distribución electrónica era que en el servidor, los documentos tuvieran un órden lógico que fuera coherente con su origen y más aún, que su nombre explicara por si mismo el origen del documento.

Para lograr esto escribí una pequeña función que asigna el nombre adecuado y organiza los documentos en directorios.

.. code-block::python


    def subir_documento(instancia, archivo):
        ext = archivo.split('.')[-1].lower()
        orig = 'docs'
        tipo = instancia.documento.tipo.slug
        doc = instancia.documento.slug
        rev = instancia.revision
        nombre = "%s_%s-%02d_rev%02d.%s" % (
            doc, tipo, instancia.documento.id, rev, ext
        )
        ruta = Path(orig, tipo, nombre)
        return ruta

Esta función toma la instancia del objeto al que pertence el archivo y el nombre del mismo. Lo primero que hace es obtner la extensión con ``archivo.split('.')[-1].lower()``.

En ``orig`` está el nombre del directorio raíz para los documentos, en ``tipo`` se guarda el tipo de documento [#fn3]_ que sirve como subdirectorio

.. [#fn1] Ahora *información documentada* en la norma ISO 9001:2015.
.. [#fn2] Claro que en ese tiempo no sabíamos que era un enfoque incorrecto.
.. [#fn3] Procedimiento, Formato, Documento externo, etc., como veremos más adelante.
