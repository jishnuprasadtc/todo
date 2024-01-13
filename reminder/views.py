from django.shortcuts import render,redirect
from django.views.generic import View
from reminder.forms import UserForm,LoginForm,TodoForm
from django.contrib.auth import authenticate,login,logout
from reminder.models import Todos
from django.utils.decorators import method_decorator
from django.contrib import messages


def signinreq(fn):
    def wrapper(request,*arg,**kwargs):
        if not request.user.is_authenticated:
            
            return redirect("signin")
        else:
            return fn(request,*arg,**kwargs)
    return wrapper


def owner_permission_required(fn):
    def wrappper(request,*args, **kwargs):
        id=kwargs.get("pk")
        todo_object=Todos.objects.get(id=id)
        if todo_object.user != request.user:
            return redirect("signin")
        else:
            return fn(request,*args, **kwargs)
    return wrappper




decs=[signinreq,owner_permission_required]

# Create your views here.

class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=UserForm()
        return render(request,"reg.html",{"form":form})

    def post(self,request,*args,**kwargs):
        form=UserForm(request.POST)
        if form.is_valid():
            form.save()
            print("account created")
            return redirect("signin")
        else:
            print("faild")
            return render(request,"reg.html",{"form":form})

class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"Sign.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            user_name=form.cleaned_data.get("username")
            psw=form.cleaned_data.get("password")
            user_object=authenticate(request,username=user_name,password=psw)
            if user_object:
                login(request,user_object)
                print("Loggedin")
                return redirect("index")
        
        print("invalid credentional")
        return render(request,"Sign.html",{"form":form})
    

@method_decorator(signinreq,name="dispatch")
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")   
     
@method_decorator(signinreq,name="dispatch")       
class IndexView(View):
    def get(self,request,*args,**kwargs):
        form=TodoForm()
        qs=Todos.objects.filter(user=request.user).order_by("status")
        return render(request,"index.html",{"form":form,"data":qs})
    
    def post(self,request,*args,**kwargs):
        form=TodoForm(request.POST)
        if form.is_valid():
            form.instance.user=request.user
            form.save()
            return redirect('index')
        else:
            return render(request,"index.html",{"form":form})
        

@method_decorator(decs,name="dispatch")
class TodoDelete(View):
    def get (self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Todos.objects.filter(id=id).delete()
        return redirect("index")
    
@method_decorator(decs,name="dispatch")
class Todoupdate(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        todo_object=Todos.objects.get(id=id)
        if todo_object.status==True:
            todo_object.status=False
            todo_object.save()
        else:
            todo_object.status=True
            todo_object.save()
        return redirect("index")
    



            



    
   