from django.db import models

# Create your models here.

class Producer(models.Model):
    cpf = models.CharField(max_length=50, unique=True, primary_key=True)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.name