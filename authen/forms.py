from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser

class Emailform(forms.Form):
    email = forms.EmailField(label='Enter your email')



class SignUpForm(UserCreationForm):
    full_name = forms.CharField(max_length=100, help_text='Required. 100 charaters of fewer.')

    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('full_name', 'age','email',)
       
       

