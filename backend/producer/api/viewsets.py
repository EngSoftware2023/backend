from rest_framework import viewsets
from producer.api import serializers
from producer import models

class ProducerViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProducerSerializer
    queryset = models.Producer.objects.all()