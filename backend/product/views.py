from django.shortcuts import render
from rest_framework import viewsets
from .models import Product, Order, OrderProduct
from .api.serializers import ProductSerializer, OrderSerializer, OrderProductSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status

from django.contrib.auth.hashers import make_password, check_password

class ProductAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        if(Product.objects.filter(name=request.data['name']).exists()):
            return Response({
                'error': True,
                'message': 'Produto já cadastrado!'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'error': False,
                'message': 'Produto cadastrado com sucesso!'
            }, status=status.HTTP_201_CREATED)
        
        if serializer.errors:
            if('name' not in request.data):
                return Response({
                    'error': True,
                    'message': 'O produto precisa de um nome!'
                }, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                'error': True,
                'message': 'Erro ao cadastrar produto!'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        if(not Product.objects.filter(name=request.data['name']).exists()):
            return Response({
                'error': True,
                'message': 'Produto não cadastrado!'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        product = Product.objects.get(name=request.data['name'])
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'error': False,
                'message': 'Produto atualizado com sucesso!'
            }, status=status.HTTP_200_OK)
        
        if serializer.errors:
            return Response({
                'error': True,
                'message': 'Erro ao atualizar produto!'
            }, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request):
        if(not Product.objects.filter(name=request.GET).exists()):
            return Response({
                'error': True,
                'message': 'Produto não cadastrado!'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        product = Product.objects.get(name=request.GET)
        product.delete()
        return Response({
            'error': False,
            'message': 'Produto deletado com sucesso!'
        }, status=status.HTTP_200_OK)

class OrderAPIView(APIView):
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data['id'])
            order = Order.objects.get(id=serializer.data['id'])
            for product in request.data['products']:
                if(not Product.objects.filter(name=product['name']).exists()):
                    return Response({
                        'error': True,
                        'message': 'Produto não cadastrado!'
                    }, status=status.HTTP_400_BAD_REQUEST)
                if(OrderProduct.objects.filter(order=serializer.data['id'], product=product['name']).exists()):
                    orderProduct = OrderProduct.objects.get(order=serializer.data['id'], product=product['name'])
                    orderProduct.quantity += product['quantity']
                    orderProduct.save()
                orderProduct = OrderProduct(
                                        order=Order.objects.get(id=serializer.data['id']), 
                                        product=Product.objects.get(name=product['name']), 
                                                                    quantity=product['quantity'], 
                                                                    price=product['price'])
                orderProduct.save()
                order.total += product['price'] * product['quantity']
                order.save()
                productRegistered = Product.objects.get(name=product['name'])
                productRegistered.request += product['quantity']
                productRegistered.save()
            return Response({
                'error': False,
                'message': 'Pedido cadastrado com sucesso!'
            }, status=status.HTTP_201_CREATED)
        
        if serializer.errors:

            return Response({
                'error': True,
                'message': 'Erro ao cadastrar pedido!'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        if(not Order.objects.filter(id=request.data['id']).exists()):
            return Response({
                'error': True,
                'message': 'Pedido não cadastrado!'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        order = Order.objects.get(id=request.data['id'])
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'error': False,
                'message': 'Pedido atualizado com sucesso!'
            }, status=status.HTTP_200_OK)
        
        if serializer.errors:
            return Response({
                'error': True,
                'message': 'Erro ao atualizar pedido!'
            }, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request):
        if(not Order.objects.filter(id=request.data['id']).exists()):
            return Response({
                'error': True,
                'message': 'Pedido não cadastrado!'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        order = Order.objects.get(id=request.data['id'])
        order.delete()
        return Response({
            'error': False,
            'message': 'Pedido deletado com sucesso!'
        }, status=status.HTTP_200_OK)