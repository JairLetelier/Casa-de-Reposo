#!/usr/bin/env bash
set -o errexit

# 1. INSTALACIÓN (Necesaria para los pasos 3 y 4)
pip install -r requirements.txt

# 2. ESTÁTICOS (Necesaria para que la página de login tenga estilos)
python manage.py collectstatic --no-input

# 3. MIGRACIONES (Necesaria para que las tablas de usuario existan)
python manage.py migrate --no-input

# 4. CREACIÓN DEL SUPERUSUARIO (Debe ser el último)
python create_admin_on_startup.py