# camina-lector-lib
Utileria para leer los pdfs

# Prerequisitos

## Instalar pyenv
##### Sirve para instalar diferentes versiones de Python en tu computadora
```bash
pip install pyenv-win --target %USERPROFILE%\\.pyenv
```
### Setear variables del sistema en PowerShell
```bash 
[System.Environment]::SetEnvironmentVariable('PYENV',$env:USERPROFILE + "\.pyenv\pyenv-win\","User")

[System.Environment]::SetEnvironmentVariable('PYENV_ROOT',$env:USERPROFILE + "\.pyenv\pyenv-win\","User")

[System.Environment]::SetEnvironmentVariable('PYENV_HOME',$env:USERPROFILE + "\.pyenv\pyenv-win\","User")

[System.Environment]::SetEnvironmentVariable('path', $env:USERPROFILE + "\.pyenv\pyenv-win\bin;" + $env:USERPROFILE + "\.pyenv\pyenv-win\shims;" + [System.Environment]::GetEnvironmentVariable('path', "User"),"User")
```
### Ver versiones de Python que se pueden instalar
```bash
pyenv install -l
```
### Ver versiones de Python instaladas
```bash
pyenv versions
```
### Instalar una version de Python en pyenv
```bash
pyenv install 3.12.0
```
### Cambiarse a una version de Python instalada
```bash
pyenv shell 3.12.0
```

## Instalar pipx 
##### Está pensado para instalar aplicaciones en tu usuario, no a nivel de sistema
### Abrir consola de windows como admistrador
```bash
pip install --user pipx
python -m pipx ensurepath
```
## Instalar poetry
##### Te ayuda a declarar, administrar e instalar dependencias de Python
```bash
pipx install poetry==1.6.1
```
### Crear entorno virtual del proyecto
##### Prerequisito clonar  el proyecto camina-lector-lib de github
### Navegar en la consola de windows sobre la carpeta clonada 
```bash
cd C:\projects\camina-lector-lib
```
### Ejecutamos el siguiente comando
```bash
 python -m pyenv venv
```
### Activar entorno virtual
```bash
.\venv\Scripts\activate.bat
```
## Instalar Librerias del Proyecto
```bash
poetry install
```
## Instalar Una Librerias en especifico al Proyecto
```bash
poetry add nombre-libreria
```

## Abrir Proyecto en Visual Code
```bash
code .
```

## License
[MIT](https://choosealicense.com/licenses/mit/
