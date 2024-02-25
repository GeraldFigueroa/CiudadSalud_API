from django.urls import path
from registro import views


urlpatterns = [
    path('paciente', views.RegistroPacienteView.as_view(), name='registro_paciente'),
    path('paciente/perfil', views.PerfilPacienteView.as_view(), name='perfil_paciente'),
    path('empleado', views.RegistroEmpleadoView.as_view(), name='registro_empleado'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('password/new', views.ChangePasswordView.as_view(), name='change_password')
]
