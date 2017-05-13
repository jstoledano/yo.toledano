Title: Encapsulamiento y Generalización en Python
Date: 2013/11/20 16:28
Category: Desarrollo
Tags: patterns, python
Slug: encapsulamiento-y-generalizacion-en-python
Author: Javier Sanchez Toledano
Summary:

<p>El <strong>encapsulamiento</strong> es el proceso de envolver una pieza de c&oacute;digo en una funci&oacute;n, permiti&eacute;ndole tomar ventaja de todas las bondades de las funciones. Generalizar significa tomar algo espec&iacute;fico, como imprimir los m&uacute;ltiplos de 2, y hacerlo m&aacute;s general para imprimir los m&uacute;ltiplos de cualquier n&uacute;mero.</p>
<p>Por ejemplo si tenemos el siguiente ciclo en Python:</p>

```python
i = 1
while i &lt;= 6:
   print 2 * i, '\',
   i = i + 1
print
```

<p>La siguiente funci&oacute;n encapsula el ciclo anterior y lo generaliza para imprimir los m&uacute;ltipos de <code>n</code>:</p>

    :::Python
    def imprimeMultiplos(n):
        i = 1
        while i &lt;= 6:
            print n * i, '\',
            i = i + 1
        print

<p>Para <em>encapsularla</em>, todo lo que tuvimos que hacer fue agregar la primera linea, que declara el nombre de la funci&oacute;n y la lista de par&aacute;metros. Para <em>generalizar</em>, todo lo que tenemos que hacer es reemplazar el valor de 2 con el par&aacute;metro <code>n</code>.</p>
<p>Si llamamos a esta funci&oacute;n con el par&aacute;metro 2, obtenemos la misma salida que antes. Con el par&aacute;metro 3, la salida es la siguiente:</p>

    :::Python
    >>> imprimeMultiplos(3)
    3     6     9     12     15     18

<p>Con cuatro como argumento, la salida es esta:</p>

    :::python
    >>> imprimeMultiplos(4)
    4     8     12     16     20     24

<p>Seguramente ya habr&aacute;s adivinado como imprimir una tabla de multiplicar &mdash; llamando a <code>imprimeMultiplos</code> repetidamente con diferentes argumentos. De hecho, podemos usar otro ciclo:</p>


    :::python
    i = 1
    while i &lt;= 6:
        imprimeMultiplos (i)
        i = i + 1

<p>Observa que similar es este ciclo al que est&aacute; dentro de <code>imprimeMultiplos</code>. Todo lo que hicimos fue reemplazar el enunciado print con una llamada a la funci&oacute;n.</p>
<p>La salida de este programa es una tabla de multiplicar:</p>

    1   2   3   4   5   6
    2   4   6   8   10   12
    3   6   9   12   15   18
    4   8   12   16   20   24
    5   10   15   20   25   30
    6   12   18   24   30   36
