Title: Generador de clases con Python y YAML 
Date: 2015-05-20 20:58:42
Category: Desarrollo
Tags:  python, webdev
Author: Javier Sanchez Toledano
Summary: Como crear un generador de clases con Python y YAML

En el proyecto en el que estoy trabajando actualmente, el Cuadro Mando Integral, existe un módulo encargado de gestionar evidencias documentales de nuestro trabajo. 

## Las metas

Se organizan por puestos y por persona, y a cada persona le corresponde, según su puesto, cierto número de metas, desde tres hasta 15. Digamos que el promedio es ocho y que hay unos siete puestos diferentes en cuatro sitios. Esto hace que el sistema maneje unas 56 metas diferentes.

La parte mas complicada de todo es que aunque son metas diferenciadas, es necesario que se contabilicen en su totalidad. Y las evidencias se clasifiquen de acuerdo al nivel que alcanzaron, alto, medio o bajo.

## Modelos abstractos

La solución fue crear un modelo abstracto que hereda a las 56 metas sus características comunes. Esto hace que cada meta se controle por separado y que estén ligadas en una tabla central.

Nunca pude hacer esto de una forma en la que pudiera sentirme cómodo. Me parece que mi código es sucio e ineficiente.

Por ejemplo, tardaba mucho escribiendo cada modelo para cada una de las metas. Me tomaba mucho tiempo hasta que decidí usar YAML.

## YAML

YAML, que según su sitio no es un lenguaje de marcado, es un formato para serializar datos. Esto quiere decir que podemos usar YAML para guardar datos de forma estructura y mantenerlos legibles. 

Es muy fácil de usar y tiene una sintaxis estricta, lo que garantiza que el documento pueda ser interpretado correctamente en una variedad de plataformas.

## Las Metas

Usé YAML para describir los modelos de las metas, en un formato que prácticamente se explica por si mismo. Miren.

```yaml
#VRL02
miembro: vrl
id: 2
nombre: Programación Trimestral
repeticiones: 8
campos:
  - oficio: ['Oficio de programación', False]
  - programacion: ['Programación Trimestral', False]
  - oficio-sis: ['Oficio SIS', False]
---
```

- La primera línea `#VRL02` es un comentario.
- La segunda es un campo `miembro` y su valor que es `vrl`.
- La tercera, cuarta y quinta línea también son campos, y su valor se especifica después de los dos puntos `:`.
- `campos` es un campo especial que esta formado por una lista de valores,
- estos a su vez, están formados por otro conjunto de atributos.

La lista de campos contiene la descripción que asigné a estos campos, por ejemplo el campo `oficio-sis` tiene dos atributos, el primero es `'Oficio SIS` y el segundo es `False` que utilizaré a continuación para crear la clase.

## La clase generadora

Entonces hice un archivo en Python que usará el archivo YAML que contiene la descripción de las metas para convertirlo en un archivo de Python y usarlo en Django.

Usaré el módulo `PyYAML` y lo primero que voy a hacer es importarlo:

```python
import yaml
```

A continuación voy a abrir el archivo para procesarlo con YAML:

```python
metas = yaml.load_all(open('metas.yml').read())
```
A continuación, defino una clase y su inicialización que recibe una meta como parámetro:

```python
class Generador():

    def __init__(self, meta):
        self.miembro = meta['miembro']
        self.id = meta['id']
        self.nombre = meta['nombre']
        self.repeticiones = meta['repeticiones']
        self.campos = meta['campos']
```

Y elementos que usaré para crear la clase:

```python
    def get_campos(self):
        return self.campos

    def get_meta(self):
        return '%s%02d' % (self.miembro.upper(), self.id)
```

La función que genera la clase, simplemente es una cadena con espacios variables que se sustituyen con los valores que tomo del archivo YAML.

```python
    def get_clase(self):
        clase = """class %s(Evidencia):""" % self.get_meta()
        for c in self.get_campos():
            for k, v in c.iteritems():
                blank = 'blank=True, null=True' if v[1] else ''
                clase += "\n    %s = models.FileField('%s', \
upload_to=subir_archivo, %s)" % (k, v[0], blank)
        clase += """\n
    class Meta:
        app_label = 'metas'
        """
        return clase
```

Al pasar el archivo por un ciclo for, solo llamo a la clase e imprimo el resultado:

```python
for meta in metas:
    m = Generador(meta)
    print m.get_clase()
```

Y así generé mi archivo de metas, de forma automática.

```python
class VRL02(Evidencia):
    oficio = models.FileField('Oficio de programación', upload_to=subir_archivo, )
    programacion = models.FileField('Programación Trimestral', upload_to=subir_archivo, )
    oficio-sis = models.FileField('Oficio SIS', upload_to=subir_archivo, )

    class Meta:
        app_label = 'metas'
```

En un artículo posterior, utilizaré esta técnica para crear fichas de procesos de cada uno de los procesos definidos en el plan de la calidad de nuestro sistema de gestión.
