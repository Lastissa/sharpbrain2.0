import django
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .models import Universities_name, CourseNames, SignUpData, Materials, CoursesForEachDept
from google import genai
from dotenv import load_dotenv
from pathlib import Path
import os
import random
from django.core.mail import send_mail
from django.contrib.auth.models import User as myUsers
from django.http import FileResponse

env_location = Path(__file__).resolve().parent.parent
load_dotenv(env_location/'.env')
api_key = os.getenv('API_KEY').strip()


"""
I WANT TO TURN ALL MY VIEWS TO CLASS BASED BUT JUST TO I REMEMBER WHAT FUNCTION BASED IS,
I WILL LEAVE UNIVERSITIES NAEM AS FUNCTION BASED VIEW BUT TURN THE REST TO CLASS BASED VIEW AS FUNCTION BASED IS MAKING MY CODE LOOK DIRTY
BUT OMO, THIS THING GO FAR, I WILL DO THE TASK LATER
"""

@api_view(['POST', 'GET',])
def universities_name(request):
    if request.method == 'POST':
        dataToUpload = request.data.get('name_of_universities', '').upper().strip()# Used the empty string incase django did not get uni names and it cannot return the nonetype.lowercase
        objects = Universities_name.objects.create(
            name_of_universities = dataToUpload
        )
        serializer = universitiesNameSerializer(objects, many = False)
        return Response(serializer.data)
    elif request.method == 'GET':
        objects = Universities_name.objects.all()
        serializer = universitiesNameSerializer(objects, many = True)
        return Response(serializer.data)
    
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
         
         
ai = genai.Client(api_key= api_key)
@api_view(['POST'])
def aichat(request):
    data_from_request = request.data
    message = data_from_request.get('message', '')
    ai_name = data_from_request.get('ai_name', '')
    history = data_from_request.get('history','')
    
    if ai_name is None or ai_name.strip() == '':
        ai_name = 'Tis'
    
    
    try:
        if len(history['user']) == 0:
            ai_response = ai.models.generate_content(model= 'gemini-2.5-flash', contents= f"""
# IDENTITY
You are {ai_name}, a world-class Academic Tutor with deep expertise across all subjects. 

# STYLE GUIDELINES
- Tone: Professional, encouraging, and scholarly.
- Detail: Be compact but highly detailed. Provide "meat" in your answers without fluff.
- Engagement: Every few messages, briefly remind the user that they can change your name. 
- Current Name: Always remember your name is {ai_name}.

# TASK
Answer the user's question as a tutor would, explaining complex concepts simply but thoroughly.
user's question: {message}
""")

        
        else:
            print('true')
            ai_response = ai.models.generate_content(model= 'gemini-2.5-flash', contents= f"""
# STYLE GUIDELINES
- Tone: Professional, encouraging, and scholarly.
- Engagement: Every few messages, briefly remind the user that they can change your name And if your name is changed ?inform the user breifly as they changed your name in this current interaction, it wont be permenent unless they do the changes in 'app setting'. 
- Current Name: Always remember your name is {ai_name}.

#CHAT HISTORY
    look into {history} for context on the user's learning journey and previous interactions. Use this to inform your response, ensuring continuity and relevance. where {history['user']} is the user's previous messages and {history['AI']} is your previous responses.
    #task: 
    
    Answer the user's current question as a tutor would, building on the context from the chat history. Provide brief but detailed explanations and insights, ensuring your response is informed by the user's learning journey and previous interactions.
    current question: {message}
                                                      """)
        
    except genai.errors.ClientError as e:
        if "429" in str(e):
            return Response({
        "ai_response" : "I'm a bit overwhelmed! Give me a minute to breathe or suscribe for infinite oxygen tank.",
        "token_count" : 0
    })
        else:
            return Response({
                "ai_response" : f"{e}",
                "token_count" : 0
            })
            
    return Response({
        "ai_response" : ai_response.text,
        "token_count" : 0
    })
  
