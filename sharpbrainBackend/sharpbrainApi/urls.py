from django.urls import path
from . import views

urlpatterns = [
    
    path('otp/', views.otp),
    path('universities_name/', views.universities_name),
    path('course_names/', views.coursesOffered),
    path('jamb_subject_combination/', views.jambAcceptedSubjects),
    path('signup/', views.UserCustomData.as_view()),
    path("material/", views.material),
    path("courses_for_each_dept/", views.Courses_for_each_dept_view.as_view()),
    
    path('users/', views.userAuth),
    path('users/all', views.viewAllUser),
    path('aichat/', views.aichat),

    path('universities_name/<str:pk>/', views.universities_nameDelPut),
    path('course_names/<str:pk>/', views.coursesOfferedDelPut),
    path('jamb_subject_combination/<str:pk>/', views.jambAcceptedSubjectsPutDel),
    
]