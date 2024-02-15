from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from registro import serializers
import random, string
class RegistroView(APIView):
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