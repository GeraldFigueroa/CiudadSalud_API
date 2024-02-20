from rest_framework import serializers
from registro import models

class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Persona
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Usuario
        fields = ['identidad', 'password', 'es_paciente', 'es_empleado', 'is_superuser', 'is_staff']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instace = self.Meta.model(**validated_data)
        if password is not None:
            instace.set_password(password)
        instace.save()
        return instace