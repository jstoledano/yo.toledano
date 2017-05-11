Title: Uso de las etiquetas de autoría en Genesis  
Date: 2014/04/21 13:24  
Category: Desarrollo  
Tags: seo, genesiswp, hacks, wordpress
Summary: Como aprovechar las etiquetas de autoría de Googla para mejorar la presencia de nuestro sitio en los resultados de las búsquedas.


<p>Aunque esta característica ya tiene bastante tiempo no he visto que se muy utilizada, me refiero a las <b>etiquetas de Autoría</b>. Estas etiquetas permiten a las los autores identificar el contenido creado por ellas y ellos en la red<sup class="footnote"><a href="#fn4555e7ef-f402-4495-992b-f3da915fdb36">1</a></sup>. </p>

<p>Por ejemplo si un autor de algún diario escribe sus artículos usando esta etiqueta, su pueden conectar estos artículos con la página del autor. Una página de autor describe e identifica al autor y puede incluir su biografía, su foto, una lista de artículos, enlaces a otros sitios, etc<sup class="footnote"><a href="#fn57215f53-81da-430f-8d3a-b5743d08f27f">2</a></sup>.</p>

<p>La etiqueta de autoría es realmente muy simple, se trata únicamente de agregar <code>rel="author"</code> a los enlaces para permitirle a los motores de búsqueda la identificación de trabajos del mismo autor en toda la web. </p>

<p>Es importante que comprendas el impacto que esta etiqueta de autoría tendrá en las búsquedas que se realicen en Google. Con la <b>etiqueta de autoría</b> podrás:</p>

<ul>
		<li>Podrás hacer un análisis de las estadísticas<sup class="footnote"><a href="#fn4819b022-1478-4867-b1b6-49029ccd8133">3</a></sup> por autor.</li>
		<li>Podrás resaltar y diferenciar tus resultados en las búsquedas.</li>
		<li>Ganar más seguidores en Google+.</li>
		<li>Ayudar a tus usuarios a encontrar más de tus contenidos en la web.</li>
	</ul>

<h2>Cómo utilizar la etiqueta de autoría con Genesis Framework</h2>

<p>Este es un tutorial para utilizar la etiqueta de autoría con Genesis Framework.</p>

<h4>1. Necesitas un perfil de Google Plus</h4>

<p>Lo primero que necesitas es crear un perfil de Google Plus, y por supuesto, una cuenta de Google. Así que si no cuentas con una, puedes crearla en este enlace: <a href="http://j.mp/cyberia-googleplus">http://j.mp/cyberia-googleplus</a>.</p>

<p>A continuación debes crear un <a href="http://j.mp/cyberia-googleprofile">Perfil de Google+</a>, recuerda subir una buena foto para tu portada y comletar la información más relevante para tus clientes.</p>

<p>El último paso en esta sección, es verificar la autoría de tu obre a tu perfil de Google; simplemente visita esta página <a href="https://plus.google.com/authorship">https://plus.google.com/authorship</a>, escribe tu dirección de correo en la caja y regístrate. Recuerda que la dirección de correo debe ser del mismo dominio que el sitio del que reclamas la autoría<sup class="footnote"><a href="#fn4bdf5f67-510e-4503-801a-51c9b5a41103">4</a></sup>. </p>

<p><img src="http://cyberia.mx/media/Snap_2012.04.22-21.56.05_002-600x325.jpg" alt="." title="Snap_2012.04.22 21.56.05_002" width="600" height="325" class="aligncenter size-large wp-image-1262" /></p>

<p>Te envían un enlace a tu correo elctrónico y al seguirlo verificas tu correo y queda enlazado a tu perfil. Con esta operación Google te identificará como el autor cuando en tus páginas aparezca la etiqueta de autoría.</p>

<h4>2. Modificación del Perfil de WordPress</h4>

<p>En esta sección necesitas un pequeño <em>hack</em> (una modificación al comportamiento estándar de WordPress) en las páginas de perfil. WordPress permite que existan varios autores en un blog, por lo que esta modificación es una buena práctica que te ahorrará tiempo y estandarizará la información de tu sitio.</p>

<p>Primero debemos agregar un campo al perfil de los autores, WordPress carece de este campo, pero solo debes agregar el siguiente código a tu archivo <code>functions.php</code> para contar con esta información:</p>
  
