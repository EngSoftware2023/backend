from .models import Production, ProdcutionProduction, Producer
from product.models import Product

class VeririficationMidleware():
    def verifyProdutions(request):
        for production in Production.objects.all():
            if(production.date.day + production.product.time_life) <= request.date.day:
                production.delete()
    