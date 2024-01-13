from django.shortcuts import render
from api.serializers import UserSerializer,TodoSerializer
from reminder.models import Todos
# Create your views here.

from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import serializers
from rest_framework.authtoken.views import ObtainAuthToken


class SignUpView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        

class TodosView(ViewSet):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]


    def list(self,request,*args,**kwargs):
        qs=Todos.objects.filter(user=request.user)
        serializer=TodoSerializer(qs,many=True)
        return Response(data=serializer.data)
        

    def create(self,request,*args,**kwargs):
        serializer=TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Todos.objects.get(id=id)
        serializers=TodoSerializer(qs)
        return Response(data=serializers.data)
    

    def update(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        todo_object=Todos.objects.get(id=id)
        serializer=TodoSerializer(data=request.data,instance=todo_object)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.data)



    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk") 
        qs=Todos.objects.get(id=id)
        if qs.user==request.user:
            qs.delete()
        else:
            raise serializers.ValidationError("permission denied")
        return Response(data={"message":"delete"})
    
   

