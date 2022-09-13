from email import message
from locale import currency
from django.db import models


class CountriesStatus(models.Model):
    operation_id = models.TextField(primary_key=False)
    message = models.TextField()


class CountriesData(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    currency_name = models.CharField(max_length=100)


class Countries(models.Model):
    status = models.ForeignKey(CountriesStatus,on_delete=models.CASCADE)
    data = models.ForeignKey(CountriesData,on_delete=models.CASCADE)


class CustomersStatus(models.Model):
    operation_id = models.TextField(primary_key=True)
    message = models.TextField()


class CustomersData(models.Model):
    id = models.TextField(primary_key=True,default=None)
    ewallet = models.TextField()
    name = models.TextField()
    email = models.TextField()
    phone_number = models.TextField()


class Customers(models.Model):
    data = models.ForeignKey(CustomersData,on_delete=models.CASCADE)


class Ewallet(models.Model):
    ewallet = models.TextField()


class Fields(models.Model):
    number = models.TextField()
    expiration_month = models.TextField()
    expiration_year = models.TextField()
    cvv = models.TextField()
    name = models.TextField()


class PaymentMethod(models.Model):
    type=models.TextField()
    fields= models.ForeignKey(Fields,on_delete=models.CASCADE)


class Payment(models.Model):
    amount = models.TextField()
    currency = models.TextField()
    payment_method = models.ForeignKey(PaymentMethod,on_delete=models.CASCADE)
    ewallets = models.ForeignKey(Ewallet,on_delete=models.CASCADE)


class MeataData(models.Model):
    user_defined= models.TextField()


class CreateGroup(models.Model):
    metadata = models.ForeignKey(MeataData,on_delete=models.CASCADE)
    merchant_reference_id= models.TextField()
    payments = models.ForeignKey(Payment,on_delete=models.CASCADE)

    
class TransactionData(models.Model):
    transactionId = models.AutoField(primary_key=True,default=None)
    source = models.TextField(default=None)
    name=models.TextField(default=None)
    destination = models.TextField()
    amount = models.FloatField()
    destinationName=models.TextField(default=None)


class TransactionDataResponse(models.Model):
    source = models.TextField(primary_key=True,default=None)
    name=models.TextField(default=None)
    destination = models.TextField()
    amount = models.FloatField()









