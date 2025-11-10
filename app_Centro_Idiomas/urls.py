from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio_centro_idiomas, name='inicio_centro_idiomas'),
    path('idiomas/agregar/', views.agregar_idioma, name='agregar_idioma'),
    path('idiomas/', views.ver_idiomas, name='ver_idiomas'),
    path('idiomas/actualizar/<int:id_idioma>/', views.actualizar_idioma, name='actualizar_idioma'),
    path('idiomas/borrar/<int:id_idioma>/', views.borrar_idioma, name='borrar_idioma'),
    
    path('profesores/agregar/', views.agregar_profesor, name='agregar_profesor'),
    path('profesores/', views.ver_profesores, name='ver_profesores'),
    path('profesores/actualizar/<int:pk>/', views.actualizar_profesor, name='actualizar_profesor'),
    path('profesores/realizar_actualizacion/<int:pk>/', views.realizar_actualizacion_profesor, name='realizar_actualizacion_profesor'),
    path('profesores/borrar/<int:pk>/', views.borrar_profesor, name='borrar_profesor'),
]