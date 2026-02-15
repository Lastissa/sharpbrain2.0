from django.db import models

class SignUp(models.Model):
    surname = models.CharField(max_length=100, null = True)
    otherName = models.CharField(max_length= 200, null = True)
    userEmail = models.EmailField(null = True)
    yearOfBirth = models.PositiveSmallIntegerField( null = True)
    monthOfBirth = models.CharField(max_length=20, null = True)
    dateOfBirth = models.PositiveSmallIntegerField(null = True)
    universityName = models.CharField(max_length=100, null = True)
    deptName = models.CharField(max_length=50, null = True)
    currentLevel = models.CharField(max_length=20, null = True)
    
    def __str__(self):
        return self.surname
    
    
    
class Universities_name(models.Model):
    
    name_of_universities = models.CharField(max_length=150, unique=True, blank= False, null= False)
    
    def __str__(self):
        return self.name_of_universities
    
class CourseNames(models.Model):
    name_of_uni = models.CharField(max_length=150, unique=True, blank=False, null=False)
    courses_offered = models.JSONField(default= list)
    
    
class JambAcceptedSubjectCombination(models.Model):
    uni_name = models.CharField(max_length= 100,blank=False, null=False)
    course_name = models.CharField(max_length= 100,blank=False, null=False)
    subject_combination = models.JSONField(default=list, null= False)