from django import forms
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User

class signupform(UserCreationForm):
    first_name=forms.CharField(max_length=50)
    last_name=forms.CharField(max_length=50)
    email=forms.CharField(max_length=50)

    class meta:
        model=User
        fields=('username','password1','password2','email','first_name','last_name')
        widgets = {
            'username': forms.TextInput(
    attrs={
     'class': 'form-control'
     }
    ),
   'password1': forms.TextInput(
    attrs={
     'class': 'form-control'
     }
    ),
   'password2': forms.TextInput(
    attrs={
     'class': 'form-control'
     }
    ),
    'email': forms.Textarea(
    attrs={
     'class': 'form-control'
     }
    ),
   'first_name': forms.Textarea(
    attrs={
     'class': 'form-control'
     }
    ),
    'last_name': forms.Textarea(
    attrs={
     'class': 'form-control'
     }
    ),

   }
    
    def save(self,commit=True):
        user=super(signupform,self).save(commit=False)
        user.email=self.cleaned_data['email']
        user.first_name=self.cleaned_data['first_name']
        user.last_name=self.cleaned_data['last_name']


        if commit:
            user.save()
        return user
