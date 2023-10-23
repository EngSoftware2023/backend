from django.contrib import admin
from .models import Producer

# Register your models here.

class ProducerAdmin(admin.ModelAdmin):
    fieldsets = [
        ('CPF', {'fields': ['cpf']}),
        ('Name', {'fields': ['name']}),
        ('Address', {'fields': ['address']}),
        ('Phone', {'fields': ['phone']}),
        ('Email', {'fields': ['email']}),
        ('Password', {'fields': ['password']}),
    ]
    list_display = ('cpf', 'name', 'address', 'phone', 'email', 'password')
    list_filter = ('cpf', 'name', 'address', 'phone', 'email', 'password')

admin.site.register(Producer)
