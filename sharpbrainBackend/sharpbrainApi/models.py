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


class SignUpData(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)#THIS IS TO LINK THE DATA IN USER TO MY CUSTOM USER 
    yearOfBirth = models.PositiveSmallIntegerField(blank= False, null= False)
    monthOfBirth = models.CharField(blank= False, null= False, max_length= 15)
    dateOfBirth = models.PositiveSmallIntegerField(blank= False, null= False)
    Universities_name = models.CharField(max_length=100,blank= False, null=False )
    dept_name = models.CharField(max_length=100,blank= False, null=False )
    level = models.CharField(max_length=100,blank= False, null=False )
    
    def __str__(self):
        return "signupData"
    
class Materials(models.Model):#this model can take in any kind of file but the file format should always be either pdf or msword file
    file_name = models.CharField(max_length= 200, blank= False, null= False, unique= True)# Name that the file will be saved as in my own case , flutter will save it as this
    file_data = models.BinaryField()#Container for the raw binary of the pdf/word, used the open method to convert the normal file to binary
    file_type = models.CharField(max_length=100, blank= False, null= False, )#The type of file it is ; Two option only ? pdf or word.
    
    def __str__(self):
         return "materials"
     
     
class CoursesForEachDept(models.Model):
    dept_name = models.CharField(max_length= 150, blank= False, null= False)
    uni_name = models.CharField(max_length= 150, blank= False, null= False)
    first_semester_courses = models.JSONField(default= list)
    second_semester_courses = models.JSONField(default= list)

    