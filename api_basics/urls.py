
from django.urls import path 
from .views import transactionList,accountTransfer,getMerchant, customers_list, createGruopPayment,setTransferResponse
#from .views import create_payment

urlpatterns = [
    path('customers/', customers_list),
    path('createGruopPayment/', createGruopPayment),
    # path('pay/', create_payment),
    path('getMerchant/', getMerchant),
    path('accountTransfer/', accountTransfer),
    path('setTransferResponse/', setTransferResponse),
    
    path('transactionList/', transactionList),

 
]
