Title: Buscar y reemplazar con Vim
Date: 2013/11/18 19:06
Category: Desarrollo 
Tags: editores, tools 
Slug: buscar-y-reemplazar-con-vim
Author: Javier Sanchez Toledano
Summary: 

<p><a href="http://www.vim.org/">Vim</a> es uno de los mejores editores que existen. Es tan bueno que muchos editores lo usan. Y es uno de los pocos que puedes manejar a través de un enlace telefónico.</p>

<p>Bueno, el caso es que este es el procedimiento para buscar un texto y reemplazarlo por otro:</p>

    :%s/antes/después/g

<p>Reemplaza <code>antes</code> por <code>después</code>, la <code>g</code> es necesaria para sustituya en todo el documento.</p>

    :%s/antes/después/gc
