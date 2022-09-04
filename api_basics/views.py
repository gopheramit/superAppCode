from django.shortcuts import render

from django.http.response import HttpResponse,JsonResponse 
from rest_framework.parsers import JSONParser
from .models import Article
from .serilizers import ArticleSerializer

# Create your views here.

def article_list(request):
    if request.method=="GET":
        articles=Article.objects.all()
        serilizer=ArticleSerializer(articles,many=True)
        return JsonResponse(serilizer.data, safe=False)

    elif request.method=="POST":
        data=JSONParser().parse(request)
        serilizer=ArticleSerializer(data=data)

        if serilizer.is_valid():
            serilizer.save()
            return JsonResponse(serilizer.data ,status=201)
        return JsonResponse(serilizer.errors,status=400)


