from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.register_api_view),
    path('authorization/', views.authorize_api_view),

]