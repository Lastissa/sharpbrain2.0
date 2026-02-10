from django.urls import path
from . import views

urlpatterns = [
    path('', views.models_in_json),
    path('data1/<str:pk>/', views.data1),
    path('create/', views.create)
]