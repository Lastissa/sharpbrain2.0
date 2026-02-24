from django.db import models
from django.contrib.auth.models import User
    
class Universities_name(models.Model):
    name_of_universities = models.CharField(max_length=150, unique=True, blank= False, null= False)
    def __str__(self):
        return self.name_of_universities
    
class CourseNames(models.Model):
    name_of_uni = models.CharField(max_length=150, unique=True, blank=False, null=False)
    courses_offered = models.JSONField(default= list)    
    def __str__(self):
        return "CourseNames"
    
    
class JambAcceptedSubjectCombination(models.Model):
    uni_name = models.CharField(max_length= 100,blank=False, null=False)
    course_name = models.CharField(max_length= 100,blank=False, null=False)
    subject_combination = models.JSONField(default=list, null= False)
    core_subjects = models.JSONField(default=list, null= False)
    def __str__(self):
        return "JambAcceptedSubjectCombination"


class signupData(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)#THIS IS TO LINK THE DATA IN USER TO MY CUSTOM USER 
    yearOfBirth = models.PositiveSmallIntegerField(blank= False, null= False)
    monthOfBirth = models.CharField(blank= False, null= False, max_length= 15)
    dateOfBirth = models.PositiveSmallIntegerField(blank= False, null= False)
    Universities_name = models.CharField(max_length=100,blank= False, null=False )
    dept_name = models.CharField(max_length=100,blank= False, null=False )
    level = models.CharField(max_length=100,blank= False, null=False )
    
    def __str__(self):
        return "signupData"