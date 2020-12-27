Title: Funciones repetitivas en R    
Date: 2020-07-04 
Category: Data Science
Tags: R, 

Para iniciar esta serie sobre las funciones _loop_ en __R__ vamos a usar un archivo que contiene los datos sobre la epidemia COVID-19 en Tlaxcala, que está disponible en este enlace. 

El archivo se ve de esta manera:

```
fecha, positivos, negativos, sospechosos, recuperados, defunciones
2020-07-01, 2541, 3565, 817, 1659, 367
2020-07-02, 2591, 3612, 873, 1659, 382
2020-07-03, 2668, 3701, 977, 1659, 389
```

Y sobre estos datos vamos a ejecutar las funciones _loop__ iniciando con la función __`lapply()`__.

Lo que hace esta función es que itera sobre una lista (de ahí viene la `l`, de _lista_), creando un ciclo para cada elemento de esa lista; aplica la función especificada a cada elemento; por último, regresa una lista. El propotipo de la función es el siguiente:

```R
lapply(x, función, ...)
```

El primer argumento es una lista `x`; el segundo `función` es el nombre de la función que se va a aplicar y el tercer argumento, `...` son otros argumentos que se van a pasar `función`. Si `x` no es una lista, se transformará en una usando la función `as.list()`. 

Algo importante a tener en cuenta es que la función `lapply()` siempre regresa una lista, sin importar el tipo de entrada que reciba.

La funciones `*apply()` (`lapply`, `sapply`, `mapply`, `vapply` y `tapply`) ofrecen una forma muy conveniente de implementar estrategias de Dividir-Aplicar-Combinar para análisis de datos.

Cada una de estas funciones _dividen_ los datos en partes más pequeñas, se _aplica_ la función a cada pieza, luego se _combinan_ los resultados. Esta estrategía se definió en el documento _"The Split-Apply-Combine Strategy for Data Analysis"_ de Hadley Wickman publicado en el [Journal of Statistical Software](https://www.jstatsoft.org/article/view/v040i01).

