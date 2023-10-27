from .models import Production, ProdcutionProduction, Producer
from product.models import Product
from datetime import date

def getDays(month, year):
    if month == 2:
        if year % 4 == 0:
            return 29
        else:
            return 28
    elif month in [1, 3, 5, 7, 8, 10, 12]:
        return 31
    else:
        return 30

class VeririficationMiddleware():
    def verifyProdutions(request):
        for production in Production.objects.all():
            if(production.date.year == request.date.year and production.date.month == request.date.month):
                if(production.date.day + production.product.time_life) <= request.date.day:
                    production.status = 'Vencido'
            else:
                if (production.date.day + production.product.time_life) >= getDays(production.date.month, production.date.year):
                    daysOfLife = production.product.time_life
                    livedDays = getDays(production.date.month, production.date.year) - production.date.day + date.today().day
                    if daysOfLife <= livedDays:
                        production.status = 'Vencido'