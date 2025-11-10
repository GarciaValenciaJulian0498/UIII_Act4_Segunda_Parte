Aquí tienes la estructura de carpetas y archivos actualizada para tu proyecto, incluyendo la subcarpeta profesores dentro de app_Idiomas/templates:

    UIII_Centro_de_Idiomas_0498/
    ├── backend_Idiomas/
    │   ├── backend_Idiomas/
    │   │   ├── __init__.py
    │   │   ├── asgi.py
    │   │   ├── settings.py
    │   │   ├── urls.py
    │   │   └── wsgi.py
    │   ├── app_Idiomas/
    │   │   ├── migrations/
    │   │   │   └── __init__.py
    │   │   ├── static/
    │   │   ├── templates/
    │   │   │   ├── base.html
    │   │   │   ├── home.html
    │   │   │   ├── navbar.html
    │   │   │   └── profesores/
    │   │   │       ├── agregar_profesor.html
    │   │   │       ├── ver_profesores.html
    │   │   │       ├── actualizar_profesor.html
    │   │   │       └── borrar_profesor.html
    │   │   ├── __init__.py
    │   │   ├── admin.py
    │   │   ├── apps.py
    │   │   ├── models.py
    │   │   ├── tests.py
    │   │   ├── urls.py
    │   │   └── views.py
    │   ├── manage.py
    └── venv/

1. backend_Idiomas/app_Idiomas/models.py

Asegúrate de que tu modelo Profesor esté definido. Necesitamos también el modelo Idioma para la relación ForeignKey. Si no lo tienes, aquí te lo incluyo:


    from django.db import models
    
    # ==========================================
    # MODELO: IDIOMA (asumido para el ForeignKey en Profesor)
    # ==========================================
    class Idioma(models.Model):
        nombre = models.CharField(max_length=50, unique=True)
    
        def __str__(self):
            return self.nombre
    
    # ==========================================
    # MODELO: PROFESORES
    # ==========================================
    class Profesor(models.Model):
        nombre = models.CharField(max_length=100)
        ap_paterno = models.CharField(max_length=100)
        ap_materno = models.CharField(max_length=100, blank=True, null=True)
        telefono = models.CharField(max_length=15, blank=True, null=True)
        correo = models.EmailField(unique=True)
        id_idioma = models.ForeignKey(Idioma, on_delete=models.CASCADE, related_name="profesores")
    
        def __str__(self):
            return f"{self.nombre} {self.ap_paterno}"

2. Procedimiento para realizar las migraciones

Desde la raíz de tu proyecto (donde está manage.py), ejecuta en la terminal:

    python manage.py makemigrations app_Idiomas
    python manage.py migrate

3. backend_Idiomas/app_Idiomas/views.py (Funciones CRUD para Profesores)

        from django.shortcuts import render, redirect, get_object_or_404
        from .models import Profesor, Idioma # Asegúrate de importar Idioma si lo necesitas para el formulario
  
        # Función para agregar un nuevo profesor
        def agregar_profesor(request):
            idiomas = Idioma.objects.all() # Obtener todos los idiomas para el select
            if request.method == 'POST':
                nombre = request.POST.get('nombre')
                ap_paterno = request.POST.get('ap_paterno')
                ap_materno = request.POST.get('ap_materno')
                telefono = request.POST.get('telefono')
                correo = request.POST.get('correo')
                id_idioma_id = request.POST.get('id_idioma') # Obtener el ID del idioma seleccionado
        
                idioma_obj = get_object_or_404(Idioma, pk=id_idioma_id) # Obtener el objeto Idioma
          
                Profesor.objects.create(
                    nombre=nombre,
                    ap_paterno=ap_paterno,
                    ap_materno=ap_materno,
                    telefono=telefono,
                    correo=correo,
                    id_idioma=idioma_obj
                )
                return redirect('ver_profesores') # Redirigir a la lista de profesores
            return render(request, 'profesores/agregar_profesor.html', {'idiomas': idiomas})
        
        # Función para ver todos los profesores
        def ver_profesores(request):
            profesores = Profesor.objects.all()
            return render(request, 'profesores/ver_profesores.html', {'profesores': profesores})
        
        # Función para editar un profesor (muestra el formulario con datos actuales)
        def actualizar_profesor(request, pk):
            profesor = get_object_or_404(Profesor, pk=pk)
            idiomas = Idioma.objects.all()
            return render(request, 'profesores/actualizar_profesor.html', {'profesor': profesor, 'idiomas': idiomas})
        
        # Función para realizar la actualización del profesor
        def realizar_actualizacion_profesor(request, pk):
            if request.method == 'POST':
                profesor = get_object_or_404(Profesor, pk=pk)
                profesor.nombre = request.POST.get('nombre')
                profesor.ap_paterno = request.POST.get('ap_paterno')
                profesor.ap_materno = request.POST.get('ap_materno')
                profesor.telefono = request.POST.get('telefono')
                profesor.correo = request.POST.get('correo')
                
                id_idioma_id = request.POST.get('id_idioma')
                idioma_obj = get_object_or_404(Idioma, pk=id_idioma_id)
                profesor.id_idioma = idioma_obj
                
                profesor.save()
                return redirect('ver_profesores')
            return redirect('ver_profesores') # En caso de que se acceda por GET, redirigir
        
        # Función para borrar un profesor
        def borrar_profesor(request, pk):
            profesor = get_object_or_404(Profesor, pk=pk)
            if request.method == 'POST':
                profesor.delete()
                return redirect('ver_profesores')
            return render(request, 'profesores/borrar_profesor.html', {'profesor': profesor})

