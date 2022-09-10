from django.contrib import  admin
from .models import CustomersData, Transactions

# Register your models here.

admin.site.register(CustomersData)
admin.site.register(Transactions)

