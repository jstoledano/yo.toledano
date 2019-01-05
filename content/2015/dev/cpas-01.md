Title: Control de Planes de Acción con Django  
Date: 2014-11-16 20:36:30  
Category: Desarrollo  
Tags: calidad, cpas, python, django,   
Author: Javier Sanchez Toledano  
Summary: Desarrollo de una aplicación para el control de planes de acción y seguimiento, de acuerdo a la norma ISO 9001:2015 y a la norma COSO II para el control de riesgos.

Planeamos usar Django para controlar los planes de acción y seguimiento como una forma de asegurarnos que estas acciones era efectivas y que el control era eficiente. 

## Datos constantes en el Control de Planes de Acción
Existen algunos datos que son constantes en todos los planes de acción. Colocarlos accesibles a todos los modelos de la aplicación es una buena idea. Estos son los datos.


#### Procesos en el SGC
El proceso en el que se detectó la _no conformidad_ o dónde el control de riesgos no fue efectivo. Tenemos cuatro procesos y agregamos una constante más por si es necesario crear un _Plan de Acción_ que afecte al sistema. 

```python
PROCESO = (
    (1, 'Planeación'),
    (2, 'Apoyo Soporte'),
    (3, 'Clave'),
    (4, 'MSA'),
    (5, 'SGC'),
)
```

#### Tipos de Plan de Acción
La norma __ISO 9001:2015__ nos dice que hay varias formas en las que puede ocurrir la mejora. Por ejemplo, de manera *reactiva* (por ejemplo, acción correctiva), de manera *incremental* (por ejemplo, mejora continua), mediante un *cambio significativo* (por ejemplo, avance), de manera *creativa* (por ejemplo, innovación) o por *reorganización* (por ejemplo, transformación).

Aunque no creo que todos estos tipos de _**cambio**_ ocurran en nuestro sistema, por ejemplo, no entiendo el _creativo_, pero no cuesta nada agregarlo.

```python
TIPO = (
    (1, 'Reactivo'),
    (2, 'Incremental'),
    (3, 'Innovación'),
    (4, 'Avance'),
    (5, 'Transformación'),
)
```

#### Detección de la no conformidad
Para la correcta determinación de la _no conformidad_ debemos indicar __cuándo__ se encontró, por ejemplo durante una auditoría, en la revisión por la dirección, al analizar los indicadores o los riesgos, etc.

```python
DETECCION = (
    (1, 'Auditoria Interna'),
    (2, 'Auditoria Externa'),
    (3, 'Revisión por los Vocales'),
    (4, 'Quejas'),
    (5, 'Otros'),
)
```



#### Tipo de mejora
También indicamos en la identificación del plan, si la mejora es a un proceso en particular, al producto o servicio o al sistema de gestión en lo general.

```python
MEJORA = (
    (1, 'Procesos'),
    (2, 'Servicio'),
    (3, 'Sistema')
)
```

#### Estado de una acción
La norma nos dice que debemos revisar la eficacia de las acciones tomadas, también debemos informar sobre el estado de las acciones en cada revisión por la dirección, para eso le agregamos un _estado_ a cada acción.

+ __Seguimiento__ - Este es un estado genérico, en general no recomiendo usarlo, pero a veces, es necesario (sobre todo cuando no tenemos mucho que entregar).
+ __Revisión de la Evidencia__ -  Cuando el auditor encargado del plan recibe una evidencia del dueño de plan, esta acción pasa a este estado, es un estado temporal.
+ __En espera de una respuesta__ - También es un estado temporal, por ejemplo cuando en nuestra acción correctiva solicitamos presupuesto.
+ __En espera de una acción__ - Cuando alguien más nos tiene que entregar algo (documento, producto o servicio) para que el plan siga fluyendo.
+ __En espera de un evento__ - Cuando esperamos que algo pase, antes de continuar con el plan de acción.
+ __Cerrada__ -  Cuando la acción correctiva terminó, no importa si fue o no efectiva.

Estos estados son importantes, porque como veremos a detalle más adelante, no podemos cerrar una acción correctiva de forma manual, se cierran de forma automática de acuerdo al seguimiento y la evidencia registrada.

```python
A_ESTADO = (
    (1, u'Seguimiento'),
    (2, u'Revisión de Evidencia'),
    (3, u'En espera de una respuesta'),
    (4, u'En espera de una acción'),
    (5, u'En espera de un evento'),
    (6, u'Cerrada')
)
```

## Modelos para el Control de Planes de Acción

### Modelo Plan
La definición de un plan de acción incluye ocho elementos, seis de ellos definidos en este plan y los otros dos ocupan su propio modelo.

Empezamos con la definición del modelo:

```python
class Plan(models.Model):
    class Meta:
        verbose_name = _(u'Plan de Acción')
        verbose_name_plural = _(u'Planes de Acción')
```

#### I. Identificación
La identificación del plan incluye los datos de fechas de detección y de llenado, el proceso que afecta, el tipo de plan, cuándo se detectó la no conformidad, que tipo de mejora realiza este plan y un pequeño nombre único.

Ya explicamos antes algunos de estos valores y los otros se explican a si mismos. Esta es su definición.

