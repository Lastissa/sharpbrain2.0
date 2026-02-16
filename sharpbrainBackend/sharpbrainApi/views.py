from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import SignUp, Universities_name, CourseNames

@api_view(['GET'])
def show_data(request):
    signupObj = SignUp.objects.all()
    serializer = SignupSerializers(signupObj, many = True)
    return Response(serializer.data)



# @api_view(['GET'])
# def data(request, pk):
#     objects = SignUp.objects.get(id = pk)
#     serializer = SignupSerializers(objects)
#     return Response(serializer.data)

# @api_view(['POST'])
# def create(request):
#     toCreate = request.data
#     objects = SignUp.objects.create(
#         surname = toCreate['surname']
#     )
#     serializer = SignupSerializers(objects, many = False)
#     return Response(serializer.data)


# @api_view(['PUT'])
# def update(request, pk):
#     inFoToUpdate = request.data
#     objects = SignUp.objects.get(id = pk)
#     serializer = SignupSerializers(objects, data = inFoToUpdate)
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)


# @api_view(['DELETE'])
# def delete (request, pk):
#     if pk == '*':
#         SignUp.objects.all().delete()
#         return Response('Everything have been deleted')
#     else:
#         objects = SignUp.objects.get(id = pk)
#         objects.delete()
#         return Response(f'{pk} have been deleted')
    
    
    
@api_view(['POST', 'GET',])
def universities_name(request):
    if request.method == 'POST':
        dataToUpload = request.data.get('name_of_universities', '').lower().strip()# Used the empty string incase django did not get uni names and it cannot return the nonetype.lowercase
        objects = Universities_name.objects.create(
            name_of_universities = dataToUpload
        )
        serializer = universitiesNameSerializer(objects, many = False)
        return Response(serializer.data)
    elif request.method == 'GET':
        objects = Universities_name.objects.all()
        serializer = universitiesNameSerializer(objects, many = True)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        objects = Universities_name.objects
        
@api_view(['DELETE', 'PUT'])
def   universities_nameDelPut(request, pk):
       if request.method == 'DELETE':
            objects = Universities_name.objects.get(id = pk)
            objects.delete()
            return Response(
            {'result' : f'id{pk} have been deleted'}
        )
        
       elif request.method == 'PUT':
           objects = Universities_name.objects.get(id = pk)
           serializer = universitiesNameSerializer(objects, data = request.data)
           if serializer.is_valid():
               serializer.save()
           return Response(serializer.data)
       return(Response.errors)
           
       
@api_view(['GET','POST'])
def coursesOffered(request):
    if request.method == 'POST':
        objects = CourseNames.objects.create(
            name_of_uni = request.data['name_of_uni'],
            courses_offered = request.data['courses_offered']
        )
        serializer = CourseNameSerializer(objects, many = False)
        return Response(serializer.data)
    
    if request.method == 'GET':
        data = Universities_name.objects.all()
        objects = CourseNames.objects.all()
        serializer = CourseNameSerializer(objects, many = True)
        return Response(serializer.data)

@api_view(['DELETE', 'PUT'])
def coursesOfferedDelPut(request, pk):
    if request.method == 'PUT':
        objects = CourseNames.objects.get(id = pk)
        serializer = CourseNameSerializer(objects, data=request.data, many = False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    return Response(serializer.errors)


@api_view(['GET', 'POST'])
def jambAcceptedSubjects(request):
    if request.method == 'POST':
        existsAlready = JambAcceptedSubjectCombination.objects.filter(uni_name = request.data['uni_name'], course_name = request.data['course_name']).exists()
        if existsAlready:
            return Response(f"""uni and course already exist
uni is {request.data['uni_name']} 
course  is {request.data['course_name']}""")
        else:
            objects = JambAcceptedSubjectCombination.objects.create(
                uni_name =request.data['uni_name'],
                course_name = request.data['course_name'],
                subject_combination  = request.data['subject_combination']

            )
            serializer = JambAcceptedSubjectCombinationSerializer(objects, many = False)
            return Response(serializer.data)
    else:#request will be treated as GET
        objects = JambAcceptedSubjectCombination.objects.all()
        serializer = JambAcceptedSubjectCombinationSerializer(objects, many = True)
        return Response(serializer.data)
        
        
@api_view(["PUT", "DELETE"])
def jambAcceptedSubjectsPutDel(request,pk):
    if request.method == "DELETE":
        pass
    elif request.method == "PUT":
        objects = JambAcceptedSubjectCombination.objects.get(id = pk)
        serializer = JambAcceptedSubjectCombinationSerializer(objects, data = request.data, many = False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.error)
         