from rest_framework import viewsets
from product.api import serializers
from product import models

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()
