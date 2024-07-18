from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from infracciones.models import Infraccion, Vehiculo, Persona
from rest_framework_simplejwt.views import TokenObtainPairView
from infracciones.serializers import MyTokenObtainPairSerializer, InfraccionSerializer
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError

class MyObtainTokenPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class CargarInfraccionView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            placa_de_patente = request.data["placa_patente"]
            timestamp = request.data["timestamp"]
            comentarios = request.data["comentarios"]
            vehiculo = Vehiculo.objects.get(placa_de_patente = placa_de_patente)
            infraccion = Infraccion(
                vehiculo = vehiculo, 
                timestamp = timestamp, 
                comentarios = comentarios, 
                oficial = request.user
            )
            infraccion.save()
        except KeyError as e:
            return Response(
                {
                    "success": False, 
                    "message": f"Valor de {e} faltante."
                }, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Vehiculo.DoesNotExist:
            return Response(
                {
                    "success": False, 
                    "message": "La patente ingresada no existe."
                }, 
                status=status.HTTP_404_NOT_FOUND
            )
        except ValidationError:
            return Response(
                {
                    "success": False, 
                    "message": "El valor del timestamp debe estar en formato YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]."
                }, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return Response(
                {
                    "success": False, 
                    "message": f"Sucedió un error: {e}."
                }, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )   
        return Response(
            {
                "success": True, 
                "message": "Infracción registrada correctamente."
            }, 
            status=status.HTTP_200_OK
        )
    

class GenerarInformeView(APIView):
    def post(self, request):
        try:
            email = request.data["email"]
            persona = Persona.objects.get(email = email)
            vehiculos = persona.persona_vehiculos.all()
            infracciones_list = []
            for vehiculo in vehiculos:
                vehiculo_infracciones_dict = {"placa_de_patente": vehiculo.placa_de_patente}
                vehiculo_infracciones_dict["infracciones"] = InfraccionSerializer(
                    vehiculo.vehiculo_infracciones.all().order_by("timestamp"), many=True
                ).data
                infracciones_list.append(vehiculo_infracciones_dict)
        except KeyError as e:
            return Response(
                {
                    "success": False, 
                    "message": f"Valor de {e} faltante."
                }, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Persona.DoesNotExist:
            return Response(
                {
                    "success": False, 
                    "message": "El email ingresado no existe."
                }, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {
                    "success": False, 
                    "message": f"Sucedió un error: {e}."
                }, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) 
        return Response(
            {
                "success": True, 
                "infracciones": infracciones_list
            }, 
            status=status.HTTP_200_OK
        )