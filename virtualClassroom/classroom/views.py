from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import *
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
# from rest_framework.authentication import BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from authService.models import profile
from django.core.exceptions import ValidationError
from datetime import *
import json
     
            

class CURDbyTeacher(APIView):
    authentication_classes = [JWTAuthentication]

    permission_classes = (IsAuthenticated,)

    def post(self,request):
        user = request.user
        userDetails = profile.objects.get(user=user)

        if userDetails.role == 'student':
            return Response({'msg':'you have no right to create the assigment'},status=status.HTTP_401_UNAUTHORIZED)
        print(request.data)
        description = request.data['description']
        assigned_to = request.data['assigned_to']
        title = request.data['title']
        deadline = request.data['deadline']
        published_at = request.data['published_at']

        if len(description) == 0 or len(assigned_to) == 0 or len(title) == 0:
            return Response({'msg':'Data format is not correct'},status=status.HTTP_400_BAD_REQUEST)
        if deadline < str(date.today()) or deadline < published_at:
            return Response({'msg':'Deadline cannot be lesser than today data'},status=status.HTTP_400_BAD_REQUEST)
        if str(published_at)<str(date.today()):
            return Response({'msg':'Published date can not be lesser than today\'s date'},status=status.HTTP_400_BAD_REQUEST)

        try:
            if published_at > str(date.today()):
                status = 'SCHEDULED'
            else:
                status = 'ONGOING'
            print(status)
            obj = Assignments.objects.create(description=description,title=title,assigned_by=userDetails,deadline=deadline,published_at=published_at,status=status)        
        except:
            return Response({'msg':'Something went wong'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        #assign to student
        for stu in assigned_to:
            userId = User.objects.get(username=stu)
            userProfile = profile.objects.get(user=userId)
            obj.assigned_to.add(userProfile)
        obj.save()
        return Response({"msg":"Assigment Created!!"},status=status.HTTP_200_OK)
            
    def put(self,request,pk):
        user = request.user
        userDetails = profile.objects.get(user=user)
        if userDetails.role == 'student':
            return Response({'msg':'you have no right to update the assigment'},status=status.HTTP_403_FORBIDDEN)
        
        temp = ['description','assigned_to','title','deadline','published_at']
        
        description = request.data['description']
        assigned_to = request.data['assigned_to']
        title = request.data['title']
        deadline = request.data['deadline']
        published_at = request.data['published_at']

    
        if len(description) == 0 or len(assigned_to) == 0 or len(title) == 0:
            return Response({'msg':'Data format is not correct'},status=status.HTTP_400_BAD_REQUEST)
        if deadline < str(date.today()) or deadline < published_at:
            return Response({'msg':'Deadline cannot be lesser than today data'},status=status.HTTP_400_BAD_REQUEST)

        try:
            if published_at > str(date.today()):
                status = 'SCHEDULED'
            else:
                status = 'ONGOING'
            print(status)
            print(userDetails)
            obj = Assignments.objects.get(id=pk,assigned_by=userDetails)

            print("yes")
            obj.description =description
            obj.title = title
            obj.published_at = published_at
            obj.deadline = deadline

            for stu in assigned_to:
                userId = User.objects.get(username=stu)
                userProfile = profile.objects.get(user=userId)
                obj.assigned_to.add(userProfile)
            
            try:
                obj.save()
            except ValidationError:
                return Response({"msg":"Something wrong in format"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        except:
            return Response({'msg':'Something went wong'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"msg":"Assignment Updated !!"})    

    def delete(self,request,pk):
        user = request.user
        userDetails = profile.objects.get(user=user)

        if userDetails.role == 'student':
            return Response({'msg':'you have no right to delete the assigment'},status=status.HTTP_403_FORBIDDEN)

        try:
            obj = Assignments.objects.get(id=pk,assigned_by=userDetails)
            obj.delete()
        except:
            return Response({"msg":"you have not right to delete this assignemt"},status=status.HTTP_401_UNAUTHORIZED)


        return Response({"msg":"Deleted successfully"})


class viewsAssign(APIView):
    authentication_classes = [JWTAuthentication]

    permission_classes = (IsAuthenticated,)

    def get(self,request,pk=None):
        user = request.user
        userDetails = profile.objects.get(user=user)
        #for teacher
        if userDetails.role == 'teacher':
            res = []
            techAsign = profile.objects.get(user= user)
            if pk is not None:
                allAss = Assignments.objects.filter(assigned_by=techAsign,id=pk)
            else:
                allAss = Assignments.objects.filter(assigned_by=techAsign)
            for i in allAss:
                dic = {'id':i.id,
                        'desc':i.description,
                        'title':i.title,
                        'published_at':i.published_at,
                        'deadline':i.deadline,
                        'status':i.status
                }
                res.append(dic)
            return Response({"data":res})
        else:
            if pk is not None :
                asign = Assignments.objects.filter(assigned_to=userDetails,id=pk)
            else:
                asign = Assignments.objects.filter(assigned_to=userDetails)
            res = []
            for i in asign:
                dic = {'id':i.id,
                        'desc':i.description,
                        'title':i.title,
                        'published_at':i.published_at,
                        'deadline':i.deadline,
                        'status':i.status,
                        'submission':"PENDING"
                }
                subDetails = Submission.objects.filter(assignment=i,submitted_by=userDetails)
                if subDetails:
                    dic['submission'] = "DONE"
                
                res.append(dic)
            return Response({"data":res})


class assigmentSubmitted(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)

    def post(self,request,pk):

        user = request.user
        userDetails = profile.objects.get(user=user)
        if userDetails.role == 'student':
            userDetails = profile.objects.get(user=user)
            try:
                assignment = Assignments.objects.get(id=pk,assigned_to=userDetails)
                
            except:
                return Response({"Invalid Assignment id or you are not eligble to submit this assignemt"},status=status.HTTP_401_UNAUTHORIZED)

            comment = request.data['comment']
            time = date.today()
            if str(assignment.deadline) < str(date.today()):
                return Response({"msg":"Assignment closed"})

            already_submit = Submission.objects.filter(submitted_by=userDetails,assignment=assignment)

            if already_submit:
                return Response({"msg":"you have already submitted.. oopss!!"})

            try:
                ass_submit = Submission.objects.create(comment=comment,time=time,submitted_by=userDetails,assignment=assignment,status="SUBMITTED")
                ass_submit.save()
            except:
                return Response({"msg":"ERROR !"})

            return Response({"msg":"SUBMITTED YEAHH!!!"})
        return Response({"msg":"you are not student"},status=status.HTTP_401_UNAUTHORIZED)

      
    def get(self,request):
        user = request.user

        userDetails = profile.objects.get(user=user)

        if userDetails.role == 'student':
            data = []
            try:
                assignment = Assignments.objects.filter(assigned_to=userDetails)
                print("esy")
                submitted = Submission.objects.filter(submitted_by=userDetails,assignment=assignment)
                print("ls")
                print(submitted)
                for i in submitted:
                    dic = {
                        "time":i.time,
                        "comment":i.comment
                    }
                    data.append(dic)
                return Response({"data":data})

            except:
                return Response({"msg":"Something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"msg":"you are not student"},status=status.HTTP_401_UNAUTHORIZED)

            