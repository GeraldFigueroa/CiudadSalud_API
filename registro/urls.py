from django.urls import path
from registro import views


urlpatterns = [
    path('paciente', views.RegistroPacienteView.as_view(), name='registro_paciente'),
    path('paciente/login', views.LoginView.as_view(), kwargs={'tipo': 'P'}, name='login_paciente'),
    path('paciente/perfil', views.PerfilPacienteView.as_view(), name='perfil_paciente'),
    path('empleado', views.RegistroEmpleadoView.as_view(), name='registro_empleado'),
    path('empleado/perfil', views.PerfilEmpleadoView.as_view(), name='perfil_empleado'),
    path('empleado/login', views.LoginView.as_view(),kwargs={'tipo': 'E'} , name='login_empleado'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('password/new', views.ChangePasswordView.as_view(), name='change_password'),
    path('cargos', views.CargoView.as_view(), name='obtener_cargos'),
]