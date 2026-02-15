from rest_framework.serializers import ModelSerializer
from .models import SignUp, Universities_name, CourseNames, JambAcceptedSubjectCombination


class SignupSerializers(ModelSerializer):
    class Meta:
        model = SignUp
        fields = '__all__'
    
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