from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from reminder.models import Todos
# --------registrion----------

class UserForm(UserCreationForm):
    class Meta:
        model=User
        fields=["username","email","password1","password2"]
        widgets={

            "username":forms.TextInput(attrs={"class":"form-control"}),
            "email":forms.EmailInput(attrs={"class":"form-control"}),
            "password1":forms.PasswordInput(attrs={"class":"form-control"}),
            "password2":forms.PasswordInput(attrs={"class":"form-contorl"})
           
        }


class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))



class TodoForm(forms.ModelForm):
    class Meta:
        model=Todos
        fields=["name"]
        widgets={

            "name":forms.TextInput(attrs={"class":"form-control"})
        }