4. backend_Idiomas/app_Idiomas/urls.py (URLs para Profesores)

Añade estas URLs para que las funciones de vista sean accesibles:

    from django.urls import path
    from . import views
    
    urlpatterns = [
        # URLs para Profesores
        path('profesores/agregar/', views.agregar_profesor, name='agregar_profesor'),
        path('profesores/', views.ver_profesores, name='ver_profesores'),
        path('profesores/actualizar/<int:pk>/', views.actualizar_profesor, name='actualizar_profesor'),
        path('profesores/realizar_actualizacion/<int:pk>/', views.realizar_actualizacion_profesor, name='realizar_actualizacion_profesor'),
        path('profesores/borrar/<int:pk>/', views.borrar_profesor, name='borrar_profesor'),
    ]

Asegúrate de que en el backend_Idiomas/backend_Idiomas/urls.py principal, tengas incluida las URLs de app_Idiomas:

    from django.contrib import admin
    from django.urls import path, include
    
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', include('app_Idiomas.urls')), # Incluye las URLs de tu aplicación
    ]

5. backend_Idiomas/app_Idiomas/templates/navbar.html (Modificar Menú)

Modifica el archivo navbar.html para incluir las opciones de profesores. Asumo que tienes una estructura similar a esta para tu barra de navegación:

    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <a class="navbar-brand" href="#">Cinépolis Idiomas</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav">
                <li class="nav-item active">
                    <a class="nav-link" href="/">Inicio <span class="sr-only">(current)</span></a>
                </li>
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" id="navbarDropdownProfesores" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        Profesores
                    </a>
                    <div class="dropdown-menu" aria-labelledby="navbarDropdownProfesores">
                        <a class="dropdown-item" href="{% url 'agregar_profesor' %}">Agregar Profesor</a>
                        <a class="dropdown-item" href="{% url 'ver_profesores' %}">Ver Profesores</a>
                    </div>
                </li>
                <!-- Otras opciones del menú (Salas, Clases, etc.) si las tienes -->
            </ul>
        </div>
    </nav>

Este navbar es muy básico, lo puedes estilizar con colores suaves como solicitaste.

6. backend_Idiomas/app_Idiomas/templates/profesores/ (Archivos HTML)

Aquí están los archivos HTML con colores suaves y atractivos. Usaré un poco de Bootstrap para facilitar el diseño. Asegúrate de tener Bootstrap incluido en tu base.html.

backend_Idiomas/app_Idiomas/templates/base.html (Ejemplo con Bootstrap)

Si no tienes un base.html con Bootstrap, aquí tienes un ejemplo. Esto es crucial para que los estilos CSS funcionen.

    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{% block title %}Cinépolis Idiomas{% endblock %}</title>
        <!-- Bootstrap CSS -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                background-color: #f8f9fa; /* Gris muy claro */
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            .navbar {
                background-color: #e3f2fd !important; /* Azul claro */
            }
            .container {
                background-color: #ffffff;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.05);
                margin-top: 30px;
            }
            h1, h2, h3 {
                color: #343a40; /* Gris oscuro */
            }
            .btn-primary {
                background-color: #007bff;
                border-color: #007bff;
            }
            .btn-success {
                background-color: #28a745;
                border-color: #28a745;
            }
            .btn-warning {
                background-color: #ffc107;
                border-color: #ffc107;
            }
            .btn-danger {
                background-color: #dc3545;
                border-color: #dc3545;
            }
            .table th {
                background-color: #f0f8ff; /* Azul muy pálido */
                color: #343a40;
            }
        </style>
    </head>
    <body>
        {% include 'navbar.html' %}
        <div class="container">
            {% block content %}
            {% endblock %}
        </div>
    
        <!-- Bootstrap JS y dependencias (Popper.js) -->
        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.7/dist/umd/popper.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.min.js"></script>
    </body>
    </html>

