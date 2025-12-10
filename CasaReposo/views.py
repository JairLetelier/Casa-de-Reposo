from django.shortcuts import render, redirect 
from django.contrib import messages 
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.forms import AuthenticationForm 
from django.urls import reverse # NECESARIO para redirigir al admin nativo
from django.core.mail import EmailMessage
import random 

# Importaciones de Modelos y Formularios
from .forms import ContactoCRMHForm 
from .models import (
    CarouselImage, RoomType, GalleryPhoto, 
    RateCategory, IncludedService, OptionalService,
    ContactMessage # Importación del modelo de mensajes de contacto
)

# ------------------------------------
# RUTAS PÚBLICAS DEL SITIO WEB
# ------------------------------------

def index_view(request):
    """Renderiza la página principal e inyecta las imágenes dinámicas del carrusel."""
    carousel_images = CarouselImage.objects.filter(is_active=True).order_by('order')
    
    context = {
        'carousel_images': carousel_images,
    }
    
    return render(request, 'index.html', context)

def nosotros_view(request):
    """Renderiza la página 'Nosotros'."""
    return render(request, 'nosotros.html', {})

def servicios_view(request):
    """Renderiza la página de 'Servicios'."""
    return render(request, 'servicios.html', {})

def tarifas_view(request):
    """
    Renderiza la página de 'Tarifas' e inyecta los datos dinámicos.
    """
    rate_categories = RateCategory.objects.filter(is_active=True).order_by('order')
    included_services = IncludedService.objects.filter(is_active=True).order_by('order')
    optional_services = OptionalService.objects.filter(is_active=True).order_by('order')
    
    context = {
        'rate_categories': rate_categories,
        'included_services': included_services,
        'optional_services': optional_services,
    }
    
    return render(request, 'tarifas.html', context)

def galeria_view(request):
    """
    Renderiza la página de 'Galería'.
    """
    room_types = RoomType.objects.filter(is_active=True).order_by('order')
    gallery_photos = GalleryPhoto.objects.filter(is_active=True).order_by('order')
    
    room_images_urls = [r.main_image.url for r in room_types]
    general_images_urls = [g.image.url for g in gallery_photos]

    all_images_for_featured = room_images_urls + general_images_urls
    random.shuffle(all_images_for_featured)
    
    context = {
        'room_types': room_types,
        'gallery_photos': gallery_photos,
        'featured_gallery_urls': all_images_for_featured[:6],
    }
    
    return render(request, 'galeria.html', context)


# ------------------------------------
# RUTAS DE CONTACTO, LOGIN Y ADMIN
# ------------------------------------

def contacto_base_view(request):
    """Renderiza la página base de Contacto."""
    return render(request, 'contacto.html', {})

def contacto_form_view(request):
    """Maneja el envío del formulario de contacto, guarda el mensaje y envía un correo electrónico."""
    
    if request.method == 'POST':
        form = ContactoCRMHForm(request.POST) 
        
        if form.is_valid():
            
            # --- 1. Guardar el Mensaje en la BD (Nuevo) ---
            mensaje_obj = ContactMessage.objects.create(
                nombre=form.cleaned_data['nombre'],
                email=form.cleaned_data['email'],
                telefono=form.cleaned_data['telefono'],
                mensaje=form.cleaned_data['mensaje']
            )

            # Extracción de datos del objeto guardado
            nombre = mensaje_obj.nombre
            email_cliente = mensaje_obj.email
            telefono = mensaje_obj.telefono
            mensaje_cliente = mensaje_obj.mensaje
            
            # --- 2. Configuración del Correo ---
            asunto_correo = f"Nueva Solicitud CRMH - Contacto de: {nombre}"
            
            # Usando la información del usuario para el cuerpo del correo
            cuerpo = f"""
            ¡Hola Juan Enrique!
            
            Se ha recibido una nueva solicitud de información para Casa de Reposo “Mi Hogar” (Maipú).
            
            --- Datos del Solicitante ---
            Nombre: {nombre}
            Email: {email_cliente}
            Teléfono: {telefono}
            
            --- Situación del Adulto Mayor ---
            {mensaje_cliente}
            
            ---
            Favor responder a la brevedad. Contacto del dueño: +56 9 9228 0344.
            """
            
            email = EmailMessage(
                subject=asunto_correo,
                body=cuerpo,
                # Email del destinatario (Juan Enrique Gómez Leviñanco)
                to=['jairletelier23@gmail.com'], 
                reply_to=[email_cliente]
            )
            
            # --- 3. Envío y Feedback ---
            try:
                email.send()
                messages.success(request, '¡Éxito! Tu solicitud ha sido enviada a Casa de Reposo “Mi Hogar”. Te contactaremos pronto.')
                return redirect('formulario_contacto') 
            
            except Exception as e:
                print(f"Error al enviar el correo: {e}")
                messages.error(request, 'Hubo un problema al enviar tu solicitud. Intenta más tarde o contáctanos por teléfono.')
                
        else:
            messages.error(request, 'Por favor, completa todos los campos requeridos correctamente.')
            
    form = ContactoCRMHForm(request.POST if request.method == 'POST' else None) 
        
    return render(request, 'formulario_contacto.html', {'form': form})

def login_view(request):
    """Maneja el inicio de sesión y redirige al panel de administración nativo de Django."""
    
    # Si el usuario ya está autenticado, lo redirige inmediatamente al admin
    if request.user.is_authenticated:
        return redirect(reverse('admin:index')) 

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Bienvenido, {username}. Serás redirigido al panel de administración.")
                # ✅ Redirección al panel nativo de Django
                return redirect(reverse('admin:index'))
            else:
                messages.error(request, "Nombre de usuario o contraseña incorrectos.")
        else:
            messages.error(request, "Error en el formulario. Por favor, revisa tus datos.")
            
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def panel_admin_view(request):
    """
    Función de redirección. Redirige al panel de administración nativo de Django 
    en lugar de renderizar una plantilla personalizada.
    """
    return redirect(reverse('admin:index'))


def logout_view(request):
    """Cierra la sesión del usuario y redirige al login."""
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, "Has cerrado sesión correctamente. Por favor, ingresa tus credenciales.")
    
    # 🚨 CORRECCIÓN APLICADA: Redirige al login.html
    return redirect('login') 

def upload_image_view(request):
    """Maneja la subida de imágenes desde un formulario POST y redirige al admin."""
    if request.method == 'POST':
        if 'image_file' in request.FILES:
            # LÓGICA DE GUARDADO EN BD (FALTANTE)
            messages.success(request, '¡Imagen procesada con éxito! (Falta la lógica de guardado en BD)')
        else:
            messages.error(request, 'No se ha seleccionado ningún archivo para subir.')
        
        # Redirige al admin nativo
        return redirect(reverse('admin:index'))
    
    # Redirige al admin nativo
    return redirect(reverse('admin:index'))