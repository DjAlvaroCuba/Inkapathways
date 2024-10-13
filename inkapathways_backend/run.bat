@echo off

REM 
if not exist venv (
    echo Creando entorno virtual...
    python -m venv venv
    call venv\Scripts\activate
    echo Instalando dependencias...
    pip install -r requirements.txt
) else (
    echo Activando entorno virtual...
    call venv\Scripts\activate
)

echo Iniciando servidor Django...
python manage.py runserver

pause
