from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    price = models.FloatField(null=True)
    stock = models.IntegerField(default=0)
    request = models.IntegerField(default=0)
    time_life = models.IntegerField(default=1)

    def __str__(self):
        return self.name