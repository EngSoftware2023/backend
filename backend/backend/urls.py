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
from producer.api.viewsets import ProducerViewSet, ProductionViewSet
from producer.views import ProducerAPIView, ProductionAPIView

from product.api import viewsets as productviewsets
from product.api import serializers as productserializers
from product.views import ProductAPIView


routers = routers.DefaultRouter()

routers.register(r'producer', ProducerViewSet, basename='Producer')
routers.register(r'production', ProductionViewSet, basename='Production')
routers.register(r'product', productviewsets.ProductViewSet, basename='Product')


urlpatterns = [
    path('api/producer/', ProducerAPIView.as_view()),
    path('api/product/', ProductAPIView.as_view()),
    path('api/production/', ProductionAPIView.as_view()),

    path('admin/', admin.site.urls),
    path('', include(routers.urls)),
]
