Title: Cómo sobreescribir el método save() en Django
Date: 2013/11/19 19:40
Category: Desarrollo
Tags: patterns, python, django, metodos
Slug: como-sobreescribir-el-metodo-save-en-django
Author: Javier Sanchez Toledano
Summary:

Para el nuevo indicador, que mide el tiempo en el que distribuimos nuestro producto desde las subdelegaciones hasta los centros de atención a clientes, capturamos los siguientes datos:

- id del sitio,
- fecha de corte,
- lote de producción,
- fecha y hora (timestamp) de recepción en la subdelegación, y
- fecha y hora de recepción en el centro de atención.

Necesitamos saber la diferencia en horas entre las fechas de recepción, pero como ya sabemos lo complicado que es hacer cálculos en consultas con Django, en esta ocasión vamos a generar la diferencia al momento de guardar la tabla, sobreescribiendo el método `save()` de nuestro modelo.

### Sobreescribiendo el método `save()` en Django

Primero veamos nuestro modelo:

```python
class Distribucion (models.Model):
    mac           = models.CharField (max_length = 6)
    fecha_corte   = models.DateField (default=timezone.now)
    lote          = models.CharField (max_length = 13)
    recibidoVRD   = models.DateTimeField ()
    disponibleMAC = models.DateTimeField ()
    diferencia    = models.IntegerField ()

    def __unicode__ (self):
        return "%s - %s - %s" % (self.mac, self.lote, self.fecha_corte)
```

Como pueden ver, existe un campo llamado `diferencia` que será nuestro campo calculado, para eso creamos el método `save` dentro de nuestro modelo y ponemos el valor calculado en segundos.

    :::python
    def save(self):
        difFecha = self.disponibleMAC - self.recibidoVRD
        self.diferencia = difFecha.seconds
        super (Distribucion, self).save()

Con esto, cada vez que actualicemos o agreguemos un registro, se calcularán los segundos de diferencia entre las dos fechas, en nuestra vista, podemos convertir estos segundos en el formato de nuestra preferencia.
