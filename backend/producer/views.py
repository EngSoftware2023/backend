from datetime import date
from django.shortcuts import render
from rest_framework import viewsets
from .models import Producer, Production, ProducerProduction, Issue, ProducerIssue, Planting, ProducerPlanting
from product.models import Product
from .api.serializers import ProducerSerializer, ProductionSerializer, ProducerProductionSerializer, IssueSerializer, ProducerIssueSerializer, PlantingSerializer, ProducerPlantingSerializer
from product.api.serializers import ProductSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status

from django.contrib.auth.hashers import make_password, check_password
from rest_framework.permissions import IsAuthenticated

from user.models import User

class ProducerAPIView(APIView):
    def get(self, request):
        producer = Producer.objects.all()
        serializer = ProducerSerializer(producer, many=True)
        return Response(serializer.data)

    def post(self, request):
        new_request = request.data.copy()

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
        if(Producer.objects.filter(email=request.data['email']).exists() or User.objects.filter(email=request.data['email']).exists()):
            return Response({
                'error': True,
                'message': 'Email já cadastrado!'
            }, status=status.HTTP_400_BAD_REQUEST)

        password = make_password(request.data['password'])
        new_request['password'] = password
        serializer = ProducerSerializer(data=new_request)
        if serializer.is_valid():
            type_user = ''
            if('type' not in request.data):
                type_user = 'producer'
            else:
                type_user = 'admin'

            #create a user model to save the credentials
            user = User.objects.create(
                email=request.data['email'],
                password=password,
                name=request.data['name'],
                type=type_user
            )
            
            user.save()
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

        producer = Producer.objects.get(cpf=request.data['cpf'])
        producer.password = new_request['password']
        producer.name = new_request['name']
        producer.email = new_request['email']
        producer.phone = new_request['phone']
        producer.address = new_request['address']
        producer.save()
        return Response({
                'error': False,
                'message': 'Produtor atualizado com sucesso!'
            }, status=status.HTTP_200_OK)



        # serializer = ProducerSerializer(data=new_request)
        # if serializer.is_valid():
        #     producer = Producer.objects.get(cpf=request.data['cpf'])
        #     producer.password = new_request['password']
        #     producer.save()
        #     return Response({
        #         'error': False,
        #         'message': 'Produtor atualizado com sucesso!'
        #     }, status=status.HTTP_200_OK)
        # if(serializer.errors):
        #     return Response({
        #         'error': True,
        #         'message': 'Erro ao atualizar produtor!'
        #     }, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        if(not Producer.objects.filter(cpf=request.data['cpf']).exists()):
            return Response({
                'error': True,
                'message': 'Este produtor não existe!'
            }, status=status.HTTP_400_BAD_REQUEST)
        producer = Producer.objects.get(cpf=request.data["cpf"])
        user = User.objects.get(email=producer.email)
        user.delete()
        producer.delete()
        return Response({
            'error': False,
            'message': 'Produtor excluído com sucesso!'
        }, status=status.HTTP_200_OK)

class ProductionAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        if(user.type == 'producer'):
            producer = Producer.objects.get(email=user.email)
            production = Production.objects.filter(producer=producer.cpf)
            serializer = ProductionSerializer(production, many=True)
            return Response(serializer.data)
        elif(user.type == 'admin'):
            production = Production.objects.all()
            serializer = ProductionSerializer(production, many=True)
            return Response(serializer.data)
        else:
            return Response({
                'error': True,
                'message': 'Você não tem permissão para fazer isso!'
            }, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        user = request.user
        if(user.type != 'producer'):
            return Response({
                'error': True,
                'message': 'Você não tem permissão para fazer isso!'
            }, status=status.HTTP_401_UNAUTHORIZED)

        producer = Producer.objects.get(email=user.email)
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

        if(Production.objects.filter(producer=producer.cpf, product=request.data['product'], date=date.today()).exists()):
            prodution = Production.objects.get(producer=producer.cpf, product=request.data['product'], date=date.today())
            prodution.quantity += request.data['quantity']
            prodution.save()
            product = Product.objects.get(name=request.data['product'])
            product.stock += request.data['quantity']
            product.save()
            return Response({
                'error': False,
                'message': 'Produção cadastrada com sucesso!'
            }, status=status.HTTP_201_CREATED)

        request.data['producer'] = producer.cpf
        serializer = ProductionSerializer(data=request.data)
        product = Product.objects.get(name=request.data['product'])
        # request.data['price'] = product.price

        if serializer.is_valid():
            serializer.save()
            product = Product.objects.get(name=request.data['product'])
            product.stock += request.data['quantity']
            product.save()

            producer_production = ProducerProduction.objects.create(
                producer=producer,
                production=Production.objects.get(id=serializer.data['id'])
            )
            producer_production.save()

            production = Production.objects.get(id=serializer.data['id'])
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
        user = request.user
        producer = Producer.objects.get(cpf=request.data['producer'])
        if(not Production.objects.filter(id=request.data['id']).exists()):
            return Response({
                'error': True,
                'message': 'Esta produção não existe!'
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
        user = request.user
        if(not Production.objects.filter(id=request.data['id']).exists()):
            return Response({
                'error': True,
                'message': 'Esta produção não existe!'
            }, status=status.HTTP_400_BAD_REQUEST)
        producer = Producer.objects.get(email=user.email)
        if(not Production.objects.filter(id=request.data['id'], producer=producer.cpf).exists()):
            return Response({
                'error': True,
                'message': 'Esta produção não pertence a você!'
            }, status=status.HTTP_400_BAD_REQUEST)
        if(not Production.objects.filter(id=request.data['id']).exists()):
            return Response({
                'error': True,
                'message': 'Esta produção não existe!'
            }, status=status.HTTP_400_BAD_REQUEST)
        production = Production.objects.get(id=request.data['id'])
        product = Product.objects.get(name=production.product.name)
        product.stock -= production.quantity
        product.save()
        production.delete()
        return Response({
            'error': False,
            'message': 'Produção excluída com sucesso!'
        }, status=status.HTTP_200_OK)

class ProductionByManagerAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        if(user.type != 'admin'):
            return Response({
                'error': True,
                'message': 'Você não tem permissão para fazer isso!'
            }, status=status.HTTP_401_UNAUTHORIZED)
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

class IssueAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        issue = Issue.objects.all()
        serializer = IssueSerializer(issue, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        if(user.type != 'producer'):
            return Response({
                'error': True,
                'message': 'Você não tem permissão para fazer isso!'
            }, status=status.HTTP_401_UNAUTHORIZED)

        producer = Producer.objects.get(email=user.email)
        request.data['producer'] = producer.cpf
        serializer = IssueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            producer_issue = ProducerIssue.objects.create(
                producer=producer,
                issue=Issue.objects.get(id=serializer.data['id'])
            )
            producer_issue.save()
            return Response({
                'error': False,
                'message': 'Problema cadastrado com sucesso!'
            }, status=status.HTTP_201_CREATED)
        if(serializer.errors):
            if('type' not in request.data):
                return Response({
                    'error': True,
                    'message': 'Tipo não informado!'
                }, status=status.HTTP_400_BAD_REQUEST)
            if('description' not in request.data):
                return Response({
                    'error': True,
                    'message': 'Descrição não informada!'
                }, status=status.HTTP_400_BAD_REQUEST)
            return Response({
                'error': True,
                'message': 'Erro ao cadastrar problema!'
            }, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request):
        user = request.user
        if(user.type != 'producer'):
            return Response({
                'error': True,
                'message': 'Você não tem permissão para fazer isso!'
            }, status=status.HTTP_401_UNAUTHORIZED)
        if(not Issue.objects.filter(id=request.data['id']).exists()):
            return Response({
                'error': True,
                'message': 'Este problema não existe!'
            }, status=status.HTTP_400_BAD_REQUEST)
        producer = Producer.objects.get(email=user.email)
        if(not Issue.objects.filter(id=request.data['id'], producer=producer.cpf).exists()):
            return Response({
                'error': True,
                'message': 'Este problema não pertence a você!'
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer = IssueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'error': False,
                'message': 'Problema atualizado com sucesso!'
            }, status=status.HTTP_200_OK)
        if(serializer.errors):
            return Response({
                'error': True,
                'message': 'Erro ao atualizar problema!'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        user = request.user
        if(user.type != 'producer'):
            return Response({
                'error': True,
                'message': 'Você não tem permissão para fazer isso!'
            }, status=status.HTTP_401_UNAUTHORIZED)
        if(not Issue.objects.filter(id=request.data['id']).exists()):
            return Response({
                'error': True,
                'message': 'Este problema não existe!'
            }, status=status.HTTP_400_BAD_REQUEST)
        producer = Producer.objects.get(email=user.email)
        if(not Issue.objects.filter(id=request.data['id'], producer=producer.cpf).exists()):
            return Response({
                'error': True,
                'message': 'Este problema não pertence a você!'
            }, status=status.HTTP_400_BAD_REQUEST)
        issue = Issue.objects.get(id=request.data["id"])
        producer_issue = ProducerIssue.objects.get(issue=issue)
        producer_issue.delete()
        issue.delete()
        return Response({
            'error': False,
            'message': 'Problema excluído com sucesso!'
        }, status=status.HTTP_200_OK)
    
class PlantingAPIView(APIView):
    def get(self, request):
        planting = Planting.objects.all()
        serializer = PlantingSerializer(planting, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        user = request.user
        if(user.type != 'producer'):
            return Response({
                'error': True,
                'message': 'Você não tem permissão para fazer isso!'
            }, status=status.HTTP_401_UNAUTHORIZED)

        producer = Producer.objects.get(email=user.email)
        if(not Product.objects.filter(name=request.data['product']).exists()):
            return Response({
                'error': True,
                'message': 'Este produto não existe!'
            }, status=status.HTTP_400_BAD_REQUEST)
        if(request.data['expeted_harvest'] < date.today()):
            return Response({
                'error': True,
                'message': 'Data de colheita deve ser maior que a data atual!'
            }, status=status.HTTP_400_BAD_REQUEST)

        request.data['producer'] = producer.cpf
        serializer = PlantingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            producer_planting = ProducerPlanting.objects.create(
                producer=producer,
                planting=Planting.objects.get(id=serializer.data['id'])
            )
            producer_planting.save()
            return Response({
                'error': False,
                'message': 'Plantio cadastrado com sucesso!'
            }, status=status.HTTP_201_CREATED)
        if(serializer.errors):
            if('product' not in request.data):
                return Response({
                    'error': True,
                    'message': 'Produto não informado'
                }, status=status.HTTP_400_BAD_REQUEST)
            if('expeted_harvest' not in request.data):
                return Response({
                    'error': True,
                    'message': 'Data de colheita não informada!'
                }, status=status.HTTP_400_BAD_REQUEST)
            return Response({
                'error': True,
                'message': 'Erro ao cadastrar plantio!'
            }, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request):
        user = request.user
        if(user.type != 'producer'):
            return Response({
                'error': True,
                'message': 'Você não tem permissão para fazer isso!'
            }, status=status.HTTP_401_UNAUTHORIZED)
        if(not Planting.objects.filter(id=request.data['id']).exists()):
            return Response({
                'error': True,
                'message': 'Este plantio não existe!'
            }, status=status.HTTP_400_BAD_REQUEST)
        producer = Producer.objects.get(email=user.email)
        if(not Planting.objects.filter(id=request.data['id'], producer=producer.cpf).exists()):
            return Response({
                'error': True,
                'message': 'Este plantio não pertence a você!'
            }, status=status.HTTP_400_BAD_REQUEST)
        if(not Product.objects.filter(name=request.data['product']).exists()):
            return Response({
                'error': True,
                'message': 'Este produto não existe!'
            }, status=status.HTTP_400_BAD_REQUEST)
        if(request.data['expeted_harvest'] < date.today()):
            return Response({
                'error': True,
                'message': 'Data de colheita deve ser maior que a data atual!'
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer = PlantingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'error': False,
                'message': 'Plantio atualizado com sucesso!'
            }, status=status.HTTP_200_OK)
        if(serializer.errors):
            return Response({
                'error': True,
                'message': 'Erro ao atualizar plantio!'
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        if(user.type != 'producer'):
            return Response({
                'error': True,
                'message': 'Você não tem permissão para fazer isso!'
            }, status=status.HTTP_401_UNAUTHORIZED)
        if(not Planting.objects.filter(id=request.data['id']).exists()):
            return Response({
                'error': True,
                'message': 'Este plantio não existe!'
            }, status=status.HTTP_400_BAD_REQUEST)
        producer = Producer.objects.get(email=user.email)
        if(not Planting.objects.filter(id=request.data['id'], producer=producer.cpf).exists()):
            return Response({
                'error': True,
                'message': 'Este plantio não pertence a você!'
            }, status=status.HTTP_400_BAD_REQUEST)
        planting = Planting.objects.get(id=request.data["id"])
        producer_planting = ProducerPlanting.objects.get(planting=planting)
        producer_planting.delete()
        planting.delete()
        return Response({
            'error': False,
            'message': 'Plantio excluído com sucesso!'
        }, status=status.HTTP_200_OK)

class ProductionsByProductAPIView(APIView):
    def get(self, request):
        if(not Product.objects.filter(name=request.data['product']).exists()):
            return Response({
                'error': True,
                'message': 'Este produto não existe!'
            }, status=status.HTTP_400_BAD_REQUEST)
        product = Product.objects.get(name=request.data['product'])
        production = Production.objects.filter(product=product.name)
        serializer = ProductionSerializer(production, many=True)
        return Response(serializer.data)