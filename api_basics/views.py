from email.policy import HTTP
from http.client import TEMPORARY_REDIRECT
import json
from types import new_class
from api_basics.utilities.make_request import make_request
from .models import CustomersData, TransactionData
from .serilizers import CustomerSerializer, CustomersDataSerializer, TransactionsSerializer,TransactionDataResponseSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
@csrf_exempt
def customers_list(request):
    if request.method=="GET":
        data_response = make_request('get','/v1/customers?limit=100','')
        serizalizer = CustomerSerializer(data_response)
        news = serizalizer.data
        for ele in news['data']:
            ele = json.dumps(ele)
            custdataserializer = CustomersDataSerializer(data = json.loads(ele))
            if custdataserializer.is_valid():
                custdataserializer.save()
        # data=[]
        # for i in news['data']:
        #     print(i)
        #     if(i["ewallet"]==""):
        #         data.append(i["id"])
        # for j in data:
        #      data_response = make_request('delete','/v1/customers/'+j,'')

        return Response(serizalizer.data,status=status.HTTP_201_CREATED)


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
        responseData={}
        responseData["amount"]=str(inputData["amount"])
        responseData["id"]=data_response["data"]["id"]
        responseData["status"]=data_response["data"]["status"]

        return Response(responseData,status=status.HTTP_201_CREATED)


@api_view(['POST'])
@csrf_exempt
def setTransferResponse(request):
    if request.method=="POST":
        inputData=request.data
        id=inputData["id"]
        body={"id":id,"metadata":{"merchant_defined":"accepted"},"status":"accept"}
        data_response = make_request('post','/v1/account/transfer/response',body)
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
        amount=(inputData["amount"])
        n=len(inputData["ids"])
        # print(inputData["amount"],"amount")
        for i in inputData["ids"]:
            dict1={}
            dict1["amount"]=str(amount/n)
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
        body={"metadata":{"user_defined":"silver"},"merchant_reference_id":"12345689","payments":[]}
        body["payments"]=payment_list
        #print(body)
        data_response = make_request('post','/v1/payments/group_payments',body)
        print(data_response)
        #bodySerilizer=CreateGroupSerializer(body)
        #print(bodySerilizer,"bodySerilizer")
        return Response(status=status.HTTP_201_CREATED)
   

@api_view(['GET'])
@csrf_exempt
def customers_notNeeded_list(request):
    if request.method=="GET":
        articles=TransactionData.objects.all()
        serilizer=TransactionsSerializer(articles,many=True)
        return Response(serilizer.data)
        
