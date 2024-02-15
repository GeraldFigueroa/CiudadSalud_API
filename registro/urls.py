from django.urls import path
from registro import views

urlpatterns = [
    path('paciente/', views.RegistroView.as_view(), name='registro_paciente'),
]
