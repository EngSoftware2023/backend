from django.db import models

# Create your models here.

class Producer(models.Model):
    cpf = models.CharField(max_length=50, unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.name