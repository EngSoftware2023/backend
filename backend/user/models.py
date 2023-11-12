from django.db import models

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email,name,  password):
        if not email:
            raise ValueError('Usuário deve ter um e-mail válido!')
        if not name:
            raise ValueError('Usuário deve ter um nome válido!')
        if not password:
            raise ValueError('Usuário deve ter uma senha válida!')
        
        user = self.model(
            username=email,
            email=self.normalize_email(email),
            name=name,
            password=password,
        )
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email,name, password):
        user = self.create_user(
            email=self.normalize_email(email),
            name=name,
            password=password,
        )
        user.type = 'admin'
        user.save(using=self._db)
        return user
    
class User(AbstractUser):
    username = None
    type = models.CharField(max_length=50, default='producer')
    email = models.EmailField(max_length=50, unique=True)
    name = models.CharField(max_length=50, default='')
    password = models.CharField(max_length=200)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','password']
    
    objects = UserManager()
    
    def __str__(self):
        return self.name