Title: Planes de Acción y Seguimiento
Date: 2015-08-09 12:47:12 a.m.
Category: Calidad
Tags:  iso, 9001:2015
Author: Javier Sanchez Toledano
Summary: Cómo desarrollar una aplicación en Django para controlar los planes de acción y seguimiento según la norma ISO 9001:2015.


El enfoque basado en procesos utilizado en los sistemas de gestión de la calidad,  la comprensión y el cumplimiento de los requisitos, la necesidad de considerar los procesos en términos que aporten valor, la obtención de resultados del desempeño y eficacia del proceso, y la mejora continua de los procesos con base en mediciones objetivas, 

El mismo sistema de gestión de la calidad o SGC tiene como propósito demostrar que nuestro producto/servicio cumple con los requisitos y que obtenemos los resultados planificados. 

El control de planes de acción y seguimiento que propongo ahora, cumple con los requisitos de la normas ISO 2001:2015 principalmente y se mantendrá la compatibilidad con la norma ISO 2001:2008 hasta donde sea posible (y alcancen los recursos).

La norma ISO 9001:2015 establece dentro de los requisitos generales que debemos determinar los procesos necesarios para el sistema de gestión de la calidad y su aplicación a través de la organización, y debemos determinar:

1. los elementos de entrada requeridos y los elementos de salida esperados de estos procesos;
1. la secuencia e interacción de estos procesos;
1. los criterios, métodos, incluyendo las mediciones y los indicadores del desempeño relacionados, necesarios para asegurarse la operación eficaz y el control de estos procesos;
1. los recursos necesarios y asegurarse de su disponibilidad;
1. la asignación de las responsabilidades y autoridades para estos procesos;
1. los riesgos y oportunidades de acuerdo con los requisitos del apartado 6.1, y planificar e implementar las acciones adecuadas para tratarlos;
1. los métodos para realizar el seguimiento, mediciones, cuando sea apropiado, y evaluación de los procesos y, si es necesario, los cambios en los procesos para asegurarse de que se logran los resultados previstos;
1. oportunidades de mejora de los procesos y del sistema de gestión de la calidad.

El control de los planes de acción y seguimiento que vamos a desarrollar está ligado a este último punto, **la mejora**, que en la norma 9001:2015 se referencia como el punto 10 y en la versión 2008 como el punto 8.

## Los Planes de Acción
Debemos determinar y planificar las oportunidades de mejora e implementar las acciones necesarias para llevar a cabo estas mejoras y lo hacemos con **planes de acción**.

Los planes de acción pueden ser _reactivos_ cuando se trata de no conformidades; *incrementales* cuando se trata de mejora continua; *creativos* cuando se trata de innovación o *por reorganización* si hablamos de transformación.

Considero que todos los planes de acción cuentan con los mismos elementos, asi que usaré mi experiencia en planes de acción reactivos para hacer esta propuesta.

### No conformidades

Para empezar, revisemos los requisitos de la norma con respecto a las no conformidades.

#### 10.2.1 No conformidad
Cuando ocurra una no conformidad, incluidas aquellas originadas por quejas, la organización debe:

1. reaccionar ante la no conformidad, y según sea aplicable
    1. tomar acciones para controlarla y corregirla;
    1. hacer frente a las consecuencias;
1. evaluar la necesidad de acciones para eliminar las causas de la no conformidad, con el fin de que no vuelva a ocurrir ni ocurra en otra parte, mediante:
    1. la revisión de la no conformidad;
    1. la determinación de las causas de la no conformidad;
    1. la determinación de si existen no conformidades similares, o que potencialmente podrían ocurrir;
1. implementar cualquier acción necesaria;
1. revisar la eficacia de las acciones correctivas tomadas;
1. si es necesario, hacer cambios al sistema de gestión de la calidad.

Las acciones correctivas deben ser adecuadas a los efectos de las no conformidades encontradas.

>
__NOTA 1__       En algunos casos, puede ser imposible eliminar la causa de una no conformidad.
>
**NOTA 2** La acción correctiva puede reducir la probabilidad de recurrencia a un nivel aceptable.


Tomo nota que 

* **primero**, una queja no es igual a una no conformidad, sino que las quejas pueden originar no conformidades y
* **segundo**, las acciones correctivas no tienen porque necesariamente eliminar la recurrencia, pero debemos demostrar que se reduce la posibilidad de que vuelva a aparecer.

#### 10.2.2 Documentación de No Conformidades

La organización debe conservar información documentada, como evidencia de:

1. la naturaleza de las no conformidades y cualquier acción posterior tomada;
1. los resultados de cualquier acción correctiva.

Las diferencias que existen con respecto a la versión 2008 se deben a que se agruparon los requisitos, pero básicamente es lo mismo.

## Modelo de Plan de Acción en Django
Ahora veamos como será el plan de acción en Django. Tenemos que cumplir con los requisitos del punto 10.2.1/8.5.2[^1], aunque no sé como documentar eso de _"hacer frente a las consecuencias"_, pero bueno.

[^1]: Para evitar la fatiga, cuando me refiera a un punto de la norma, utilizaré la siguiente sintaxis: primero el punto en la norma ISO 9001:2015, una diagonal y por último, el punto de la norma que corresponda a la versión 9001:2008. Cuando no exista la correspondencia usaré `N/A` en donde corresponda. 
op`


