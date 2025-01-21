from django.urls import path
from . import views
from utils.constants import LIST_CREATE, RETRIEVE_UPDATE_DESTROY

urlpatterns = [
    path('', views.product_list_api_view),
    path('<int:id>/', views.product_detail_api_view),
    path('categories/', views.CategoryListAPIView.as_view()),
    path('categories/<int:id>/', views.CategoryDetailAPIView.as_view()),
    path('search_words/', views.SearchWordViewSet.as_view(LIST_CREATE)),
    path('search_words/', views.SearchWordViewSet.as_view(RETRIEVE_UPDATE_DESTROY)),
]