backend_Idiomas/app_Idiomas/templates/profesores/agregar_profesor.html

    {% extends 'base.html' %}
    
    {% block title %}Agregar Profesor{% endblock %}
    
    {% block content %}
    <div class="card shadow-sm p-4">
        <h2 class="mb-4 text-center">Registrar Nuevo Profesor</h2>
        <form method="post">
            {% csrf_token %}
            <div class="mb-3">
                <label for="nombre" class="form-label">Nombre:</label>
                <input type="text" class="form-control" id="nombre" name="nombre" required>
            </div>
            <div class="mb-3">
                <label for="ap_paterno" class="form-label">Apellido Paterno:</label>
                <input type="text" class="form-control" id="ap_paterno" name="ap_paterno" required>
            </div>
            <div class="mb-3">
                <label for="ap_materno" class="form-label">Apellido Materno:</label>
                <input type="text" class="form-control" id="ap_materno" name="ap_materno">
            </div>
            <div class="mb-3">
                <label for="telefono" class="form-label">Teléfono:</label>
                <input type="text" class="form-control" id="telefono" name="telefono">
            </div>
            <div class="mb-3">
                <label for="correo" class="form-label">Correo Electrónico:</label>
                <input type="email" class="form-control" id="correo" name="correo" required>
            </div>
            <div class="mb-3">
                <label for="id_idioma" class="form-label">Idioma que Imparte:</label>
                <select class="form-select" id="id_idioma" name="id_idioma" required>
                    {% for idioma in idiomas %}
                        <option value="{{ idioma.pk }}">{{ idioma.nombre }}</option>
                    {% endfor %}
                </select>
            </div>
            <div class="d-grid gap-2">
                <button type="submit" class="btn btn-success btn-lg">Agregar Profesor</button>
                <a href="{% url 'ver_profesores' %}" class="btn btn-secondary btn-lg">Cancelar</a>
            </div>
        </form>
    </div>
    {% endblock %}

backend_Idiomas/app_Idiomas/templates/profesores/ver_profesores.html

    {% extends 'base.html' %}
    
    {% block title %}Ver Profesores{% endblock %}
    
    {% block content %}
    <h2 class="mb-4 text-center">Nuestros Profesores</h2>
    <div class="text-end mb-3">
        <a href="{% url 'agregar_profesor' %}" class="btn btn-primary">Agregar Nuevo Profesor</a>
    </div>
    
    {% if profesores %}
    <div class="table-responsive">
        <table class="table table-hover table-striped">
            <thead class="table-light">
                <tr>
                    <th>Nombre</th>
                    <th>Apellido Paterno</th>
                    <th>Apellido Materno</th>
                    <th>Teléfono</th>
                    <th>Correo</th>
                    <th>Idioma</th>
                    <th class="text-center">Acciones</th>
                </tr>
            </thead>
            <tbody>
                {% for profesor in profesores %}
                <tr>
                    <td>{{ profesor.nombre }}</td>
                    <td>{{ profesor.ap_paterno }}</td>
                    <td>{% if profesor.ap_materno %}{{ profesor.ap_materno }}{% else %}N/A{% endif %}</td>
                    <td>{% if profesor.telefono %}{{ profesor.telefono }}{% else %}N/A{% endif %}</td>
                    <td>{{ profesor.correo }}</td>
                    <td>{{ profesor.id_idioma.nombre }}</td>
                    <td class="text-center">
                        <a href="{% url 'actualizar_profesor' profesor.pk %}" class="btn btn-warning btn-sm me-2">Editar</a>
                        <a href="{% url 'borrar_profesor' profesor.pk %}" class="btn btn-danger btn-sm">Borrar</a>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
    {% else %}
    <div class="alert alert-info text-center" role="alert">
        No hay profesores registrados aún. ¡Anímate a agregar uno!
    </div>
    {% endif %}
    {% endblock %}

