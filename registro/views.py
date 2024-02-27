from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed, APIException
from registro import serializers
from registro.models import Usuario, Persona, Empleado, Cargo
import jwt, datetime, random, string

class RegistroPacienteView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')
        payload = is_authenticated(token)

        try:
            empleado = Usuario.objects.get(identidad=payload['identidad'])
        except Exception as e:
            raise AuthenticationFailed('Error de Autenticación, Usuario no encontrado')

        if empleado is None:
            raise AuthenticationFailed('Error de Login')

        if not empleado.is_superuser:
            if not empleado.is_staff:
                    raise AuthenticationFailed('Usuario sin permisos')

        serializer = serializers.PersonaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = {
            'identidad': serializer.data.identidad,
            'password': 'asd.456', #''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))
            'es_paciente': True,
            'es_empleado': False,
            'is_superuser': False,
            'is_staff': False,
            'username': request.data['persona']['identidad']
        }

        serializer = serializers.UsuarioSerializer(data=user_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'message': 'Paciente Registrado correctamente'
        }, status=status.HTTP_201_CREATED)
class PerfilPacienteView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        payload = is_authenticated(token)

        try:
            persona = Persona.objects.get(identidad=payload['identidad'])
        except Exception as e:
            raise AuthenticationFailed('Error de Autenticación, Usuario no encontrado')

        response = Response()
        response.data = {
            'message': 'Perfil de Paciente',
            'persona': {
                'primer_nombre': persona.primer_nombre,
                'segundo_nombre': persona.segundo_nombre,
                'primer_apellido': persona.primer_apellido,
                'segundo_apellido': persona.segundo_apellido,
                'email': persona.email,
                'telefono': persona.telefono,
                'direccion': persona.direccion,
                'estado_civil': persona.estado_civil
            }
        }
        response.status_code = 200
        return response
class LoginView(APIView):
    def post(self, request, tipo):
        identidad = request.data['identidad']
        password = request.data['password']

        try:
            usuario = Usuario.objects.filter(identidad=identidad).first()
        except Exception as e:
            raise AuthenticationFailed('Usuario o Contraseña Incorrectos')

        if tipo == 'P':
            if not usuario.es_paciente:
                raise AuthenticationFailed('Usuario o Contraseña Incorrectos')
        else:
            if not usuario.es_empleado:
                raise AuthenticationFailed('Usuario o Contraseña Incorrectos')

        persona = Persona.objects.get(identidad=identidad)
        if (usuario is None) or (not usuario.check_password(password)):
            raise AuthenticationFailed('Usuario o Contraseña Incorrectos')

        cargo = ''
        if usuario.es_paciente:
            cargo = 'Paciente'
        else:
            empleado = Empleado.objects.get(identidad=identidad)
            cargo = empleado.cargo

        payload = {
            'identidad': usuario.identidad.identidad,
            'cargo': cargo,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')


        response = Response()
        response.set_cookie(key='jwt', value=token, samesite='Lax')
        response.data = {
            'jwt': token,
            'persona': {
                'primer_nombre': persona.primer_nombre,
                'segundo_nombre': persona.segundo_nombre,
                'primer_apellido': persona.primer_apellido,
                'segundo_apellido': persona.segundo_apellido,
                'email': persona.email,
                'telefono': persona.telefono,
                'direccion': persona.direccion,
                'estado_civil': persona.estado_civil,
                'cargo': cargo
            }
        }
        response.status_code = 200
        return response
class RegistroEmpleadoView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')
        payload = is_authenticated(token)

        try:
            empleado = Usuario.objects.get(identidad=payload['identidad'])
        except Usuario.DoesNotExist:
            raise AuthenticationFailed('Error de Autenticación, Usuario no encontrado')

        if empleado is None:
            raise AuthenticationFailed('Error de Autenticación, Usuario no encontrado')

        if not empleado.is_superuser or not empleado.is_staff:
            raise AuthenticationFailed('Usuario sin permisos')

        try:
            serializer = serializers.PersonaSerializer(data=request.data['persona'])
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except Exception as e:
            raise APIException(str(e))

        user_data = {
            'identidad': request.data['persona']['identidad'],
            'password': 'asdf.4567', #''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))
            'es_paciente': False,
            'es_empleado': True,
            'is_superuser': False,
            'is_staff': False,
            'username': request.data['persona']['identidad']
        }

        try:
            serializer = serializers.UsuarioSerializer(data=user_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except Exception as e:
            raise APIException(str(e))

        try:
            serializer = serializers.EmpleadoSerializer(data=request.data['empleado'])
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except Exception as e:
            raise APIException(str(e))


        return Response({
            'message': 'Empleado Registrado correctamente'
        }, status=status.HTTP_201_CREATED)
class PerfilEmpleadoView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        payload = is_authenticated(token)

        try:
            persona = Persona.objects.get(identidad=payload['identidad'])
            empleado = Empleado.objects.get(identidad=payload['identidad'])
        except Exception as e:
            raise AuthenticationFailed('Error de Autenticación, Usuario no encontrado')

        response = Response()
        response.data = {
            'message': 'Perfil de Empleado',
            'empleado': {
                'primer_nombre': persona.primer_nombre,
                'segundo_nombre': persona.segundo_nombre,
                'primer_apellido': persona.primer_apellido,
                'segundo_apellido': persona.segundo_apellido,
                'email': persona.email,
                'telefono': persona.telefono,
                'direccion': persona.direccion,
                'estado_civil': persona.estado_civil,
                'cargo': empleado.cargo,
                'fecha_contratacion': empleado.fecha_contratacion
            }
        }
        response.status_code = 200
        return response
def is_authenticated(token):
    if not token:
        raise AuthenticationFailed('Sin Autenticación')
    try:
        payload = jwt.decode(token, 'secret', 'HS256')
    except Exception as e:
        print(e)
        raise AuthenticationFailed('TOKEN ERROR')

    return payload
class LogoutView(APIView):
    def get(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            "mensaje": 'Sesión Cerrada'
        }

        return response
class ChangePasswordView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')
        payload = is_authenticated(token)

        usuario = Usuario.objects.filter(identidad=payload['identidad']).first()
        if usuario is None:
            raise AuthenticationFailed('Error de Autenticación, Usuario no encontrado')

        usuario.set_password(request.data['password'])
        usuario.save()

        return Response({'mensaje': 'Contraseña Cambiada'}, status=200)
class CargoView(APIView):
    def get(self, request):
        #token = request.COOKIES.get('jwt')
        #payload = is_authenticated(token)
        cargos = Cargo.objects.all()
        serializer = serializers.CargoSerializer(cargos, many=True)
        return Response(serializer.data, status=200)