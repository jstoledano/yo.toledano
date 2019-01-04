Title: Cómo instalar Docker en OS X
Date: 2015-05-08 20:29:36
Category: Desarrollo
Tags:  docker, admin, osx
Author: Javier Sanchez Toledano
Summary: Cómo instalar docker en Mac OS X fácil y rápido.

Ya que en agosto cambiaremos de infraestructura para pasar todos los sitios a Amazon EC2, además ante el escenario de implementar el Cuadro de Mando Integral a nivel nacional, para ser más competitivo he resuelto utilizar Docker.

Para para poder trabajar en mi laptop, esta es la forma fácil de instalarlo.

## Instalar Homebrew

**Homebrew** es un instalador de paquetes y programas para OS X, tiene miles de paquetes llamadas _fórmulas_ y tenemos que instalar las siguientes primero.

```bash
ruby -e "$(curl -fsSL https://raw.github.com/Homebrew/homebrew/go/install)"
```

## Instalar Virtualbox

Con Homebrew podemos instalar ***VirtualBox** que es una máquina virtual. Usamos la fórmula `cask` porque no debemos usar, por razones de seguridad, usar `sudo` junto con `brew`.

```bash
brew update
brew tap phinze/homebrew-cask
brew install brew-cask
brew cask install virtualbox
```

## Instalar boot2docker 

`boot2docker` es un pequeño script que nos sirve de interface entre Docker y VirtualBox. Debemos ejecutar estos comandos:

```bash
brew install boot2docker
boot2docker init
boot2docker up
```

Al finalizar nos debe indicar que agreguemos algunas variables a nuestro archivo de arranque:

```bash
To connect the Docker client to the Docker daemon, please set:
    export DOCKER_HOST=tcp://192.168.59.103:2376
    export DOCKER_CERT_PATH=/Users/toledano/.boot2docker/certs/boot2docker-vm
    export DOCKER_TLS_VERIFY=1
```

## Instalar Docker

Por último el motor de contenedores, `docker` que se instala de forma muy sencilla.

```bash
brew install docker
docker version
```

Eso es todo. Sigo aprendiendo a usar esta herramienta y pronto publicaré más experiencias.

