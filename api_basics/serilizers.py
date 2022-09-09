from pyexpat import model
from rest_framework import serializers
from .models import CreateGroup,MeataData,Payment,PaymentMethod,Fields, Countries, CountriesData, CountriesStatus, Customers, CustomersData, CustomersStatus,Ewallet

class CountryStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountriesStatus
        fields = ('operation_id', 'message')


class CountryDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountriesData
        fields = ('id', 'name','currency_name')


class CountrySerializer(serializers.ModelSerializer):
    status = CountryStatusSerializer(many=False)
    data = CountryDataSerializer(many = True)
    class Meta:
        model = Countries
        fields =('status','data')


class CustomerStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomersStatus
        fields = ('operation_id', 'message')


class CustomersDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomersData
        fields =('id','ewallet','name','email','phone_number')


class CustomerSerializer(serializers.ModelSerializer):
    data = CustomersDataSerializer(many=True)
    # status = CustomerStatusSerializer(many=False)
    class Meta:
        model = Customers
        fields = '__all__'


class EwalletSerializer(serializers.ModelSerializer) :
    class Meta:
        model = Ewallet
        # fields = [ 'id' , 'title' , 'author' ]
        fields = '__all__'


class FieldsSerializer(serializers.ModelSerializer) :
    class Meta:
        model = Fields
        # fields = [ 'id' , 'title' , 'author' ]
        fields = '__all__'


class PaymentMethodSerializer(serializers.ModelSerializer) :
    fields=FieldsSerializer(many=False)
    class Meta:
        model = PaymentMethod
        # fields = [ 'id' , 'title' , 'author' ]
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer) :
    paymentMethod=PaymentMethodSerializer(many=False)
    ewallets=EwalletSerializer(many=False)
    class Meta:
        model = Payment
        # fields = [ 'id' , 'title' , 'author' ]
        fields = '__all__'

class MeataDataSerializer(serializers.ModelSerializer) :
    class Meta:
        model = MeataData
        # fields = [ 'id' , 'title' , 'author' ]
        fields = '__all__'

class CreateGroupSerializer(serializers.ModelSerializer) :
    metadata=MeataDataSerializer(many=False)
    payment=PaymentSerializer(many=True)
    class Meta:
        model = CreateGroup
        # fields = [ 'id' , 'title' , 'author' ]
        fields = '__all__'

        

