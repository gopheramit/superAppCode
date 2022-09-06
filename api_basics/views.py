from http.client import BAD_REQUEST
import imp
import json
from telnetlib import STATUS
from django.shortcuts import render

from django.http.response import HttpResponse,JsonResponse 
from rest_framework.parsers import JSONParser

from api_basics.utilities.make_request import make_request
from .models import Article, Customers
from .serilizers import ArticleSerializer, CountrySerializer, CustomerSerializer, CustomersDataSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins


class GenericArticleView(generics.GenericAPIView,mixins.DestroyModelMixin,mixins.ListModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,mixins.RetrieveModelMixin):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    lookup_field = 'id'

    def get(self, request,id = None):
        if id:
            return self.retrieve(id)
        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request,id = None):
        return self.create(request,id)

    def delete(self, request,id = None):
        return self.destroy(request,id)


class ArticleAPIView(APIView):
    def get(self, request):
        articles=Article.objects.all()
        serilizer=ArticleSerializer(articles,many=True)
        return Response(serilizer.data)
    
    def post(self, request):
        serilizer=ArticleSerializer(data=request.data)

        if serilizer.is_valid():
            serilizer.save()
            return Response(serilizer.data ,status=status.HTTP_201_CREATED)
        return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST)



class ArticleDetailsAPIView(APIView):
    def get_object(self, id):
        try:
            return Article.objects.get(id=id)
        except Article.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, id):
        article = self.get_object(id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    
    def put(self, request, id):
        article = self.get_object(id)
        serilizer=ArticleSerializer(article,data=request.data)
        if serilizer.is_valid():
            serilizer.save()
            return Response(serilizer.data )
        return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, id):
        article = self.get_object(id)
        article.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)



# Create your views here.
@api_view(['GET','POST'])
@csrf_exempt
def article_list(request):
    if request.method=="GET":
        articles=Article.objects.all()
        serilizer=ArticleSerializer(articles,many=True)
        return Response(serilizer.data)

    elif request.method=="POST":
        serilizer=ArticleSerializer(data=request.data)

        if serilizer.is_valid():
            serilizer.save()
            return Response(serilizer.data ,status=status.HTTP_201_CREATED)
        return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@csrf_exempt
def countries_list(request):
    if request.method=="GET":
        data_response = make_request('get','/v1/customers?limit=100','')
        serizalizer = CustomerSerializer(data_response)
        print("""
        serializer iss 

        """)
        print(serizalizer)
        print("""
        
        
        """)
        news = serizalizer.data
        for ele in news['data']:
            print("teri maa ki cjhuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu",ele)
            ele = json.dumps(ele)
            print(ele)
            custdataserializer = CustomersDataSerializer(data = json.loads(ele))
            # custdataserializer = CustomersDataNewSerializer(data = json.loads(ele))
            print("""
            
            
            """)
            print(custdataserializer)
            print(custdataserializer.is_valid())
            if custdataserializer.is_valid():
                custdataserializer.save()
        # if serizalizer.is_valid():
        #     serizalizer.save()

        # print(serizalizer.is_valid())
        # if serizalizer.is_valid():
        #     print(serizalizer.data)
        #     data=serizalizer.validated_data.get('data')
        #     print("data is _________________________________________- ",data)
        #     for ele in data['data'] :
        #         print("eleeeeeeeeeeeeeeeeeeeee",ele)
        #         newserializer = CustomersDataSerializer(data = ele)

        #         if newserializer.is_valid():
        #             print("new seriazl____--------------------------")
        #             print(newserializer)
        #             newserializer.save()

        
        # if serizalizer.is_valid():
        return Response(serizalizer.data)
        # else:
        #     return Response(serizalizer.errors,status=BAD_REQUEST)
        
@api_view(['POST'])
@csrf_exempt
def create_gr(request):
    if request.method=="POST":
        body={"metadata":{"user_defined":"silver"},"merchant_reference_id":"12345689","payments":[{"amount":"5","currency":"USD","payment_method":{"type":"sg_debit_visa_card","fields":{"number":"4111111111111111","expiration_month":"10","expiration_year":"23","cvv":"123","name":"Rivers"}},"ewallets":[{"ewallet":"ewallet_f49f45152f2081fbccf70052fdd8c9c0"}]},{"amount":"2","currency":"USD","payment_method":{"type":"sg_debit_visa_card","fields":{"number":"4111111111111111","expiration_month":"10","expiration_year":"23","cvv":"123","name":"Henderson"}},"ewallets":[{"ewallet":"ewallet_ad689618491a6161f5c2e49dcf4aa156"}]}]}
        data_response = make_request('post','/v1/payments/group_payments',body)
        print(data_response)

        # serizalizer = CountrySerializer(data_response)
        # print("""
        # serializer iss 

        # """)
        # print(serizalizer)
        # # if serizalizer.is_valid():
        return Response(status=status.HTTP_201_CREATED)
        # else:
        #     return Response(serizalizer.errors,status=BAD_REQUEST)
        





@api_view(['GET','PUT','DELETE'])
@csrf_exempt
def article_detail(request, pk) :
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serilizer=ArticleSerializer(article,data=request.data)
        if serilizer.is_valid():
            serilizer.save()
            return Response(serilizer.data )
        return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        article.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

