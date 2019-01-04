Title: El paradigma de modelos conductuales en Django    
Date: 2017-03-31 09:17:44
Category: desarrollo
Tags: django, patterns, 
Status: draft
Summary: 

Conforme los proyectos de Django aumentan en complejidad y escapan del nivel de los tutoriales, ¿cómo podemos estructurar nuestros proyectos para mantenerlos manejables? Estamos hablando de decenas hasta cientos de modelos, que usan numerosas vistas, plantillas y pruebas. Tan solo la aplicación de `metas` tiene unos 50 modelos por año en el 2017. 

El paradigma de *modelos compuestos* nos permite manejar la complejidad de los modelos separando su funcionalidad en componentes manejables. 

### Beneficios de los modelos robustos
- Encapsulamiento,
- Rutas únicas,
- Separación de responsabilidades

