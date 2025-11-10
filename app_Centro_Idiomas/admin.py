from django.contrib import admin
from .models import Idioma, Profesor, Clase

# Registrar los modelos aquí.
admin.site.register(Idioma)
admin.site.register(Profesor)
# admin.site.register(Clase)    # Dejar pendiente