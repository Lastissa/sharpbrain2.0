from django.urls import path
from . import views

urlpatterns = [
    # path('', views.show_data),
    # path('create/', views.create),
    path('universities_name/', views.universities_name),
    path('course_names/', views.coursesOffered),
    path('jamb_subject_combination/', views.jambAcceptedSubjects),
    path('aichat/', views.aichat),
    path('universities_name/<str:pk>/', views.universities_nameDelPut),
    path('course_names/<str:pk>/', views.coursesOfferedDelPut),
    path('jamb_subject_combination/<str:pk>/', views.jambAcceptedSubjectsPutDel),
    # path('update/<str:pk>',views.update),
    # path('delete/<str:pk>',views.delete),
    # path('<str:pk>/', views.data),
]