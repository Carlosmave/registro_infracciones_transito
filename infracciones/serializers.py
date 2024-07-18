from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from infracciones.models import Infraccion

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["numero_unico_identificatorio"] = user.numero_unico_identificatorio
        return token
    

class InfraccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Infraccion
        exclude = ["id", "vehiculo", "oficial"]