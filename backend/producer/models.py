from django.db import models
from product.models import Product


# Create your models here.

class Producer(models.Model):
    cpf = models.CharField(max_length=50, unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=200)
    productions = models.ManyToManyField('Production', through='ProducerProduction', related_name='productions')

    def __str__(self):
        return self.name
    
class Production(models.Model):
    id = models.AutoField(primary_key=True)
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Disponível')
    # price = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.product.name + ' - ' + self.producer.name
    
class ProducerProduction(models.Model):
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE)
    production = models.ForeignKey(Production, on_delete=models.CASCADE)

    def __str__(self):
        return self.producer.name + ' - ' + self.production.product.name