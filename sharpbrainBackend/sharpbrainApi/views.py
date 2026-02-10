from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import SignupSerializers
from .models import SignUp

@api_view(['GET'])
def models_in_json(request):
    signupObj = SignUp.objects.all()
    serializer = SignupSerializers(signupObj, many = True)
    return Response(serializer.data) 



@api_view(['GET'])
def data1(request, pk):
    objects = SignUp.objects.get(id = pk)
    serializer = SignupSerializers(objects)
    return Response(serializer.data)

@api_view(['POST'])
def create(request):
    toCreate = request.data
    objects = SignUp.objects.create(
        surname = toCreate['surname'],
        otherName = toCreate['otherName']
    )
    serializer = SignupSerializers(objects, many = False)
    return Response(serializer.data)