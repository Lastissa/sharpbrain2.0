from rest_framework.serializers import ModelSerializer
from .models import SignUp


class SignupSerializers(ModelSerializer):
    class Meta:
        model = SignUp
        fields = '__all__'
    