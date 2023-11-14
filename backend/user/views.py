from django.shortcuts import render
from .models import User
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password

class UserAPIView(APIView):
    def get(self, request):
        users = User.objects.all()
        return Response(users.values())

    def post(self, request):
        data = request.data
        data['password'] = make_password(data['password'])
        user = User.objects.create(**data)
        return Response(user.values())

    def delete(self, request):
        User.objects.all().delete(email=request.data['email'])
        return Response(status=status.HTTP_204_NO_CONTENT)