from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.RegisterAPIView.as_view()),
    path('authorization/', views.AuthAPIView.as_view()),

]