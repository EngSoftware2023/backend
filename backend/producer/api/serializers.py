from rest_framework import serializers
from producer import models

class ProducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Producer
        fields = '__all__'

class ProductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Production
        fields = '__all__'

class ProducerProductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProducerProduction
        fields = '__all__'

class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Issue
        fields = '__all__'

class ProducerIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProducerIssue
        fields = '__all__'

class PlantingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Planting
        fields = '__all__'

class ProducerPlantingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProducerPlanting
        fields = '__all__'

class PulverizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Pulverization
        fields = '__all__'

class PlantingPulverizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PlantingPulverization
        fields = '__all__'