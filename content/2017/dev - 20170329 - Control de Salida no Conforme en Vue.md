Title: Control de salidas no conformes, parte I
Date: 2017-03-29 13:57:22
Category: desarrollo
Tags: cmi, vuejs, javascript, axios
Summary: Iniciamos con el desarrollo de una aplicación para controlar productos no conforme usando el framework VueJS

Según la norma ISO 9001:2015, la organización _debe controlar las salidas que no sean conformes con sus requisitos_, y estos controles deben aplicarse también a los productos y servicios no conformes detectados después de la entrega. 

Además, existen cuatro posibles maneras de tratar a una salida no conforme y por supuesto debe existir información documentada sobre la no conformidad.

Las Solicitudes de Actualización que no cumplen con los requisitos para su resguardo en el Centro de Cómputo y Resguardo Documental, CeCyRD, reciben un tratamiento de __salida no conforme__, por lo que existe una aplicación y un indicador que nos ayuda en esta tarea.

En la re-ingeniería del cuadro de mando, esta aplicación llamada `rechazos` está compuesta por pequeñas piezas que realizan actividades muy concretas.

Vamos a empezar describiendo el control de rechazos.

### El control de salida no conforme
La información documentada que se resguarda en CeCyRD está compuesta por hasta tres documentos físicos, la solicitud individual que es obligatoria y hasta dos testimoniales, una para suplir el comprobante de domicilio y otra para cumplir con el requisito de identificación con fotografía.

Hay más de 30 requisitos en estos documentos, treinta riesgos de rechazos y se deben de controlar todos ellos. Pero además, los riesgos aparecen en diferentes lugares, es decir:

- en el área de trámite de la solicitud
- en el área de recibo de la solicitud
- en la testimonial de fotografía 
- en la testimonial de domicilio
- etc.

El tipo de control que solicita CeCyRD y la norma ISO 9001 requieren que se identifique la salida no conforme para poder tomas las acciones adecuadas para solucionarla.

Ahora bien, para mantener la compatibilidad con la información que ya existe, decidí dejar la misma estructura.

### Modelo Conjunto
Este modelo no es realmente necesario, solo contiene tres registros, pero se utiliza para _filtrar_ los requisitos por tipo de documento. En la primera versión, llamé a esta tabla `Conjunto`.

En esta nueva aplicación, ya use el _paradigma de conductas_[^1], el modelo `Conjunto` en Django se ve así:

```python
class Conjunto(Trackable, Authorable, Permalinkable, Timestampable):
    """
    Este modelo es un apoyo para disminuir los errores de captura de rechazos.
    Solo son tres conjuntos, que corresponden a los numerales romanos en el
    catálogo de causas de rechazo.
    """
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre
```

Debido a los _mixins_, solo se requiere un campo en este modelo.

El serializador, pretende[^2] unir la clave foránea `author` con el modelo `User`, además, se devuelven todos los campos.

```python
class ConjuntoSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Conjunto
        fields = '__all__'
```

El _ViewSet_ tiene como permisos estándar, los permisos indicados en el modelo de Django o si es un acceso anónimo, de solo lectura: `permissions.DjangoModelPermissionsOrAnonReadOnly`. El __único__ tipo de acreditación permitida para este _endpoint_ es `TokenAuthentication`.

```python
class ConjuntoViewSet(viewsets.ModelViewSet):
    """
    Lista el catálogo de conjuntos
    """
    queryset = Conjunto.objects.all()
    serializer_class = ConjuntoSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )
```

En el lado del cliente, usando __VueJS__, traemos el contenido de este modelo con una promesa, usando __Axios__:

```javascript
  let _getConjuntos = function () {
    this.axios.get('http://localhost:8000/rechazos/conjuntos').then((carga) => {
      this.conjuntos = carga.data.map((conjunto) => {
        return {
          id: conjunto.id,
          nombre: conjunto.nombre,
          slug: conjunto.slug,
          autor: conjunto.author
        }
      })
    })
  }
```

Esta función _mapea_ el contenido porque solo requerimos cuatro campos. Esta función la colocamos en los métodos:

```javascript
    methods: {
      getConjuntos: _getConjuntos
    },
```

y la activamos en el gancho `mounted()`:

```javascript
    mounted () {
      this.getConjuntos()
    }
```

De este modo, la variable `conjuntos` queda poblada con el contenido de este modelo.

En el próximo archivo, veremos como realizar operaciones CRUD con VueJS y Django.


[^1]: De este paradigma, se tratará un próximo artículo. 
[^2]: Digo _pretende_, porque no aparece ninguna relación.