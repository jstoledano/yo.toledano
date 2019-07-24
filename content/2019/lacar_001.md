Title: Creando un sitio de videotutoriales   
Date: 2019-07-02 18:07:52
Category: desarrollo
Tags: django, python, video, 100DaysOfCode
Summary: Estoy  creando  un proyecto  dentro  del  reto de  100 días  de código  que consiste  en  crear un  clon Udemy  para capacitación en mi trabajo.

# Antecedentes

Existe un reto llamado __100 días de código__ que consiste en
programar todos  los días durante  una hora, para  aprender un
nuevo lenguaje  o para  mejorar alguno ya  conocido. Como tengo
mucho  que  aprender de  Django,  he  decidido crear  un  nuevo
proyecto y trabajar en él durante 100 días.

# Requisitos

El proyecto  se llama __LACar__  que son las siglas  para _Loca
Academia de Cartografía_  y es una especie de clon  de Udemy o
esas plataformas de capacitación por videos. Veamos si podemos
establecer  las  características  iniciales  que  va  a  tener
_LACar_.

- Tiene dos  tipos de usuarios: maestros y  alumnos, unos suben
los cursos, otros se inscriben a estos cursos.
- Los maestros pueden crear, activar/desactivar o borrar cursos.
- Los  maestros pueden  agregar, borrar, modificar,  cambiar el
orden de las lecciones.
- Los alumnos y maestros pueden comentar cada lección.
- Los comentarios de los maestros están identificados.
- Los maestros y alumnos reciben una notificación cuando crean
un comentario a su curso o contestan un comentario.

Los cursos están compuestos por _n_ lecciones, generalmente en
video, pero también es posible  que tengan algún otro tipo de
recursos,  como  un PDF,  una  presentación  una plantilla  de
Geomedia, archivo Shape de Qgis, etc.

El  proyecto incluye  la parte  del servidor  o _backend_  y la
parte que se visualiza en el navegador o _frontend_.

# Frontend
La idea es que el frontend de una lección se vea así:

![Single View Lesson LACar](https://media.toledano.org/images/2019/single_videoLACAR.png)

Para el _frontend_ usaremos [Bootstrap 4.3.1](https://getbootstrap.com) ya que __LACar__ se integrará con el Cuadro de Mando Integral. La parte del encabezado y del pie de página no serán tratados en esta serie.

# Backend
Ahora bien, las claves de este  proyecto son los modelos de los
cursos, las lecciones. Y si queremos  que se registre el avance
de los alumnos, debemos enlazar a  los alumnos con los cursos y
lecciones.

El  curso  con  el  que  haremos las  pruebas,  tiene  unas  35
lecciones acomodadas en en  secciones, además, tiene dos tipos
de alumnos,  de Junta Local  o de las subdelegaciones  o juntas
distritales. Aunque no creo necesario bloquear el contenido.

![WBS Caso Complejo](https://media.toledano.org/images/2019/wbs_caso_complejo.png)

El curso  además tiene  dos lecciones de  apoyo, que  no forma
parte propiamente  del curso y algunos  recursos como formatos,
archivos de proyecto y de  _layout_ que tenemos que integrar al
curso.

# ReactJS
Creo que merece una mención aparte. El objetivo no solo es mejorar mi dominio de Django, sino también de [React](https://es.reactjs.org), así que vamos a integrar a Django y a React… o tal vez sea un proyecto independiente, en cuyo caso usaría [Django Rest Framework](https://www.django-rest-framework.org). Ya veremos.

El día de mañana empezaré con los modelos.