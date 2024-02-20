from django.urls import path
from registro import views

urlpatterns = [
    path('paciente/', views.RegistroPacienteView.as_view(), name='registro_paciente'),
    path('login/paciente', views.LoginView.as_view(), name='login_paciente'),
]
