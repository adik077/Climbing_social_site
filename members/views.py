from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.urls import reverse
from .forms import UserCreation, ChangeUserForm, ChangePassword
from django.contrib import messages
from .models import UserProfile


def login_user(request):
    if request.method == 'POST':
        user_login = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=user_login,password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('main_dashboard'))
        else:
            messages.error(request,"Yoy have used wrong login data, try again...")
    return render(request,'members/login.html',{})

def logout_user(request):
    logout(request)
    messages.success(request,'You were logged out successfully...')
    return HttpResponseRedirect(reverse('main_dashboard'))

def register(request):
    if request.method == 'POST':
        form = UserCreation(request.POST)
        if form.is_valid():
            username=form.cleaned_data["username"]
            form.save()
            user=User.objects.get(username=username)
            UserProfile.objects.create(user=user)
            messages.success(request,'User account was created successfully, now you can log in...')
            return HttpResponseRedirect(reverse('login_user'))
    else:
        form = UserCreation()
    return render(request,'members/register.html',{'form':form})

@login_required
def main_settings(request):
    if request.method == 'POST':
        form = ChangeUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,'Your settings were saved successfully...')
            return HttpResponseRedirect(reverse('main_settings'))
        else:
            messages.warning(request, 'There were problems with updating your data, please check errors below...')
    else:
        form = ChangeUserForm(instance=request.user)
    return render(request,'members/main_settings.html',{'form':form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePassword(data=request.POST,user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            messages.success(request,'Your password was changed successfully')
            return HttpResponseRedirect(reverse('main_dashboard'))
        else:
            messages.warning(request,'You have entered invalid data, please check errors below and try again...')
    else:
        form = ChangePassword(user=request.user)
    return render(request,'members/change_password.html',{'form':form})
