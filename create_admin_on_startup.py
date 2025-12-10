# create_admin_on_startup.py

import os
import django
from django.contrib.auth import get_user_model
from django.db.utils import ProgrammingError

# IMPORTANTE: Asegúrate de que 'Global.settings' es la ruta correcta
# para tu archivo settings.py.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Global.settings') 

# Intenta configurar Django. Puede fallar si la base de datos no está lista
# (por ejemplo, si se ejecuta antes de la migración), pero el script 
# en el build se ejecuta *después* de 'migrate', lo que minimiza el riesgo.
try:
    django.setup()
except Exception as e:
    # Esto es un caso de fallo para la configuración de Django.
    # Puede ser útil en la depuración, pero no debería ocurrir post-migrate.
    print(f"ERROR: Fallo al configurar Django. Mensaje: {e}")
    exit(1)

# Credenciales leídas de las Variables de Entorno de Render
# Usando el nombre del establecimiento guardado para el mensaje de bienvenida.
USERNAME = os.environ.get('DJANGO_SUPERUSER_USERNAME')

PASSWORD = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

# Si las variables de entorno están definidas, intentamos crear el usuario.
if USERNAME and PASSWORD:
    print('--- Iniciando intento de Creación de Superusuario Automático ---')
    try:
        User = get_user_model()
        
        # 1. Comprobamos si el usuario ya existe.
        if not User.objects.filter(username=USERNAME).exists():
            # 2. Si no existe, lo creamos.
            User.objects.create_superuser(USERNAME, PASSWORD)
            
            # Usando la información de tu Casa de Reposo:
            print(f'✅ Superusuario "{USERNAME}" para Casa de Reposo “Mi Hogar” creado exitosamente.')
            print(f'   Utiliza estas credenciales para acceder al administrador de Jazzmin.')
        else:
            print(f'ℹ️ Superusuario "{USERNAME}" ya existe. Saltando creación en este despliegue.')

    except ProgrammingError as pe:
        # Esto ocurre si la tabla de usuarios aún no se ha creado (aunque no debería si 
        # el build script está ordenado correctamente).
        print(f'❌ ERROR: La tabla de usuarios no existe o no es accesible (ProgrammingError). Asegúrate de que python manage.py migrate se ejecutó primero. {pe}')
    except Exception as e:
        # Manejo de cualquier otro error genérico durante la creación
        print(f'❌ ERROR Inesperado: Fallo al crear el superusuario. {e}')

else:
    print('⚠️ ADVERTENCIA: Faltan las variables DJANGO_SUPERUSER_* en el entorno de Render. No se intentó crear el superusuario.')