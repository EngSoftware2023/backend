from django.shortcuts import render
from rest_framework import viewsets
from .models import Producer, Production, ProducerProduction
from product.models import Product
from .api.serializers import ProducerSerializer, ProductionSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status

from django.views.decorators.http import require_http_methods
from django.contrib.auth.hashers import make_password, check_password

from datetime import date

class ProducerAPIView(APIView):
    def get(self, request):
        producer = Producer.objects.all()
        serializer = ProducerSerializer(producer, many=True)
        return Response(serializer.data)

    def post(self, request):
        if(len(request.data['password']) < 6):
            return Response({
                'error': True,
                'message': 'Senha deve ter no mínimo 6 caracteres!'
            }, status=status.HTTP_400_BAD_REQUEST)
        if(Producer.objects.filter(email=request.data['cpf']).exists()):
            return Response({
                'error': True,
                'message': 'CPF já cadastrado!'
            }, status=status.HTTP_400_BAD_REQUEST)
        if(Producer.objects.filter(email=request.data['email']).exists()):
            return Response({
                'error': True,
                'message': 'Email já cadastrado!'
            }, status=status.HTTP_400_BAD_REQUEST)
        password = make_password(request.data['password'])
        new_request = request.data.copy()
        new_request['password'] = password
        serializer = ProducerSerializer(data=new_request)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'error': False,
                'message': 'Produtor cadastrado com sucesso!'
            }, status=status.HTTP_201_CREATED)
        
        if serializer.errors:
            if('cpf' not in request.data):
                return Response({
                    'error': True,
                    'message': 'CPF não informado!'
                }, status=status.HTTP_400_BAD_REQUEST)
            if('email' not in request.data):
                return Response({
                    'error': True,
                    'message': 'Email não informado!'
                }, status=status.HTTP_400_BAD_REQUEST)
            if('phone' not in request.data):
                return Response({
                    'error': True,
                    'message': 'Telefone não informado!'
                }, status=status.HTTP_400_BAD_REQUEST)
            if('address' not in request.data):
                return Response({
                    'error': True,
                    'message': 'Endereço não informado!'
                }, status=status.HTTP_400_BAD_REQUEST)
            if('name' not in request.data):
                return Response({
                    'error': True,
                    'message': 'Nome não informado!'
                }, status=status.HTTP_400_BAD_REQUEST)
            return Response({
                'error': True,
                'message': 'Erro ao cadastrar produtor!'
            }, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request):
        if(not Producer.objects.filter(cpf=request.data['cpf']).exists()):
            return Response({
                'error': True,
                'message': 'Este produtor não existe!'
            }, status=status.HTTP_400_BAD_REQUEST)
        if(len(request.data['password']) < 6):
            return Response({
                'error': True,
                'message': 'Senha deve ter no mínimo 6 caracteres!'
            }, status=status.HTTP_400_BAD_REQUEST)
        new_request = request.data.copy()
        new_request['password'] = make_password(request.data['password'])
        serializer = ProducerSerializer(data=new_request)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'error': False,
                'message': 'Produtor atualizado com sucesso!'
            }, status=status.HTTP_200_OK)
        if(serializer.errors):
            return Response({
                'error': True,
                'message': 'Erro ao atualizar produtor!'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        if(not Producer.objects.filter(cpf=request.GET).exist):
            return Response({
                'error': True,
                'message': 'Este produtor não existe!'
            }, status=status.HTTP_400_BAD_REQUEST)
        producer = Producer.objects.get(cpf=request.GET)
        producer.delete()
        return Response({
            'error': False,
            'message': 'Produtor excluído com sucesso!'
        }, status=status.HTTP_200_OK)

class ProductionAPIView(APIView):
    def get(self, request):
        production = Production.objects.all()
        serializer = ProductionSerializer(production, many=True)
        return Response(serializer.data)

    def post(self, request):
        if(not Producer.objects.filter(cpf=request.data['producer']).exists()):
            return Response({
                'error': True,
                'message': 'Este produtor não existe!'
            }, status=status.HTTP_400_BAD_REQUEST)
        if(not Product.objects.filter(name=request.data['product']).exists()):
            return Response({
                'error': True,
                'message': 'Este produto não existe!'
            }, status=status.HTTP_400_BAD_REQUEST)
        if(request.data['quantity'] <= 0):
            return Response({
                'error': True,
                'message': 'Quantidade deve ser maior que 0!'
            }, status=status.HTTP_400_BAD_REQUEST)

        if(Production.objects.filter(producer=request.data['producer'], product=request.data['product'], date=date.today()).exists()):
            prodution = Production.objects.get(producer=request.data['producer'], product=request.data['product'], date=date.today())
            prodution.quantity += request.data['quantity']
            prodution.save()
            product = Product.objects.get(name=request.data['product'])
            product.stock += request.data['quantity']
            product.save()
            return Response({
                'error': False,
                'message': 'Produção cadastrada com sucesso!'
            }, status=status.HTTP_201_CREATED)


        serializer = ProductionSerializer(data=request.data)
        product = Product.objects.get(name=request.data['product'])
        # request.data['price'] = product.price

        if serializer.is_valid():
            serializer.save()
            product = Product.objects.get(name=request.data['product'])
            product.stock += request.data['quantity']
            product.save()

            producer_production = ProducerProduction.objects.create(
                producer=Producer.objects.get(cpf=request.data['producer']),
                production=Production.objects.get(id=serializer.data['id'])
            )
            producer_production.save()

            return Response({
                'error': False,
                'message': 'Produção cadastrada com sucesso!'
            }, status=status.HTTP_201_CREATED)
        if(serializer.errors):
            if('producer' not in request.data):
                return Response({
                    'error': True,
                    'message': 'Produtor não informado!'
                }, status=status.HTTP_400_BAD_REQUEST)
            if('product' not in request.data):
                return Response({
                    'error': True,
                    'message': 'Produto não informado!'
                }, status=status.HTTP_400_BAD_REQUEST)
            if('quantity' not in request.data):
                return Response({
                    'error': True,
                    'message': 'Quantidade não informada!'
                }, status=status.HTTP_400_BAD_REQUEST)
            return Response({
                'error': True,
                'message': 'Erro ao cadastrar produção!'
            }, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request):
        if(not Production.objects.filter(id=request.data['id']).exists()):
            return Response({
                'error': True,
                'message': 'Esta produção não existe!'
            }, status=status.HTTP_400_BAD_REQUEST)
        if(not Producer.objects.filter(cpf=request.data['producer']).exists()):
            return Response({
                'error': True,
                'message': 'Este produtor não existe!'
            }, status=status.HTTP_400_BAD_REQUEST)
        if(not Product.objects.filter(name=request.data['product']).exists()):
            return Response({
                'error': True,
                'message': 'Este produto não existe!'
            }, status=status.HTTP_400_BAD_REQUEST)
        if(request.data['quantity'] <= 0):
            return Response({
                'error': True,
                'message': 'Quantidade deve ser maior que 0!'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        product = Product.objects.get(name=request.data['product'])
        # request.data['price'] = product.price
        product.stock -= Production.objects.get(id=request.data['id']).quantity

        serializer = ProductionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            product = Product.objects.get(name=request.data['product'])
            product.stock += request.data['quantity']
            product.save()
            return Response({
                'error': False,
                'message': 'Produção atualizada com sucesso!'
            }, status=status.HTTP_200_OK)
        if(serializer.errors):
            return Response({
                'error': True,
                'message': 'Erro ao atualizar produção!'
            }, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request):
        if(not Production.objects.filter(id=request.GET).exists()):
            return Response({
                'error': True,
                'message': 'Esta produção não existe!'
            }, status=status.HTTP_400_BAD_REQUEST)
        production = Production.objects.get(id=request.GET)
        product = Product.objects.get(name=production.product.name)
        product.stock -= production.quantity
        product.save()
        producer_production = ProducerProduction.objects.get(production=production)
        producer_production.delete()
        production.delete()
        return Response({
            'error': False,
            'message': 'Produção excluída com sucesso!'
        }, status=status.HTTP_200_OK)
