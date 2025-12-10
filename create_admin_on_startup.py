# create_admin_on_startup.py (SOLUCIÓN DE RESETEO FORZADO)

import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Global.settings') 
try:
    django.setup()
except Exception as e:
    print(f"ERROR: Fallo al configurar Django. Mensaje: {e}")
    exit(1)

USERNAME = os.environ.get('DJANGO_SUPERUSER_USERNAME')
PASSWORD = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
# Usamos un email vacío ('') para cumplir con la firma de create_superuser
EMAIL = os.environ.get('DJANGO_SUPERUSER_EMAIL', '') 


if USERNAME and PASSWORD:
    print('--- Iniciando Operación de Reseteo/Creación de Superusuario ---')
    try:
        User = get_user_model()
        
        # 1. Obtenemos o creamos el usuario. Pasamos EMAIL para cumplir con el modelo base.
        # Si el usuario ya existe (ej. 'admin'), lo obtiene. Si no, lo crea.
        user, created = User.objects.get_or_create(
            username=USERNAME, 
            defaults={'email': EMAIL, 'is_staff': True, 'is_superuser': True}
        )
        
        # 2. **Paso Clave:** Reseteamos la contraseña con la variable de entorno
        user.set_password(PASSWORD) 
        user.save()

        if created:
            # Usando la información de tu Casa de Reposo:
            print(f'✅ Superusuario "{USERNAME}" para Casa de Reposo “Mi Hogar” creado exitosamente.')
        else:
            print(f'🔄 Superusuario "{USERNAME}" ya existía. Contraseña RESETEADA exitosamente.')
            
    except Exception as e:
        print(f'❌ ERROR Inesperado durante la creación/reseteo: {e}')

else:
    print('⚠️ ADVERTENCIA: Faltan las variables DJANGO_SUPERUSER_USERNAME o DJANGO_SUPERUSER_PASSWORD en Render.')