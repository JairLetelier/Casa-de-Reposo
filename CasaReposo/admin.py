from django.contrib import admin
# Importamos todos los modelos, incluyendo los nuevos para Tarifas
from .models import (
    CarouselImage, RoomType, GalleryPhoto, 
    RateCategory, IncludedService, OptionalService,
    ContactMessage # Asegúrate de que ContactMessage esté importado si lo usas.
)

# ----------------------------------------------------
# 1. Gestión del Carrusel (CarouselImage)
# ----------------------------------------------------
@admin.register(CarouselImage)
class CarouselImageAdmin(admin.ModelAdmin):
    # 💥 CORRECCIÓN: Cambiar 'image' por 'image_url'
    list_display = ('caption', 'image_url', 'order', 'is_active') 
    list_editable = ('order', 'is_active') 
    list_filter = ('is_active',)
    search_fields = ('caption',)
    
    fieldsets = (
        (None, {
            # 💥 CORRECCIÓN: Cambiar 'image' por 'image_url'
            'fields': ('image_url', 'caption', 'order', 'is_active')
        }),
    )
    
# ----------------------------------------------------
# 2. Tipos de Habitación (RoomType)
# ----------------------------------------------------
@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active', 'order')
    list_editable = ('price', 'is_active', 'order')
    search_fields = ('name', 'description')
    list_filter = ('is_active',)
    
    fieldsets = (
        ("Información Básica y Precios", {
            # 💥 CORRECCIÓN: Cambiar 'main_image' por 'main_image_url'
            'fields': ('name', 'main_image_url', 'price', 'is_active', 'order'),
        }),
        ("Contenido y Detalles", {
            'fields': ('description', 'details'),
            'description': 'Usa saltos de línea para listar los detalles o servicios incluidos.'
        })
    )

# ----------------------------------------------------
# 3. Fotos de Áreas Comunes/Generales (GalleryPhoto)
# ----------------------------------------------------
@admin.register(GalleryPhoto)
class GalleryPhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    search_fields = ('title', 'category')
    list_filter = ('category', 'is_active')
    
    fieldsets = (
        (None, {
            # 💥 CORRECCIÓN: Cambiar 'image' por 'image_url'
            'fields': ('title', 'image_url', 'category', 'is_active', 'order')
        }),
    )

# ====================================================
# 💥 NUEVOS REGISTROS PARA TARIFAS Y CONTACTO
# ====================================================

# ----------------------------------------------------
# 💥 REGISTRO 4: Categorías de Tarifa (RateCategory)
# ----------------------------------------------------
@admin.register(RateCategory)
class RateCategoryAdmin(admin.ModelAdmin):
    list_display = ('patient_type', 'monthly_rate', 'weekly_rate', 'is_active', 'order')
    list_editable = ('monthly_rate', 'weekly_rate', 'is_active', 'order')
    search_fields = ('patient_type', 'notes')
    list_filter = ('is_active',)
    
    fieldsets = (
        (None, {
            'fields': ('patient_type', 'monthly_rate', 'weekly_rate', 'notes', 'is_active', 'order')
        }),
    )

# ----------------------------------------------------
# 💥 REGISTRO 5: Servicios Incluidos (IncludedService)
# ----------------------------------------------------
@admin.register(IncludedService)
class IncludedServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    search_fields = ('name',)
    list_filter = ('is_active',)
    
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'is_active', 'order')
        }),
    )

# ----------------------------------------------------
# 💥 REGISTRO 6: Servicios Opcionales (OptionalService)
# ----------------------------------------------------
@admin.register(OptionalService)
class OptionalServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'cost', 'is_active', 'order')
    list_editable = ('cost', 'is_active', 'order')
    search_fields = ('name', 'cost')
    list_filter = ('is_active',)
    
    fieldsets = (
        (None, {
            'fields': ('name', 'cost', 'is_active', 'order')
        }),
    )
    
# ----------------------------------------------------
# 💥 REGISTRO 7: Mensajes de Contacto (ContactMessage)
# ----------------------------------------------------
# Debes añadir esta sección si usas el modelo ContactMessage
# @admin.register(ContactMessage)
# class ContactMessageAdmin(admin.ModelAdmin):
#     list_display = ('nombre', 'email', 'fecha_envio', 'respondido')
#     list_filter = ('respondido', 'fecha_envio')
#     search_fields = ('nombre', 'email', 'mensaje')
#     readonly_fields = ('nombre', 'email', 'telefono', 'mensaje', 'fecha_envio')
#     actions = ['mark_as_responded']
    
#     def mark_as_responded(self, request, queryset):
#         queryset.update(respondido=True)
#         self.message_user(request, "Los mensajes seleccionados han sido marcados como respondidos.")
#     mark_as_responded.short_description = "Marcar como respondido"