Title: Mixins en LESS    
Date: 2015-09-27 2:10:35 p.m.
Category: desarrollo
Tags:  
Summary: 

LESS es un pre-procesador de hojas de estilo que permite editarlas de forma muy rápida,y como dicen ahora, de forma muy semántica, es decir, de forma lógica que se explica de forma clara por si misma.

Agrupa los elementos, de forma que se encadenan fácilmente, lo que ahorra tiempo y disminuye la posibilidad de errores. Adicionalmente se pueden programar funciones que nos permiten utilizar de forma muy eficiente grupos de propiedades, sin repeticiones y sin errores. Estos se llaman **mixins**.

## Mixins

Uno de los estilos que más me gusta es agregar esquinas redondeadas a las imágenes, a las cajas y a todo lo que tenga borde.

En LESS es muy fácil crear un _mixin_ y luego usarlo en cualquier estilo. Incluso, puedo pasarle como parámetro el del número de pixeles que debe tener el radio de las esquinas.

Este es el _mixin_:

```less
.redondear (@radio: 5px) {
    -webkit-border-radius: @radio;
    -moz-border-radius:    @radio;
    border-radius:         @radio;

    -moz-background-clip:    padding;
    -webkit-background-clip: padding-box;
    background-clip:         padding-box;
}
``` 

Toma como parámetro el `@radio` y luego se aplica a todos los elementos que generan los bordes redondeados.

Y se usa de la siguiente manera:

```less
.xeMusicPlayer3 {
  .xeCover {
    img {
      margin: 0;
      padding: 0;
      max-height: 70px;
      max-width: 70px;
      .redondear();
    }
  }
  
  .xeMusicHeaderText {
      line-height: 1em;
  }
}
```

Como mantengo los `5px` de radio, no necesito especificar un valor diferente, aunque podría usarlo de esta manera `.redondear(3px)`. 

Al compilarlo, obtenemos una limpia hoja de estilo. Este es el resultado.

```css
.xeMusicPlayer3 .xeCover img {
  margin: 0;
  padding: 0;
  max-height: 70px;
  max-width: 70px;
  -webkit-border-radius: 3px;
  -moz-border-radius: 3px;
  border-radius: 3px;
  -moz-background-clip: padding;
  -webkit-background-clip: padding-box;
  background-clip: padding-box;
}
.xeMusicPlayer3 .xeMusicHeaderText {
  line-height: 1em;
}
```