```python
    # #################################### #
    # I. Identificación del plan
    fecha_llenado = models.DateField(
        'Fecha de Llenado',
        default=datetime.date.today()
    )
    fecha_deteccion = models.DateField('Fecha de Detección')
    proceso = models.PositiveSmallIntegerField(choices=PROCESO)
    tipo = models.PositiveSmallIntegerField(choices=TIPO)
    deteccion = models.PositiveSmallIntegerField(choices=DETECCION)
    mejora = models.PositiveSmallIntegerField(choices=MEJORA)
    nombre = models.CharField(max_length=40)
```

#### II. Revisión de la no conformidad
Ahora debemos revisar la no conformidad, para saber qué requisito no se cumplió o dónde no fue suficiente el control de riesgos. En este apartado, se redacta la no conformidad de una manera objetiva y clara (__redacción__), también es posible ampliar los datos en un campo llamado (__declaración__) para agregar información que ayude a comprender la no conformidad. Se indican las evidencias objetivas que nos llevaron a tomar la decisión de levantar la no conformidad (__evidencias__). Indicamos también el requisito que se incumplío y por último, debemos indicar si hemos tenido alguna no conformidad similar o relacionada, para saber mejor qué está pasando.

```python
    # #################################### #
    # II. Revisión
    redaccion = HTMLField(default='', blank=True, null=True)
    declaracion = HTMLField(default='', blank=True, null=True)
    evidencia = HTMLField(default='', blank=True, null=True)
    requisitos = HTMLField(default='', blank=True, null=True)
    relacionadas = HTMLField(default='', blank=True, null=True)
```

#### III. Responsabilidades
Este apartado es completamente opcional. En mi opinión no es necesario, pero es un requisito de los usuarios del sistema. Indica quienes son los responsables de ejecutar el plan, de revisarlo y darle seguimiento... algo que se repite en las acciones, por cierto.

```python
    # #################################### #
    # III. Responsabilidades
    informacion = models.CharField(max_length=30, blank=True, null=True)
    aplicacion = models.CharField(max_length=30, blank=True, null=True)
    responsable = models.CharField(max_length=30, blank=True, null=True)
```

#### IV. Reacción
Cuando se declara una no conformidad debemos _reaccionar_ sin demora injustificada. Debemos tomar las medidas, por medio de acciones correctivas, para contener la no conformidad (algunas veces no se podrá eliminar) y, si es necesario, hacer frente a las consecuencias.

```python
# #################################### #
    # IV. Reacción
    correccion = HTMLField(default="", blank=True, null=True)
    consecuencias = models.FileField(blank=True, null=True)
    reaccion_responsable = models.ForeignKey(
        Pipol, blank=True, null=True)
    reaccion_evidencia = models.FileField(blank=True, null=True)
```

#### V. Determinación de las causas
Una vez contenida la no conformidad, debemos analizar la declaración de no conformidad así como las evidencias presentadas. El objetivo es determinar la causa, de modo que podamos eliminarla (o reducir la probabilidad que ocurra de nuevo).

Para este análisis es preferible hacerlo con datos estadísticos que den certeza a nuestras decisiones, aunque también podemos usar otras técnicas como la «Causa y Efecto», lluvia de ideas, cinco porques. El objetivo es encontrar la causa que origina la no conformidad (o el riesgo) y tomar medidas para eliminarla o controlarla hasta niveles aceptables.

```python
    # #################################### #
    # V. Determinación de las Causas
    pescadito = models.FileField(blank=True, null=True)
    cincopq = models.FileField('5 Por qués', blank=True, null=True)
    causa_raiz = HTMLField(default='', blank=True, null=True)
```

#### VI. Determinación de acciones
Según el flujo del proceso definido por la norma, después de determinas las acciones necesarias para eliminar las causas que originan la no conformidad y verificar la eficacia de estas acciones.

En esta aplicación tanto las acciones como el seguimiento a las mismas tienen su propio modelo, que se relacionan en cascada, es decir, el modelo de seguimiento está relacionado con el modelo de acciones que a su vez está relacionado con el modelo de plan.

En el siguiente artículo veremos estos dos módulos.

#### VII. Cierre
El apartado dedicado al cierre del plan es, en realidad, para compatibilidad con el procedimiento anterior. Tiene campos para indicar si se eliminó la causa raíz o si hay recurrencia y otros campos para alguna aclaración que sea pertinente. Pero en general, el plan de acción puede considerarse cerrado con base en la evidencia del seguimiento a las acciones.


```python
    # #################################### #
    # VIII. Cierre
    eliminacion = models.BooleanField(default=False)
    txt_eliminacion = HTMLField(blank=True, null=True)
    recurrencia = models.BooleanField(default=False)
    txt_recuerrencia = HTMLField(blank=True, null=True)
```

### Conclusión

Este es el modelo para los planes de acción. Parecen muchos campos, pero la idea es llenarlos conforme vaya ejecutándose el proceso de cierre de la no conformidad. Por eso la mayoría está marcado como `null`, para usarlos solo cuando tengamos información.

Este plan es la base del proceso, pero la verdadera magia ocurre con los modelos relacionados, como veremos en el artículo siguiente.