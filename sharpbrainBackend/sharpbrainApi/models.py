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