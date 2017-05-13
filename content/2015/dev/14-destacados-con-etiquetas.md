Title: Destacados con etiquetas
Date: 2013/11/20 17:47
Category: Desarrollo
Tags: php, wp_query, wordpress
Slug: destacados-con-etiquetas
Author: Javier Sanchez Toledano
Summary:

Desde hace mucho quería saber como hacer que un post se destacara de alguna manera sin tener que asignarle una categoría especia, sino con etiquetas, claro que es mas difícil que en WordPress, pero si se puede.

Esta es la forma.

```php
<?php $starred = new WP_Query('tag=star&showposts=2'); ?>
  <?php if ($starred->have_posts()) : ?>
    <?php while ($starred->have_posts()) : $starred->the_post(); ?>
      <h4><?php the_title(); ?></h4>
      <?php the_content(); ?>
    <?php endwhile; ?>
  <?php else : ?>
<?php endif; ?>
```

Es importante usar `WP_Query` para evitar conflictos con el *loop* principal.
