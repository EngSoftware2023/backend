from django.db import models
from product.models import Product


# Create your models here.
    
class Producer(models.Model):
    cpf = models.CharField(max_length=50, unique=True, primary_key=True)
    type = models.CharField(max_length=50, default='producer')
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=200)
    productions = models.ManyToManyField("Production", through='ProducerProduction', related_name='productions')
    issues = models.ManyToManyField("Issue", through='ProducerIssue', related_name='issues')
    plantings = models.ManyToManyField("Planting", through='ProducerPlanting', related_name='plantings')

    def __str__(self):
        return self.name

class Production(models.Model):
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Disponível')

    def __str__(self):
        return self.product.name + ' - ' + self.producer.name
    
class ProducerProduction(models.Model):
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE)
    production = models.ForeignKey(Production, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name + ' - ' + self.producer.name
    
class Issue(models.Model):
    id = models.AutoField(primary_key=True)
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Aberto')

    def __str__(self):
        return self.type + ' - ' + self.producer.name

class ProducerIssue(models.Model):
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)

    def __str__(self):
        return self.type + ' - ' + self.producer.name
    
class Planting(models.Model):
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    expeted_harvest = models.DateField()
    status = models.CharField(max_length=50, default='Em crescimento')
    pulverizations = models.ManyToManyField("Pulverization", through='PlantingPulverization', related_name='pulverizations')

    def __str__(self):
        return self.product.name + ' - ' + self.producer.name
    
class ProducerPlanting(models.Model):
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE)
    planting = models.ForeignKey(Planting, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name + ' - ' + self.producer.name
    
class Pulverization(models.Model):
    planting = models.ForeignKey(Planting, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    product = models.CharField(max_length=100)

    def __str__(self):
        return self.planting.product.name + ' - ' + self.planting.producer.name
    
class PlantingPulverization(models.Model):
    planting = models.ForeignKey(Planting, on_delete=models.CASCADE)
    pulverization = models.ForeignKey(Pulverization, on_delete=models.CASCADE)

    def __str__(self):
        return self.planting.product.name + ' - ' + self.pulverization.date