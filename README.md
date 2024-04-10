# FastAPI Template - Rework

<sub> Si estas viendo este archivo en VSCode, se veerá mejor si aplastas **`CTRL + SHIFT + P`** y buscas la opción **`Markdown: Open Preview`**, o ves el archivo en **`github.com`** </sub>

## Indice

-   [Pre-requisitos](#pre-requisitos)
-   [Pasos](#pasos)
    -   [Primeros pasos](#primeros-pasos)
    -   [Crear el entorno virtual (venv)](#crear-el-entorno-virtual-venv)
    -   [Ingresar al entorno virtual (venv)](#ingresar-al-entorno-virtual-venv)
    -   [Instalar las dependencias del proyecto](#instalar-las-dependencias-del-proyecto)
    -   [Correr el proyecto](#correr-el-proyecto)
-   [Preguntas frecuentes](#preguntas-frecuentes)
    -   [¿Como instalo un requirement nuevo al proyecto?](#como-instalo-un-requirement-nuevo-al-proyecto)

## Pre-requisitos

-   Python 3.10.x

## Pasos

### Primeros pasos

1. Clonar el repositorio.
1. Clonar el archivo **`.env.example`** y renombrarlo como **`.env`**.
1. No es necesario configurar el nuevo **`.env`**, ya que esta pre-configurado, así como viene asi debería funcionar perfectamente.
1. [Crear el entorno virtual (venv)](#crear-el-entorno-virtual-venv)
1. [Ingresar al entorno virtual (venv)](#ingresar-al-entorno-virtual-venv)
1. [Crear migraciones con `alembic`](#crear-migraciones-con-alembic)
1. [Aplicar migraciones con `alembic`](#aplicar-migraciones-con-alembic)
1. [Correr el proyecto](#correr-proyecto)
1. La documentación se debera poder ver en http://localhost:8000/docs (Este comando difiere dependiendo en que puerto lo decidiste desplegar)

### Crear el entorno virtual (venv)

El **venv** _(entorno virtual)_ es un pequeño espacio aislado donde el desarrollador puede instalar las dependencias del proyecto.
Las dependencias instaladas dentro de un **venv** no estaran disponibles en otro **venv**, ni fuera del **venv**.

Para crear un **venv** deberas escribir el siguiente comando:

```bash
python3 -m venv venv
```

> **NOTA:** El comando `python3` difiere entre las instalaciónes de todos los desarrolladores, podria ser `python`, `python3`, `python310`, etc. En dado caso de que falle, intentar experimentando con los demas comandos.

Proximamente, [deberas ingresar al entorno virtual](#ingresar-al-entorno-virtual-venv) y [instalar las dependencias del proyecto](#instalar-las-dependencias-del-proyecto).

### Ingresar al entorno virtual (venv)

Para ingresar al **venv** previamente [debera estar creado](#crear-el-entorno-virtual-venv), y despues correr el siguiente comando:

> **NOTA:** Recomiendo que aplastes **`TAB`** mientras <u>escribes las rutas</u> para que se auto-completen.

```bash
# Si estas en Windows es:
.\venv\Scripts\activate.ps1

# Si estas en Linux/OSX es:
. venv/bin/activate
```

Una vez ingresado, notaras que estará un prefijo **`"(venv)"`** hasta la izquierda tu pantalla indicandote que estas dentro del **`venv`**.

### Instalar las dependencias del proyecto

[Una vez ingresado al entorno virtual](#ingresar-al-entorno-virtual-venv) deberas correr el siguiente comando:

> **NOTA:** Recomiendo que aplastes **`TAB`** mientras <u>escribes el nombre del archivo</u> para que se auto-complete.

```bash
pip install -r requirements.txt
```

Una vez instalado, [ya podras correr el proyecto](#correr-el-proyecto).

### Crear migraciones con `alembic`

[Una vez ingresado al entorno virtual](#ingresar-al-entorno-virtual-venv) deberas correr el siguiente comando:

```bash
alembic revision --autogenerate -m "<nombre de la migración>"
```

### Aplicar migraciones con `alembic`

[Una vez ingresado al entorno virtual](#ingresar-al-entorno-virtual-venv) deberas correr el siguiente comando:

```bash
alembic upgrade head
```

### Correr el proyecto

[Una vez ingresado al entorno virtual](#ingresar-al-entorno-virtual-venv) deberas correr el siguiente comando:

```bash
# Correr en http://localhost:8000/
uvicorn main:app

# Personalizar el puerto en el que se despliega, ej. http://localhost:3000/
uvicorn main:app --port 8000
```

### pre-commit

Es una librería que se encarga de correr acciones antes de hacer un commit, en este caso, se encarga de correr los comandos de `flake8` y `black` para que el código sea más legible y tenga un estándar de código (linter).
El modulo `pre-commit` está agregado al proyecto para formatear el código antes de hacer un commit.
Una opción es instalar `pre-commit` de manera global en Python con el comando `pip install pre-commit` y otra opción es ejecutar la versión que está dentro del contenedor. (`pip install pre-commit`)
Para instalar `pre-commit` en el proyecto se debe ejecutar el comando `pre-commit install`.
Para formatear el código que está listo para hacer commit se debe ejecutar el comando `pre-commit run`.
Para formatear todos los archivos del proyecto se debe ejecutar el comando `pre-commit run --all-files`.

> **NOTA:** (antes de correr el comando run, se debe agregar los archivos al stage con git add .)

## Preguntas frecuentes

### ¿Como instalo un requirement nuevo al proyecto?

Para instalar un requirement nuevo, solamente agregas **MANUALMENTE** el requirement nuevo en el **`requirements.project.txt`** y [instalar los requirements.txt de nuevo](#instalar-las-dependencias-del-proyecto).
Sera necesario que una vez instalada la libreria escribas que versión fue la que se instaló, de las siguientes maneras:

-   Correr el comando **`pip freeze`** y copiar la version manualmente en **`requirements.project.txt`**
    > **Nota:** Ojo no copiar todas las librerias nuevas, solo copiar la libreria instalada, nisiquiera copiar las sub-librerias instaladas por la libreria recien agregada.
-   Buscar la libreria en [https://pypi.org/](https://pypi.org/project/) y copiar la ultima version de allí (ejemplo: <https://pypi.org/project/django-q/#history>).
-   Puedes ver el output de la terminal en el momento que se instalo y de ahi sacar la versión.
