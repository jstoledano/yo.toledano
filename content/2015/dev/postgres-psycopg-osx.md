Title: PostgreSQL y Python en Mac OSX usando PsycoPG2  
Date: 2015-02-23 10:57:09  
Category: Desarrollo  
Tags:  osx, pip, postgresql, python  
Author: Javier Sanchez Toledano
Summary:  Cómo utilizar PostgreSQL y Python en Mac OSX usando PsycoPG2  

Se me ocurrió utilizar un conjunto de paquetes comunes en los entornos virtuales que utilizo en mis proyectos de trabajo y personales, como `iPython` y `PsycoPG2`, para no tener que instalarlos una y otra vez en cada entorno y tal vez ahorrar algo de espacio y tiempo.

No tuve ningún problema con la mayoría de los paquetes, pero compilar `psycopg` el driver para PostgreSQL resultó ser un problema al principio y afortunadamente muy fácil de resolver.

La solución consiste en usar la mejor versión que existe de este administrador de base de datos: [**Postgres.app**](http://postgresapp.com) que es un paquete que contiene todo lo necesario para trabajar, instalarlo es tan simple como arrastrar el paquete y para configurarlo, solo hace falta hacer clic en el icono del elefantito.

Ahora solo tenemos que ejecutar `pip` e indicar la ruta de los ejecutables de Postgres.app y esperar a que se instale el paquete.

    sudo PATH=$PATH:/Applications/Postgres.app/Contents/Versions/9.4/bin pip install psycopg2

