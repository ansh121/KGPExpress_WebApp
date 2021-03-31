from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

# from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

class SignUpForm(UserCreationForm):
    username = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

# class ProfileForm(forms.ModelForm):
#     username = forms.CharField()
#     first_name = forms.CharField(required=False)
#     last_name = forms.CharField(required=False)
#     roll_no = forms.CharField(required=False)
#     institute_email_id = forms.EmailField(required=False)

#     class Meta:
#         model = CustomUser
#         fields = ('username','first_name', 'last_name', 'roll_no', 'institute_email_id')

#     def update(self, username, commit=True):
#         instance = super(ProfileForm, self).save(commit=False)
#         instance.username = username  
#         if self.cleaned_data['first_name']:
#             instance.first_name = self.cleaned_data['multi_choice']
#         print(instance)
