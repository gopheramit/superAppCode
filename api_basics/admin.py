from django.contrib import  admin
from .models import CustomersData, TransactionData, TransactionDataResponse


admin.site.register(CustomersData)
admin.site.register(TransactionData)
admin.site.register(TransactionDataResponse)

