from rest_framework import viewsets
from producer.api import serializers
from producer import models

class ProducerViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProducerSerializer
    queryset = models.Producer.objects.all()

class ProductionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProductionSerializer
    queryset = models.Production.objects.all()

class ProducerProductionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProducerProductionSerializer
    queryset = models.ProducerProduction.objects.all()

class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.IssueSerializer
    queryset = models.Issue.objects.all()