#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Instala dependencias
pip install -r requirements.txt

# 2. Recopila estáticos
python manage.py collectstatic --no-input

# 3. Migra la base de datos (CREA LAS TABLAS)
python manage.py migrate --no-input

# 4. CREAR SUPERUSUARIO CON VARIABLES DE ENTORNO (Reemplaza el loaddata)
python create_admin_on_startup.py