backend_Idiomas/app_Idiomas/templates/profesores/actualizar_profesor.html

    {% extends 'base.html' %}
    
    {% block title %}Actualizar Profesor{% endblock %}
    
    {% block content %}
    <div class="card shadow-sm p-4">
        <h2 class="mb-4 text-center">Actualizar Información del Profesor</h2>
        <form method="post" action="{% url 'realizar_actualizacion_profesor' profesor.pk %}">
            {% csrf_token %}
            <div class="mb-3">
                <label for="nombre" class="form-label">Nombre:</label>
                <input type="text" class="form-control" id="nombre" name="nombre" value="{{ profesor.nombre }}" required>
            </div>
            <div class="mb-3">
                <label for="ap_paterno" class="form-label">Apellido Paterno:</label>
                <input type="text" class="form-control" id="ap_paterno" name="ap_paterno" value="{{ profesor.ap_paterno }}" required>
            </div>
            <div class="mb-3">
                <label for="ap_materno" class="form-label">Apellido Materno:</label>
                <input type="text" class="form-control" id="ap_materno" name="ap_materno" value="{{ profesor.ap_materno|default_if_none:'' }}">
            </div>
            <div class="mb-3">
                <label for="telefono" class="form-label">Teléfono:</label>
                <input type="text" class="form-control" id="telefono" name="telefono" value="{{ profesor.telefono|default_if_none:'' }}">
            </div>
            <div class="mb-3">
                <label for="correo" class="form-label">Correo Electrónico:</label>
                <input type="email" class="form-control" id="correo" name="correo" value="{{ profesor.correo }}" required>
            </div>
            <div class="mb-3">
                <label for="id_idioma" class="form-label">Idioma que Imparte:</label>
                <select class="form-select" id="id_idioma" name="id_idioma" required>
                    {% for idioma in idiomas %}
                        <option value="{{ idioma.pk }}" {% if idioma == profesor.id_idioma %}selected{% endif %}>
                            {{ idioma.nombre }}
                        </option>
                    {% endfor %}
                </select>
            </div>
            <div class="d-grid gap-2">
                <button type="submit" class="btn btn-primary btn-lg">Guardar Cambios</button>
                <a href="{% url 'ver_profesores' %}" class="btn btn-secondary btn-lg">Cancelar</a>
            </div>
        </form>
    </div>
    {% endblock %}

backend_Idiomas/app_Idiomas/templates/profesores/borrar_profesor.html

    {% extends 'base.html' %}
    
    {% block title %}Borrar Profesor{% endblock %}
    
    {% block content %}
    <div class="card shadow-sm p-4 text-center">
        <h2 class="mb-4 text-danger">Confirmar Borrado de Profesor</h2>
        <p class="lead">¿Estás seguro de que quieres eliminar a <strong>{{ profesor.nombre }} {{ profesor.ap_paterno }}</strong> de la lista de profesores?</p>
        <p class="text-muted">Esta acción no se puede deshacer.</p>
    
        <form method="post" action="{% url 'borrar_profesor' profesor.pk %}">
            {% csrf_token %}
            <div class="d-grid gap-2 col-md-6 mx-auto">
                <button type="submit" class="btn btn-danger btn-lg">Sí, Eliminar</button>
                <a href="{% url 'ver_profesores' %}" class="btn btn-secondary btn-lg">Cancelar</a>
            </div>
        </form>
    </div>
    {% endblock %}

7. backend_Idiomas/app_Idiomas/admin.py (Registrar Modelos)

        from django.contrib import admin
        from .models import Profesor, Idioma
        
        # Registra tus modelos aquí.
        admin.site.register(Idioma)
        admin.site.register(Profesor)

8. Volver a realizar las migraciones (Si hiciste cambios en el modelo Idioma o si quieres estar seguro)

        python manage.py makemigrations app_Idiomas
        python manage.py migrate

9. Crear un superusuario (si no tienes uno)

Necesitarás un superusuario para acceder al panel de administración de Django y poder crear algunos Idioma para que la ForeignKey del Profesor funcione.

    python manage.py createsuperuser

10. Ejecutar el servidor en el puerto 8498

Desde la raíz de tu proyecto (donde está manage.py), ejecuta en la terminal:

    python manage.py runserver 8498

Ahora puedes abrir tu navegador y visitar http://127.0.0.1:8498/. En la barra de navegación, busca la opción "Profesores" para empezar a usar el CRUD. También puedes ir a http://127.0.0.1:8498/admin/ para gestionar los Idiomas y Profesores desde el panel de administración.

¡Espero que esto te sea de gran ayuda para tu proyecto!
