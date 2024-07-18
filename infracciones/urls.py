from django.urls import path
from infracciones.views import MyObtainTokenPairView, CargarInfraccionView, GenerarInformeView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("token/", MyObtainTokenPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('cargar_infraccion/', CargarInfraccionView.as_view(), name='cargar_infraccion'),
    path('generar_informe/', GenerarInformeView.as_view(), name='generar_informe'),
]