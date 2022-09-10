from dataclasses import field
from http.client import BAD_REQUEST
import imp
import json
from telnetlib import STATUS
# from xml.dom.xmlbuilder import _DOMInputSourceStringDataType
from django.shortcuts import render

from django.http.response import HttpResponse,JsonResponse 
from rest_framework.parsers import JSONParser

from api_basics.utilities.make_request import make_request
from .models import    CustomersData
from .serilizers import    CustomerSerializer, CustomersDataSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins


@api_view(['GET'])
@csrf_exempt
def customers_list(request):
    if request.method=="GET":
        data_response = make_request('get','/v1/customers?limit=100','')
        serizalizer = CustomerSerializer(data_response)
        # print("""serializer iss """)
        # print(serizalizer)
        # print("""""")
        news = serizalizer.data
        for ele in news['data']:
            #print("ele",ele)
            ele = json.dumps(ele)
            #print(ele)
            custdataserializer = CustomersDataSerializer(data = json.loads(ele))
            # custdataserializer = CustomersDataNewSerializer(data = json.loads(ele))
            # print("""""")
            # print(custdataserializer)
            # print(custdataserializer.is_valid())
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
        # else:
        #     return Response(serizalizer.errors,status=BAD_REQUEST)
        return Response(serizalizer.data)


@api_view(['GET'])
@csrf_exempt
def getMerchant(request):
    if request.method=="GET":
        data=[{"ewallet":"ewallet_4cd1ba086af64550aecd05776faea29a","name":"cab wallet","phone_number":"+18888888888"},{"ewallet":"ewallet_f37430011770efc9f31b165865749cfa","name":"Restaurant wallet","phone_number":"+19999999999"}]
        return Response(data)

    
@api_view(['POST'])
@csrf_exempt
def accountTransfer(request):
    if request.method=="POST":
        inputData=request.data
        source_wallet="ewallet_3cce2ff8b6c4250ed8d93512ddcb78de"
        destination_ewallet=inputData["ids"]
        amount=str(inputData["amount"])
        body={"source_ewallet": source_wallet,"amount": amount,"currency": "USD","destination_ewallet":destination_ewallet,"metadata":{"merchant_defined": "true"}}
        data_response = make_request('post','/v1/account/transfer',body)
        print(data_response)
        return Response(status=status.HTTP_201_CREATED)




@api_view(['POST'])
@csrf_exempt
def createGruopPayment(request):
    if request.method=="POST":
        #print("request dat is :  ",request.data)
        inputData=request.data
        cardData1={"number":"4111111111111111","expiration_month":"10","expiration_year":"23","cvv":"123","name":"John"}
        cardData2={"number":"4111111111111111","expiration_month":"10","expiration_year":"23","cvv":"123","name":"Henderson"}
        cardData3={"number":"4111111111111111","expiration_month":"10","expiration_year":"23","cvv":"123","name":"amit"}
        cardData4={"number":"4111111111111111","expiration_month":"10","expiration_year":"23","cvv":"123","name":"Romonovski"}
        cardData5={"number":"4111111111111111","expiration_month":"10","expiration_year":"23","cvv":"123","name":"James"}
        cardData6={"number":"4111111111111111","expiration_month":"10","expiration_year":"23","cvv":"123","name":"Jordan"}
        cardData7={"number":"4111111111111111","expiration_month":"10","expiration_year":"23","cvv":"123","name":"Rivers"}
        cardData8={"number":"4111111111111111","expiration_month":"10","expiration_year":"23","cvv":"123","name":"achal"}
        dictData={}
        dictData["ewallet_c908e65751fe5d29e7d27739d6e447dc"]=cardData1
        dictData["ewallet_ad689618491a6161f5c2e49dcf4aa156"]=cardData2
        dictData["ewallet_e599f93804d5655c485df3f3062dc90b"]=cardData3
        dictData["ewallet_24e46058e7fcaa8ce66b34d094964df9"]=cardData4
        dictData["ewallet_2a42449f995810ed3e35c1a38b773a68"]=cardData5
        dictData["ewallet_5b15058d8e6015c7324edca8b8dfe1a7"]=cardData6
        dictData["ewallet_f49f45152f2081fbccf70052fdd8c9c0"]=cardData7
        dictData["ewallet_c1cf9298de57bafc266805596e1bacde"]=cardData8
        #print(dictData)
        customers=CustomersData.objects.all()
        serilizer=CustomersDataSerializer(customers,many=True)
        #print(json.dumps(serilizer.data))
        AllCustomers=json.dumps(serilizer.data)
        AllCustomers=json.loads(AllCustomers)
        payment_list=[]
        # print("inputdata  --------------------------- ",inputData)
        # print(inputData.ids,"ids")
        amount=int(inputData["amount"])
        n=len(inputData["ids"])
        # print(inputData["amount"],"amount")
        for i in inputData["ids"]:
            dict1={}
            dict1["amount"]=str(round(amount/n))
            dict1["currency"]="USD"
            paymentMethod={}
            paymentMethod["type"]="sg_debit_visa_card"
            ewallets=[]
            for ele in AllCustomers:
                if(i==ele["id"]):
                    ewallet_id=ele["ewallet"]
                    cardDetail=dictData[ewallet_id]
                    paymentMethod["fields"]=cardDetail
                    ewallet={}
                    ewallet["ewallet"]="ewallet_3cce2ff8b6c4250ed8d93512ddcb78de"
                    ewallets.append(ewallet)
                    dict1["payment_method"]=paymentMethod
                    dict1["ewallets"]=ewallets
                    payment_list.append(dict1)
                    #print(ele["ewallet"],"ewallet id")
                    #print(cardDetail,"cardDetail")
        #print(payment_list)
        body={"metadata":{"user_defined":"silver"},"merchant_reference_id":"12345689","payments":[]}
        body["payments"]=payment_list
        #print(body)
        data_response = make_request('post','/v1/payments/group_payments',body)
        #print(data_response)
        #bodySerilizer=CreateGroupSerializer(body)
        #print(bodySerilizer,"bodySerilizer")
        return Response(status=status.HTTP_201_CREATED)
   
        

# @api_view(['POST'])
# @csrf_exempt
# def create_payment(request):
#     if request.method=="POST":
#         inputData=request.data
#         body={"amount":"10","currency":"USD","payment_method":{"type":"sg_debit_visa_card","fields":{"number":"4111111111111111","expiration_month":"10","expiration_year":"23","cvv":"123","name":"rahul"}},"ewallets":[{"ewallet":"","percentage":"100"}],"metadata":{"merchant_defined":"true"}}
#         body["amount"]=inputData["amount"]
#         body["ewallets"][0]["ewallet"]=inputData["id"]
#         print(body)
#         data_response = make_request('post','/v1/payments',body)
#         print(data_response)
#         return Response(status=status.HTTP_201_CREATED)

