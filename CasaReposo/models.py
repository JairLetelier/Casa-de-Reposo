from django.db import models

# ====================================================
# MODELOS EXISTENTES (CARRUSEL Y GALERÍA)
# ====================================================

# Modelo para las imágenes del Carrusel (Hero)
class CarouselImage(models.Model):
    # 💥 CAMBIO CRÍTICO: Reemplazar ImageField por CharField para almacenar la URL
    image_url = models.CharField(
        max_length=500, 
        verbose_name="URL de Imagen Pública", 
        help_text="Pega aquí el enlace de Imgur/Google Fotos. Máx 500 caracteres."
    ) 
    caption = models.CharField(max_length=255, blank=True, verbose_name="Título/Descripción")
    order = models.IntegerField(default=0, verbose_name="Orden")
    is_active = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Imagen del Carrusel"
        verbose_name_plural = "Imágenes del Carrusel"
        ordering = ['order']

    def __str__(self):
        return self.caption or f"Imagen de Carrusel #{self.id}"

# 💥 MODELO 1: Tipos de Habitación
class RoomType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre de la Habitación")
    # 💥 CAMBIO CRÍTICO: Reemplazar ImageField por CharField para almacenar la URL
    main_image_url = models.CharField(
        max_length=500, 
        verbose_name="URL de Foto Principal",
        help_text="Pega aquí el enlace de la imagen principal. Máx 500 caracteres."
    )
    description = models.TextField(verbose_name="Descripción", help_text="Descripción detallada de la habitación.")
    details = models.TextField(verbose_name="Detalles/Incluye", help_text="Lista de detalles o servicios incluidos. Usa saltos de línea para listar.")
    price = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True, verbose_name="Precio base mensual (opcional)")
    is_active = models.BooleanField(default=True, verbose_name="Mostrar en Galería")
    order = models.IntegerField(default=0, verbose_name="Orden de visualización")

    class Meta:
        verbose_name = "Tipo de Habitación"
        verbose_name_plural = "Tipos de Habitaciones"
        ordering = ['order']

    def __str__(self):
        return self.name

# 💥 MODELO 2: Fotos de Áreas Comunes/Generales
class GalleryPhoto(models.Model):
    CATEGORY_CHOICES = [
        ('PATIO', 'Patio/Jardín'),
        ('COMUN', 'Área Común/Salón'),
        ('FACHADA', 'Fachada/Exterior'),
        ('OTRO', 'Otro')
    ]
    
    title = models.CharField(max_length=150, verbose_name="Título de la Foto")
    # 💥 CAMBIO CRÍTICO: Reemplazar ImageField por CharField para almacenar la URL
    image_url = models.CharField(
        max_length=500, 
        verbose_name="URL de Archivo de Imagen",
        help_text="Pega aquí el enlace de la imagen de galería. Máx 500 caracteres."
    )
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='COMUN', verbose_name="Categoría")
    is_active = models.BooleanField(default=True, verbose_name="Mostrar en Galería")
    order = models.IntegerField(default=0, verbose_name="Orden de visualización")

    class Meta:
        verbose_name = "Foto de Galería (General)"
        verbose_name_plural = "Fotos de Galería (General)"
        ordering = ['order']

    def __str__(self):
        return self.title

# ====================================================
# MODELOS PARA TARIFAS (DINÁMICO)
# ====================================================

# 💥 MODELO 3: Categorías de Tarifa (Tabla)
class RateCategory(models.Model):
    patient_type = models.CharField(max_length=150, verbose_name="Tipo de Paciente/Estadía")
    weekly_rate = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True, verbose_name="Tarifa Semanal (CLP)", help_text="Monto sin puntos ni comas. Dejar en blanco si no aplica.")
    monthly_rate = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Tarifa Mensual (CLP)", help_text="Monto sin puntos ni comas.")
    notes = models.CharField(max_length=255, blank=True, verbose_name="Nota Adicional", help_text="Ej: 'Solo estadías cortas', 'Sujeto a evaluación médica'.")
    is_active = models.BooleanField(default=True, verbose_name="Mostrar en tabla")
    order = models.IntegerField(default=0, verbose_name="Orden")

    class Meta:
        verbose_name = "Categoría de Tarifa"
        verbose_name_plural = "Tarifas de Estadía"
        ordering = ['order']

    def __str__(self):
        return self.patient_type

# 💥 MODELO 4: Servicios Incluidos (Lista)
class IncludedService(models.Model):
    name = models.CharField(max_length=200, verbose_name="Servicio Incluido")
    description = models.TextField(blank=True, verbose_name="Descripción", help_text="Detalle breve del servicio.")
    is_active = models.BooleanField(default=True, verbose_name="Mostrar en lista")
    order = models.IntegerField(default=0, verbose_name="Orden")

    class Meta:
        verbose_name = "Servicio Incluido"
        verbose_name_plural = "Servicios Incluidos"
        ordering = ['order']

    def __str__(self):
        return self.name

# 💥 MODELO 5: Servicios Opcionales (Lista de Costos)
class OptionalService(models.Model):
    name = models.CharField(max_length=200, verbose_name="Servicio Opcional")
    cost = models.CharField(max_length=100, verbose_name="Costo/Frecuencia", help_text="Ej: '$15.000', 'Según requerimiento', 'Consultar'.")
    is_active = models.BooleanField(default=True, verbose_name="Mostrar en lista")
    order = models.IntegerField(default=0, verbose_name="Orden")

    class Meta:
        verbose_name = "Servicio Opcional"
        verbose_name_plural = "Costos de Servicios Opcionales"
        ordering = ['order']

    def __str__(self):
        return self.name

# ====================================================
# 🆕 MODELO AGREGADO: MENSAJES DE CONTACTO
# ====================================================
class ContactMessage(models.Model):
    """
    Modelo para almacenar los mensajes enviados a través del formulario de contacto.
    """
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True, null=True)
    mensaje = models.TextField()
    
    # Campos para la administración
    fecha_envio = models.DateTimeField(auto_now_add=True)
    respondido = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Mensaje de Contacto"
        verbose_name_plural = "Mensajes de Contacto"
        ordering = ['-fecha_envio'] # Los más nuevos primero

    def __str__(self):
        return f"Mensaje de {self.nombre} - {self.fecha_envio.strftime('%Y-%m-%d')}"