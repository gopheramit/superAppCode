from pyexpat import model
from rest_framework import serializers
from .models import Article, Countries, CountriesData, CountriesStatus, Customers, CustomersData, CustomersStatus

class ArticleSerializer(serializers.ModelSerializer) :
    class Meta:
        model = Article
        # fields = [ 'id' , 'title' , 'author' ]
        fields = '__all__'


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
# class CustomersDataNewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomersDataNew
#         fields =('id','ewallet','name','email','phone_number')

class CustomerSerializer(serializers.ModelSerializer):
    data = CustomersDataSerializer(many=True)
    # status = CustomerStatusSerializer(many=False)
    class Meta:
        model = Customers
        fields = '__all__'


# class ArticleSerializers(serializers.Serializer):
#     title = serializers.CharField(max_length=100)
#     author =serializers.CharField(max_length=100)
#     email = serializers.EmailField(max_length=100)
#     date = serializers.DateTimeField()

#     def create(self, validated_data):
#         return Article.objects.create(validated_data)

#     def update(self, instance, validated_data):
       
#         instance.title = validated_data.get( ' title' , instance.title)
#         instance.author = validated_data.get('author' , instance.author)
#         instance.email = validated_data.get(' email' , instance.email)
#         instance.date = validated_data.get('date' , instance.date)
#         instance.save()

#         return instance
        
