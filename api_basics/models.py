from email import message
from locale import currency
from django.db import models

# Create your models here.

class Article(models.Model) :
    title = models.CharField(max_length=100)
    author =models.CharField(max_length=100)
    # email = models.EmailField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



class CountriesStatus(models.Model):
    operation_id = models.TextField(primary_key=False)
    message = models.TextField()
    # emp_email = models.TextField(null = True)
    # created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    # created_at = models.DateTimeField(auto_now=True)

class CountriesData(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    currency_name = models.CharField(max_length=100)
    # emp_email = models.TextField(null = True)
    # created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    # created_at = models.DateTimeField(auto_now=True)

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
# class CustomersDataNew(models.Model):
#     id = models.TextField(primary_key=True,default=None)
#     ewallet = models.TextField()
#     name = models.TextField()
#     email = models.TextField()
#     phone_number = models.TextField()

class Customers(models.Model):
    # status = models.ForeignKey(CustomersStatus,on_delete=models.CASCADE)
    data = models.ForeignKey(CustomersData,on_delete=models.CASCADE)


