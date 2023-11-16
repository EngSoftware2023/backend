from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    stock = models.IntegerField(default=0)
    request = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True)
    date = models.DateTimeField(auto_now_add=True)
    total = models.FloatField(null=True, default=0)
    status = models.CharField(max_length=100, default='pendente')
    products = models.ManyToManyField(Product, through='OrderProduct')

    def __str__(self):
        return str(self.id)
    
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    price = models.FloatField(null=True, blank=True, default=0)

    def __str__(self):
        return str(self.id)