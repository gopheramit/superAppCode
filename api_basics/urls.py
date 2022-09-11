
from django.urls import path 
from .views import createSalaryPayment, transactionList,accountTransfer,getMerchant, customers_list, createGruopPayment,setTransferResponse


urlpatterns = [
    path('customers/', customers_list),
    path('createGruopPayment/', createGruopPayment),
    path('getMerchant/', getMerchant),
    path('accountTransfer/', accountTransfer),
    path('setTransferResponse/', setTransferResponse),
    path('transactionList/', transactionList),
    path('createSalaryPayment/', createSalaryPayment),

 
]
