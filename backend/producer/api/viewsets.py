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

class ProducerIssueViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProducerIssueSerializer
    queryset = models.ProducerIssue.objects.all()

class PlantingViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PlantingSerializer
    queryset = models.Planting.objects.all()

class ProducerPlantingViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProducerPlantingSerializer
    queryset = models.ProducerPlanting.objects.all()