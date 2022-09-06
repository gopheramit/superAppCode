
from django.urls import path 
from .views import ArticleAPIView, ArticleDetailsAPIView, GenericArticleView, article_detail, article_list, countries_list,create_gr

urlpatterns = [
    # path('article/', article_list),
    path('article/', ArticleAPIView.as_view()),
    path('generic/article/<int:id>/', GenericArticleView.as_view()),
    # path('detail/<int:pk>/', article_detail),
    path('detail/<int:id>/', ArticleDetailsAPIView.as_view()),
    path('countries/', countries_list),
    path('createPayment/', create_gr),

 
]