@api_view(['POST'])
def otp(request):
    try:
        email = request.data.get('email', '')
        surName = request.data['surname']
        firstName = request.data['firstname']
        userExist = SignUpData.objects.filter(user__username = email.upper()).exists()
        if userExist:
            send_mail("Welcome Back SharpBrainer", f"""
This email is already been used by another sharpbrainer, please change email or proceed to login if you are the owner of this email""",
django.conf.settings.DEFAULT_FROM_EMAIL,
[email]
)
            return Response({
                "message" : "Email Already In Use",
                "otp" : random.randint(1234567, 12345678)
            })
        otp = random.randint(10000,99999)
        # cache.set(email, otp, timeout=400)  # Store OTP in cache for 5 minutes
        send_mail(
        'Your OTP Code From SharpBrain',
        f"""Dear {surName.upper()} {firstName.upper()}, your otp code is {otp}, it expires in 5 minutes\nIf you wan dare me let that five minute pass.
if the name does not match your name, just ignore this mail, Thank you.
""",
        django.conf.settings.DEFAULT_FROM_EMAIL,
        [email])
        return Response({'message': 'OTP sent to email.',
                         'otp': otp})
    except Exception as e:
        return Response({'message': f'Failed to send OTP: {str(e)}', 'otp': 0}, )

