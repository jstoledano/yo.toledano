Title: Agrupar resultados con MySQL
Date: 2013/11/18 19:03
Category: Desarrollo 
Tags: mysql, sql 
Slug: agrupar-resultados-con-mysql
Author: Javier Sanchez Toledano
Summary: 

Una tarea muy común es obtener un total de una consulta que “agrupe” los resultados; es decir, que nos de, por ejemplo, el resultado de sumar las ventas de una companía y que este resultado sea mostrado por vendedor.

Para obtener este resultado, debemos usar `GROUP BY` en nuestra consulta.

    :::sql
    SELECT vendendor, SUM(ventas) 
    FROM tblVentas
    GROUP BY vendedor

Es necesario que el campo que usamos para agrupar se muestre en el conjunto de resultados. En este ejemplo, el campo es `vendedor`.

Y podemos usar funciones para agrupar los resultados. Por ejemplo, para saber cuántos alumnos nacieron en cada año, usando su CURP, podemos usar la función `SUBSTRING`, de esta manera:

    :::SQL
    SELECT SUBSTRING(curp, 6,6) as ANIO, COUNT(curp)
    FROM tblAlumnos
    GROUP BY SUBSTRING(curp, 6,6)

La consulta puede ser mas compleja y puede abarcar varias tablas o usar otro tipo de criterios, ya de ordenación o de selección. Pero esa es la idea básica.
