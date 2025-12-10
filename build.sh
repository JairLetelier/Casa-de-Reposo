#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# CORRECCIÓN: --no-input sin espacio
python manage.py collectstatic --no-input
python manage.py migrate