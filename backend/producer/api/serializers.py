from rest_framework import serializers
from producer import models

class ProducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Producer
        fields = '__all__'