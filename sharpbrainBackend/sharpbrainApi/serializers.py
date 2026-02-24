from rest_framework.serializers import ModelSerializer
from .models import Universities_name, CourseNames, JambAcceptedSubjectCombination, signupData
from django.contrib.auth.models import User



class universitiesNameSerializer(ModelSerializer):
    class Meta:
        model  = Universities_name
        fields = '__all__'
        
        
class CourseNameSerializer(ModelSerializer):
    class Meta:
        model = CourseNames
        fields = '__all__'
        
        
class JambAcceptedSubjectCombinationSerializer(ModelSerializer):
    class Meta:
        model  = JambAcceptedSubjectCombination
        fields = '__all__'
        
        
        
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'#u can use list if you dont want all
        
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
            return super().update(instance, validated_data)# this have called the instance.save() already
            
    # def create(self, validated_data):
    #     return super().create_user(**validated_data)
    #i choose not to use the create function cos some of my data have to be in uppercase so i will write them manually myself
    
    
class signupSerializer(ModelSerializer):
    class Meta:
        model = signupData
        fields = "__all__"
        
    def create(self, validated_data):
         return super().create() # return signunupdata.objects.create(**validated data)
         
        
        