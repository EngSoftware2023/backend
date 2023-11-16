from rest_framework import serializers
from user import models
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from producer import models as producer_models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(CustomTokenObtainPairSerializer, cls).get_token(user)

        if(user.type == 'producer'):
            producer = producer_models.Producer.objects.get(email=user.email)

            token['type'] = user.type
            token['cpf'] = producer.cpf
            token['name'] = producer.name
            token['email'] = producer.email
            token['phone'] = producer.phone
            token['address'] = producer.address
        else:
            token['type'] = user.type
            token['email'] = user.email

        return token