<pre class="brush:php">
/* *** Agrega la URL de Google Profile al perfil del autor en WordPress *** */
add_filter( &#39;user_contactmethods&#39;, &#39;cyberia_google_profile&#39;, 10, 1);
function cyberia_google_profile( $contactmethods ) {
  // Add Google Profiles
  $contactmethods[&#39;google_profile&#39;] = &#39;Perfil de Google&#39;;
  return $contactmethods;
} 
</pre>

<p>Ahora aparecerá una nueva caja de datos en los métodos de contacto y se rellena con la <span class="caps">URL</span> del perfil de Google del autor.</p>

<p><img src="http://cyberia.mx/media/Snap_2012.04.22-22.52.57_003-600x329.jpg" alt="." title="Snap_2012.04.22 22.52.57_003" width="600" height="329" class="aligncenter size-large wp-image-1264" /></p>

<h4>Agregar la etiqueta de autoría a la información de los artículos</h4>

<p>El código para agregar la etiqueta de autoría puede parecer muy complicado al principio<sup class="footnote"><a href="#fn633da8f0-faf8-4dc6-9be3-902de323af80">5</a></sup>, pero vamos a diseccionar y analizar cada uno de sus componentes para entenderlo mejor. Primero veamos el código.</p>


<pre class="brush:php">/* *** Agregar Google Authorship ***  */
add_filter( &#39;genesis_post_info&#39;, &#39;cyberia_filtrar_info&#39; );
function cyberia_filtrar_info($post_info) {
  if (!is_page()) {
    $post_info = &#39;[ post_date] por [ post_author_posts_link]&#38;nbsp;&#60;a rel=&#34;me author&#34; href=&#34;&#39;. get_the_author_meta( &#39;google_profile&#39; ) .&#39;/about&#34;&#62;&#60;img class=&#34;plus&#34; src=&#34;http://cyberia.mx/images/gplus.png&#34; width=&#34;12&#34; height=&#34;12&#34; border=&#34;0&#34; align=&#34;&#34; alt=&#34;Google+&#34; title=&#34;Google+ Profile&#34;&#62;&#60;/a&#62; a las [ post_time] [ post_comments] [ post_edit]&#39;;
    return $post_info;
  }
}
</pre>

<p>La primera línea agrega una función al filtro <code>genesis_info_post</code>. Esta función se llama <code>cyberia_filtrar_info</code> y recibe como argumento la información del post.</p>

<p>Este código es el que se usa en <b>Cyberia.MX</b>, por eso se ve en la línea 4 que solo funciona cuando NO se trata de páginas.</p>

<p>En la línea 5 cambiamos el <code>post_info</code> que nos mando la función con uno nuevo que nosotros especificamos. Los campos <code>post_date</code>, <code>post_author_posts_link</code>, <code>post_time</code>, <code>post_comments</code> y <code>post_edit</code> son atajos que proporciona <a href="/go/genesis"><b>Genesis Framework</b></a> pero agregamos este enlace clave:</p>

<pre class="brush:php,first-line:5">&#60;a rel=&#34;me author&#34; href=&#34;&#39;. get_the_author_meta( &#39;google_profile&#39; ) .&#39;/about&#34;&#62;&#60;img class=&#34;plus&#34; src=&#34;http://cyberia.mx/images/gplus.png&#34; width=&#34;12&#34; height=&#34;12&#34; border=&#34;0&#34; align=&#34;&#34; alt=&#34;Google+&#34; title=&#34;Google+ Profile&#34;&#62;&#60;/a&#62;
</pre>

<p>Como podrás ver, la función <code>get_the_author_meta('google_profile')</code> es la que se encarga de colocar la <span class="caps">URL</span> del perfil del autor y así formar el enlace. Un mini icóno completa este trabajo y hace el enlace un poco más notorio<sup class="footnote"><a href="#fn301804ea-3242-4829-83e5-1a74398bcaae">6</a></sup>.</p>

<h4>La Etiqueta de Autoría</h4>

<p>Este enlace contiene la <b>etiqueta de autoría</b> que es <code>rel="author"</code>. Esto es entonces un enlace a un sitio central verificado por Google, es decir nuestro perfil de Google Plus, donde verificamos la autoría de nuestros artículos y le damos más relevancia a los resultados de las búsquedas.</p>

<p>Esta etiqueta de autoría, <code>rel='author'</code> es parte de los fragmentos enriquecidos con microformatos que está promoviendo Google activamente, porque agregan información sobre nuestro artículo que entienden y aprovechan los buscadores.</p>

<h4>Prueba de la Etiqueta de Autoría y Microformatos</h4>

<p>Para verificar que has realizado todos los pasos correctamente, visita esta página <a href="http://www.google.com/webmasters/tools/richsnippets">http://www.google.com/webmasters/tools/richsnippets</a> y en la caja que aperece escribe la <span class="caps">URL</span> de tu sitio.</p>

<p><img src="http://cyberia.mx/media/Snap_2012.04.22-23.54.20_004-600x395.jpg" alt="." title="Snap_2012.04.22 23.54.20_004" width="600" height="395" class="aligncenter size-large wp-image-1265" /></p>

<p>Si quieres ver cómo debe verse usa esta página de Cyberia.MX: <a href="http://cyberia.mx/apps/angry-birds">Angry Birds</a> que no solamente tiene la etiqueta de autoría, también tiene microformatos que especifican la opinión de una aplicación.</p>

<p>Espero que te haya servido este tutorial para <a href="/go/genesis"><b>Genesis Framework</b></a> y las <b>Etiquetas de Autoría</b>.</p>

<hr />

<h3>Notas</h3>

<p id="fn4555e7ef-f402-4495-992b-f3da915fdb36" class="footnote"><sup>1</sup>Voy a trabajar en un proyecto sobre equidad de género y esto es para empezar a acostumbrarme.</p>

<p id="fn57215f53-81da-430f-8d3a-b5743d08f27f" class="footnote"><sup>2</sup>Puedes leer más sobre este tema en el blog <a href="http://j.mp/JGHIJb">Webmaster Central</a></p>

<p id="fn4819b022-1478-4867-b1b6-49029ccd8133" class="footnote"><sup>3</sup>El artículo se llama <a href="http://j.mp/I49XGE">Clics e impresiones por autor</a></p>

<p id="fn4bdf5f67-510e-4503-801a-51c9b5a41103" class="footnote"><sup>4</sup>En realidad, ignoro el por qué de esta demanda, pero si no tienes una dirección de correo, puedes usar un <a href="http://j.mp/JGRf2X">método alterno</a></p>

<p id="fn633da8f0-faf8-4dc6-9be3-902de323af80" class="footnote"><sup>5</sup>Los filtros para mi son muy complicados, pero sigo aprendiendo.</p>

<p id="fn301804ea-3242-4829-83e5-1a74398bcaae" class="footnote"><sup>6</sup>Aunque el color desentona con el tema de <strong>Cyberia.MX</strong> un poco #opino.</p>