@api_view(['GET','POST'])
@csrf_exempt
def transactionList(request):
    if request.method=="GET":
        articles=TransactionData.objects.all()
        serilizer=TransactionsSerializer(data=articles,many=True)
        print(serilizer.is_valid(),"get serilizer")
        data=[]
        for i in serilizer.data:
            temp={}
            if(i["name"]=="Rahul"):
                temp["source"]=i["destination"]
                temp["amount"]= -(i["amount"])
                temp["destination"]=i["source"]
                temp["name"]=i["destinationName"]
            elif(i["destinationName"]=="Rahul"):
                temp["source"]=i["source"]
                temp["amount"]=(i["amount"])
                temp["destination"]=i["destination"]
                temp["name"]=i["name"]
            if(len(temp)>0):
                data.append(temp)
        print(data,"datatatatttttttttttttttttttttttttttttttttttttttttttt")
        serilizerpost=TransactionDataResponseSerializer(data=data,many=True)
        if serilizerpost.is_valid():
            # serilizerpost.save()
            return Response(serilizerpost.data ,status=status.HTTP_201_CREATED)
        return Response(serilizerpost.errors,status=status.HTTP_400_BAD_REQUEST)

        # return Response(serilizer.data)
    elif request.method=="POST":
        inputData=request.data
        articles=TransactionData.objects.all()
        serilizer=TransactionsSerializer(articles,many=True)
        ListData=[]
        data= {}
        Newarticles=serilizer.data
        sourceList = []
        destinationList=[]
        sourceDestToAmount = {}
        keysfordict = []
        for ele in Newarticles:
            # sourceDest = {}
            sourceList.append(ele["source"])
            # sourceAndAmount[ele["source"]] = ele["amount"]
            destinationList.append(ele["destination"])
            sd = ele["source"]+ele["destination"]
            sourceDestToAmount[sd]=ele["amount"]
            # print("Sourcedest dict is **",sourceDest)

            # sourceDestToAmount.pus(sourceDest)
            # print("***************************************",setSourceList,"-----",setDestinationList)
            # destinationAndAmount[ele["destination"]]=ele["amount"]
        print(sourceDestToAmount)
        for keys,values in sourceDestToAmount.items():
            keysfordict.append(keys)
        for item in inputData:
            sourceItem=item["source"]
            destinationItem=item["destination"]
            # print(''''
            
            # ''',(sourceItem+destinationItem in keysfordict),(destinationItem+sourceItem in keysfordict),(destinationItem+sourceItem))
            if (sourceItem+destinationItem) in keysfordict:
                print('''
                Inside source dest
                ''')
                finalamount = sourceDestToAmount[(sourceItem+destinationItem)] + item["amount"]
                TransactionData.objects.filter(destination = destinationItem, source = sourceItem).update(amount=(finalamount))  
            elif (destinationItem+sourceItem) in keysfordict:
                print('''
                Inside  dest source
                ''')
                finalamount = sourceDestToAmount[(destinationItem+sourceItem)] - item["amount"]
                TransactionData.objects.filter(destination = sourceItem, source = destinationItem).update(amount=(finalamount))            
                # print(item,"else itemmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm")
            else:
                data={}
                data["source"]=item["source"]
                data["amount"]=(item["amount"])
                data["destination"]=item["destination"]
                data["name"]=item["name"]
                data["destinationName"]=item["destinationName"]
                # print(data,"data insertionnnnnnnnnnnnnnnnnnnn")
                ListData.append(data)

        print(ListData,"ListDAraaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        serilizerpost=TransactionsSerializer(data=ListData,many=True)
        if serilizerpost.is_valid():
            serilizerpost.save()
            return Response(serilizerpost.data ,status=status.HTTP_201_CREATED)
        return Response(serilizerpost.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@csrf_exempt
def createSalaryPayment(request):
    if request.method=="POST":
        #print("request dat is :  ",request.data)
        inputData=request.data
        cardData1={"number":"4111111111111111","expiration_month":"10","expiration_year":"23","cvv":"123","name":"rahul"}
        customers=CustomersData.objects.all()
        serilizer=CustomersDataSerializer(customers,many=True)
        #print(json.dumps(serilizer.data))
        AllCustomers=json.dumps(serilizer.data)
        AllCustomers=json.loads(AllCustomers)
        payment_list=[]
        amount=int(inputData["amount"])
        # n=len(inputData["ids"])
        # print(inputData["amount"],"amount")
        for i in inputData["ids"]:
            dict1={}
            dict1["amount"]=str(amount)
            dict1["currency"]="USD"
            paymentMethod={}
            paymentMethod["type"]="sg_debit_visa_card"
            ewallets=[]
            for ele in AllCustomers:
                if(i==ele["id"]):
                    ewallet_id=ele["ewallet"]
                    #cardDetail=dictData[ewallet_id]
                    paymentMethod["fields"]=cardData1
                    ewallet={}
                    ewallet["ewallet"]=ewallet_id
                    ewallets.append(ewallet)
                    dict1["payment_method"]=paymentMethod
                    dict1["ewallets"]=ewallets
                    payment_list.append(dict1)
        body={"metadata":{"user_defined":"silver"},"merchant_reference_id":"12345689","payments":[]}
        body["payments"]=payment_list
        #print(body)
        data_response = make_request('post','/v1/payments/group_payments',body)
        #print(data_response)
        #bodySerilizer=CreateGroupSerializer(body)
        #print(bodySerilizer,"bodySerilizer")
        return Response(status=status.HTTP_201_CREATED)
   

@api_view(['POST'])
@csrf_exempt
def settleUp(request):
    if request.method=="POST":
        inputData=request.data
        print(inputData,"input daRa")
        cusid=inputData["source"]
        amount=str(inputData["amount"])
        articles=CustomersData.objects.all()
        serilizer=CustomersDataSerializer(articles,many=True)
        for i in serilizer.data:
            if(i["id"]==cusid):
                destination_ewallet=i["ewallet"]

        print(destination_ewallet,"destination wallet")
        source_wallet="ewallet_3cce2ff8b6c4250ed8d93512ddcb78de"
        body={"source_ewallet": source_wallet,"amount": amount,"currency": "USD","destination_ewallet":destination_ewallet,"metadata":{"merchant_defined": "true"}}
        data_response = make_request('post','/v1/account/transfer',body)
        print(data_response)
        responseData={}
        responseData["amount"]=str(inputData["amount"])
        responseData["id"]=data_response["data"]["id"]
        responseData["status"]=data_response["data"]["status"]
        responseData["source"]=cusid
        return Response(responseData,status=status.HTTP_201_CREATED)
        # return Response(status=status.HTTP_201_CREATED)


@api_view(['POST'])
@csrf_exempt
def settleUpConfirm(request):
    if request.method=="POST":
        inputData=request.data
        id=inputData["id"]
        body={"id":id,"metadata":{"merchant_defined":"accepted"},"status":"accept"}
        data_response = make_request('post','/v1/account/transfer/response',body)

        TransactionData.objects.filter(source=inputData['source']).update(amount=(0))
        return Response(status=status.HTTP_201_CREATED)
        # (data_response)


