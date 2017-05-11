Title: Problemas al actualizar la versión de Ubuntu
Date: 2014/04/09 21:53
Category: Desarrollo
Tags: Ubuntu, linux, 
Summary: Como solucionar los problemas de codificación al actualizar la versión de Ubuntu

Con esto de los problemas de seguridad de __OpenSSL__ me dispuse a iniciar un nuevo proyecto con una VPS configurada con el sistema operativo más moderno o con Ubuntu 13.10, lo que encontrara primero.

Entonces, instalé la versión 13.04 y al ejecutar el comando `do_release_update` me aparece este error:


Ha ocurrido un error fatal 

	Error in sys.excepthook:
	Traceback (most recent call last):
	  File "/tmp/ubuntu-release-upgrader-6qqpqy/DistUpgrade/DistUpgradeViewText.py", line 107, in _handleException
	    "\n".join(lines))
	  File "/tmp/ubuntu-release-upgrader-6qqpqy/DistUpgrade/DistUpgradeViewText.py", line 142, in error
	    print(twrap(msg))
	UnicodeEncodeError: 'ascii' codec can't encode character u'\xf3' in position 139: ordinal not in range(128)

	Original exception was:
	Traceback (most recent call last):
	  File "/tmp/ubuntu-release-upgrader-6qqpqy/saucy", line 10, in <module>
	    sys.exit(main())
	  File "/tmp/ubuntu-release-upgrader-6qqpqy/DistUpgrade/DistUpgradeMain.py", line 230, in main
	    app = DistUpgradeController(view, options, datadir=options.datadir)
	  File "/tmp/ubuntu-release-upgrader-6qqpqy/DistUpgrade/DistUpgradeController.py", line 126, in __init__
	    self._view.updateStatus(_("Reading cache"))
	  File "/tmp/ubuntu-release-upgrader-6qqpqy/DistUpgrade/DistUpgradeViewText.py", line 121, in updateStatus
	    print(msg)
	UnicodeEncodeError: 'ascii' codec can't encode character u'\xe9' in position 15: ordinal not in range(128)
	=== Command detached from window (Thu Apr 10 03:53:05 2014) ===
	=== Command terminated with exit status 1 (Thu Apr 10 03:53:05 2014) ===

Esto se debe a un conflicto en la codificación. Mi terminal manda a la terminal de Linux mi configuración de `locales` y el comando de actualización al parecer solo funciona con `en_US`.

La solución es ejecutar este comando con una variable de entorno  que establesca la codificación `C`. Así:

	root@hydra:~# LC_ALL=C.UTF-8 do-release-upgrade

Con esto la actualización corre como el viento.