#for default auth django provides # built only for login, custom user account for signup and probably other features
@api_view(['POST', 'GET','PUT', 'DELETE', 'PATCH'])
def userAuth(request):
    if request.method == 'GET':
        try:
            typed_email = 'LASTISSA11@GMAIL.COM'#request.data.get('email', '')
            typed_password = 'Realmadrid123'#request.data.get('password', '')
            if typed_email and typed_password:
                objects = myUsers.objects.get(username = typed_email.upper())
                if objects.check_password(typed_password):
                    serializer = UserSerializer(objects, many = False)
                    return Response({'message' : 'success', 'id' : str(serializer.data['username'])})
            return Response({'message' : 'email and password is required'})
        except Exception as e:
            return Response({
                'message' : f'{e}'
            })
            
    if request.method == 'POST':
        user_email = request.data['email']
        firstName = request.data['firstName']
        surName = request.data['surName']
        password = request.data['password']
        objects = myUsers.objects.create_user(
            username = user_email.upper(),
            first_name = firstName.upper(),
            last_name = surName.upper(),
            email = user_email.upper(),
            password = password
        )#this could have been replaced by the serializer.save() as it calls the update / create automatically depending of wether my serilizer have data or not
        serializer = UserSerializer(objects, many = False)
        return Response(serializer.data)
    
    if request.method == 'PATCH':
        user_email = request.data.get('email', '').upper()
        rowToUpdate = myUsers.objects.get(username = user_email) #since email is same as username
        serializer = UserSerializer(rowToUpdate, data = request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message' : 'success, password updated succcesfuly'})
        
        return Response({'message' : 'Password not updated'})
    
    if request.method == 'DELETE':
        user_email = request.data.get('email')
        password = request.data.get('password')
        if user_email:
            rowToDelete = User.objects.get(username = user_email.upper())
            if rowToDelete.check_password(password):
                rowToDelete.delete()
                return Response({'message' : 'Account Deleted'})
        return Response({'message' : 'incorrect  credentials, failed to delete'})
        

@api_view(['GET'])
def viewAllUser(request):
    objects = myUsers.objects.all()
    serializer = UserSerializer(objects, many = True)
    return Response(serializer.data)

# @api_view(["GET"])
# def userExist


#for other feilds i need to save during registration that django does not provide
class UserCustomData(APIView):
    def get(self, request):
        user_email = request.query_params.get("email", "").upper()
        password = request.query_params.get("password")
        userMainModel = SignUpData.objects.get(user__username = user_email)#Could have used a try or except but this is the best appraoch as per it returns none, and the .first() literally mean ut should return the first item it find with the said data
        if userMainModel:
            if userMainModel.user.check_password(password):
                serializer = signupSerializer(userMainModel, many = False)
                secondObject= User.objects.get(id = int(userMainModel.user.id))
                secondSerializer = UserSerializer(secondObject, many = False)
                return Response({"message" : "success", **serializer.data, **secondSerializer.data})
            return Response({"message": "wrong password"})
        return Response({"message" : "no user"})
    def post(self, request):
        user_first_name = request.data.get("first_name").upper().strip()
        user_surname = request.data.get("surname").upper().strip()
        user_email = request.data.get("email", "").upper().strip()
        user_year_of_birth  = request.data.get('yearOfBirth')
        user_month_of_birth = request.data.get("monthOfBirth", "").upper().strip()
        user_date_of_birth = request.data.get("dateOfBirth")
        user_university = request.data.get("Universities_name", "").upper().strip()
        user_dept = request.data.get("dept_name", "").upper().strip()
        user_level = request.data.get("level", "").upper().strip()
        try:
            user_password = request.data['password']
        except Exception as e:
            return Response(status= 400)#400 mean i heard you but i no fit do wetin u want make i do ; bad request
        try:
            if_email_already_in_db = SignUpData.objects.get(user__username = user_email)
        except:
            if_email_already_in_db = None

        if len(user_email) > 0 and if_email_already_in_db == None:#all verification that the data is genuine have been done, about to update db
            serializer = signupSerializer(data = {
                "yearOfBirth" : user_year_of_birth,
                "monthOfBirth" : user_month_of_birth,
                "dateOfBirth" : user_date_of_birth,
                "Universities_name" : user_university,
                "dept_name" : user_dept,
                "level" : user_level,
            })
            if serializer.is_valid():
                userAuthObject = myUsers.objects.create_user(first_name = user_first_name,last_name = user_surname,username= user_email, email=user_email, password = user_password)
                serializer.save(user = userAuthObject)
                return Response({"message" : "success", "data" : [serializer.data]})
            else:
                return Response({"message" : "Serializer not valid", "error" : serializer.errors})
        elif if_email_already_in_db != None:
            return Response({"message" : "email already exist"})
        else:
            return Response({"message" : "error uploading"})
        
        
        

@api_view(["POST",'GET'])
def material(request):
    if request.method == "GET":#return three things : (1) -> file_name(if file foes not exiat, return file_name as no_file)
        file_name = request.data.get("file_name", "").upper()
        if_file_exist = Materials.objects.filter(file_name = file_name).exists()
        if len(file_name) > 1 and if_file_exist:
            object = Materials.objects.get(file_name = file_name)
            serializer = MaterialSerializer(object, many = False)
            return Response(serializer.data) #FileResponse() #Does not really understand how the file response work, come back later to solve
        
        return Response({"file_name" : "invalid", "file_data" : None, "file_type" : None})
    elif request.method == "POST":
        file_name = request.data.get("file_name").upper()
        file_type = request.data.get("file_type").upper()
        file_data = request.data.get("file_data")
        serializer = MaterialSerializer(data = request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
           serializer.errors
        )
        
        
        
class Courses_for_each_dept_view(APIView):
    def post(self, request):
        try:
            dept_name = request.data.get("dept_name", "").upper().strip()
            uni_name =  request.data.get("uni_name", "").upper().strip()
            first_semester_courses =  request.data.get("first_semester_courses")
            second_semester_courses =  request.data.get("second_semester_courses")
            try:
                dataExist = CoursesForEachDept.objects.get(uni_name = uni_name, dept_name = dept_name)
                dataExist = False
                return Response({"message" : "data exist"})
            except:
                objects = CoursesForEachDept.objects.create(uni_name = uni_name, dept_name = dept_name, first_semester_courses =first_semester_courses, second_semester_courses = second_semester_courses)
                serializer = CoursesForEachDeptSeriaizer(objects, many = False)
                return Response(serializer.data)
            
            
        except Exception as e:
            return Response({"message" : str(e)})
        

           
    def get(self, request):
        dept_name_ =request.query_params["dept_name"]
        uni_name_ =request.query_params["uni_name"]
        try:
            objects = CoursesForEachDept.objects.get(uni_name = uni_name_.strip().upper(), dept_name =dept_name_.strip().upper())
            serializer = CoursesForEachDeptSeriaizer(objects, many = False)
            return Response({"message" : "successful", **serializer.data})
        except Exception as e:
           
            return Response({"message": f"{e}"})
       
        