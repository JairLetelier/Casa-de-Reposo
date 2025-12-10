# Global/urls.py

from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.views.static import serve
# Importamos las vistas de nuestra aplicación principal
from CasaReposo import views 


urlpatterns = [
    # ------------------------------------
    # Rutas de Administración de Django
    # ------------------------------------
    path('admin/', admin.site.urls),
    
    # ------------------------------------
    # RUTAS PÚBLICAS DEL SITIO WEB
    # ------------------------------------
    path('', views.index_view, name='index'), 
    path('nosotros/', views.nosotros_view, name='nosotros'), 
    path('servicios/', views.servicios_view, name='servicios'), 
    path('tarifas/', views.tarifas_view, name='tarifas'), 
    path('galeria/', views.galeria_view, name='galeria'), 
    path('contacto/', views.contacto_base_view, name='contacto'), 
    
    # ✅ RUTA CLAVE PARA EL ENVÍO DEL FORMULARIO
    path('contacto/formulario_contacto/', views.contacto_form_view, name='formulario_contacto'), 
    
    # ------------------------------------
    # RUTAS DE ADMINISTRACIÓN
    # ------------------------------------
    path('login/', views.login_view, name='login'), 
    path('logout/', views.logout_view, name='logout'), 
    
    # Panel de Administración
    path('panel-admin/', views.panel_admin_view, name='panel_admin'), 
    
    # Subida de imágenes
    path('upload/', views.upload_image_view, name='upload_image'), 
]

# ----------------------------------------------------------------------
# ⚙️ CONFIGURACIÓN DE MEDIA Y DEBUG (PARA DESARROLLO)
# ----------------------------------------------------------------------
if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        })
    ]