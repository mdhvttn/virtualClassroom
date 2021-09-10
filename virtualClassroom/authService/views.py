from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import profile
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status


# Create your views here.



class register(APIView):

    def createUser(self,user,role):
        profile.objects.create(user=user,role=role)
        return "Created"

    
    def post(self,request):
        
        uname = ""
        password = ""
        role = ""
    

        uname = request.data['name']
        password = request.data['password']
        role = request.data['role']

     
        if len(uname) == 0 or len(password) == 0 or len(role) == 0:
            return Response({'msg':'Please enter correct format'},status=status.HTTP_400_BAD_REQUEST)
        elif role != 'teacher' and role!='student':
            return Response({'msg':'Role either be teacher or student'},status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                user = User.objects.create(username=uname)
                user.set_password(password)
                try:
                    user.save()
                    if self.createUser(user,role) == "Created":
                        print("yes")
                        refresh = RefreshToken.for_user(user)
                        print(refresh)
                        return Response({'refresh': str(refresh),'access': str(refresh.access_token),})
                except:
                    return Response({'msg':'Something Went wrong'})

            except:
                return Response({'msg':'user already registered'},status=status.HTTP_409_CONFLICT)












