from django.db import models

class Idioma(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    nivel = models.CharField(max_length=50)
    region = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    codigo = models.CharField(max_length=10, unique=True)
    bandera_img = models.ImageField(upload_to='banderas/', blank=True, null=True)

    def __str__(self):
        return self.nombre
    
class Profesor(models.Model):
    nombre = models.CharField(max_length=100)
    ap_paterno = models.CharField(max_length=100)
    ap_materno = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    correo = models.EmailField(unique=True)
    id_idioma = models.ForeignKey(Idioma, on_delete=models.CASCADE, related_name="profesores")

    def __str__(self):
        return f"{self.nombre} {self.ap_paterno}"
    
class Clase(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    capacidad = models.PositiveIntegerField()
    nivel = models.CharField(max_length=50, choices=[
        ('Básico A1', 'Básico A1'),
        ('Básico A2', 'Básico A2'),
        ('Intermedio B1', 'Intermedio B1'),
        ('Intermedio B2', 'Intermedio B2'),
        ('Avanzado C1', 'Avanzado C1'),
        ('Avanzado C2', 'Avanzado C2')
    ])
    id_profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE, related_name="clases")
    idioma = models.ForeignKey(Idioma, on_delete=models.CASCADE, related_name="clases_idioma")

    def __str__(self):
        return f"{self.nombre} ({self.idioma.nombre})"