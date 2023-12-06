"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from producer.api.serializers import ProducerSerializer, ProductionSerializer
from producer.api.viewsets import ProducerViewSet, ProductionViewSet, IssueViewSet, PlantingViewSet, PulverizationViewSet
from producer.views import ProducerAPIView, ProductionAPIView, ProductionByManagerAPIView, IssueAPIView, PlantingAPIView, ProductionByManagerAPIView, ProductionsByProductAPIView

from product.api import viewsets as productviewsets
from product.api import serializers as productserializers
from product.views import ProductAPIView, OrderAPIView, OrderProductAPIView

from user.api import viewsets as userviewsets
from user.api import serializers as userserializers
from user.views import UserAPIView, CustomTokenObtainPairView

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

routers = routers.DefaultRouter()

routers.register(r'producer', ProducerViewSet, basename='Producer')
routers.register(r'product', productviewsets.ProductViewSet, basename='Product')
routers.register(r'user', userviewsets.UserViewSet, basename='User')
routers.register(r'production', ProductionViewSet, basename='Production')
routers.register(r'order', productviewsets.OrderViewSet, basename='Order')
routers.register(r'issue', IssueViewSet, basename='Issue')
routers.register(r'planting', PlantingViewSet, basename='Planting')
routers.register(r'pulverization', PulverizationViewSet, basename='Pulverization')


urlpatterns = [
    path('api/producer/', ProducerAPIView.as_view()),
    path('api/product/', ProductAPIView.as_view()),
    path('api/product/production/', ProductionsByProductAPIView.as_view()),
    path('api/production/', ProductionAPIView.as_view()),
    path('api/manager/production/', ProductionByManagerAPIView.as_view()),
    path('api/order/', OrderAPIView.as_view()),
    path('api/issue/', IssueAPIView.as_view()),
    path('api/planting/', PlantingAPIView.as_view()),

    path('api/orderproduct/', OrderProductAPIView.as_view()),

    path('api/user/', UserAPIView.as_view()),
    path('api/token/', CustomTokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),

    #path('admin/', admin.site.urls),
    path('', include(routers.urls)),
]
