from rest_framework import serializers
from product import models

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'

class OrderProductSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    class Meta:
        model = models.OrderProduct
        fields = ['product_name', 'quantity', 'price']
        

class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True, read_only=True, source='orderproduct_set')
    class Meta:
        model = models.Order
        fields = ['id', 'name', 'date', 'total', 'status', 'products']