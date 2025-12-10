#!/usr/bin/env bash
set -o errexit

# Intenta imprimir una línea y luego ejecutar el script de forma independiente
echo "--- INICIANDO PRUEBA DE ADMIN SCRIPT ---"
python create_admin_on_startup.py

# Luego ejecuta los comandos normales
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate --no-input