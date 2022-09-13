from django.contrib import  admin
from .models import CustomersData, TransactionData, TransactionDataResponse

# Register your models here.

admin.site.register(CustomersData)
admin.site.register(TransactionData)
admin.site.register(TransactionDataResponse)

