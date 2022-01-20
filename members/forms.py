from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import UserProfile
from croppie.fields import CroppieField
from taggit.forms import TagWidget

class UserCreation(UserCreationForm):
    username = forms.CharField(label="Username",widget=forms.TextInput(attrs={'class':'form-control form-control-lg','placeholder':'Enter your username'}))
    email = forms.CharField(label="Email",widget=forms.EmailInput(attrs={'class':'form-control form-control-lg','placeholder':'Enter your email'}))
    password1 = forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'class':'form-control form-control-lg','placeholder':'Enter your password'}))
    password2 = forms.CharField(label="Password confirmation",widget=forms.PasswordInput(attrs={'class':'form-control form-control-lg','placeholder':'Confirm your password'}))
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class UserProfileForm(forms.ModelForm):
    twitter_url = forms.CharField(required=False,widget=forms.URLInput(attrs={'class':'form-control form-control-lg'}))
    facebook_url = forms.CharField(required=False,widget=forms.URLInput(attrs={'class':'form-control form-control-lg'}))
    instagram_url = forms.CharField(required=False,widget=forms.URLInput(attrs={'class':'form-control form-control-lg'}))
    where_from = forms.CharField(required=False,label='From:',widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}))
    where_lives = forms.CharField(required=False,label='Lives in:',widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}))
    photo = CroppieField(required=False, options={
            'viewport': {
                'width': 150,
                'height': 150,
                'type': 'circle'
            },
            'boundary': {
                'width': '90%',
                'height': 200,
            },
            'showZoomer': True,
        },)
    class Meta:
        model = UserProfile
        fields = ['twitter_url','facebook_url','instagram_url','where_from','where_lives','best_places','photo']
        widgets={
            'best_places':TagWidget(attrs={'class':'form-control form-control-lg'})
        }

class ChangeUserForm(UserChangeForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}))
    first_name = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}))
    last_name = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}))
    email = forms.CharField(required=False,widget=forms.EmailInput(attrs={'class':'form-control form-control-lg'}))
    password=None
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']

class ChangePassword(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-lg'}))
    new_password1 = forms.CharField(label='New password',widget=forms.PasswordInput(attrs={'class':'form-control form-control-lg'}))
    new_password2 = forms.CharField(label='Confirm password',widget=forms.PasswordInput(attrs={'class':'form-control form-control-lg'}))
    class Meta:
        model = User
        fields = ['old_password','new_password1','new_password2']