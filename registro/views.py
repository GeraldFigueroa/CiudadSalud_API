from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from registro import serializers
from registro.models import Usuario
import jwt, datetime, random, string
class RegistroPacienteView(APIView):
    def post(self, request):

        serializer = serializers.PersonaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = {
            'identidad': serializer.data.identidad,
            'password': 'asd.456', #''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))
            'es_paciente': True,
            'es_empleado': False,
            'is_superuser': False
        }

        serializer = serializers.UsuarioSerializer(data=user_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'message': 'Paciente Registrado correctamente'
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        identidad = request.data['identidad']
        password = request.data['password']

        usuario = Usuario.objects.filter(identidad=identidad).first()
        print("Encontrado")
        if (usuario is None) or (not usuario.check_password(password)):
            raise AuthenticationFailed('Usuario o Contraseña Incorrectos')


        payload = {
            'identidad': usuario.identidad.identidad,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')


        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }

        return response
