from django.urls import path
from registro import views

urlpatterns = [
    path('paciente', views.RegistroPacienteView.as_view(), name='registro_paciente'),
    path('empleado', views.RegistroEmpleadoView.as_view(), name='registro_empleado'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout')
]
