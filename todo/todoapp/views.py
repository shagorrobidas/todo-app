from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages

# Create your views here.


def home(request):
    return render(request, 'todoapp/todo.html', {})


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if len(password) < 4:
            messages.error(request, 'Password must be at least 4 characters')
            return redirect('register')
        
        get_all_users_by_username = User.objects.filter(username=username)
        if get_all_users_by_username:
            messages.error(request, 'Error, username already exists, User another.')  # noqa
            return redirect('register')
        
        get_all_users_by_email = User.objects.filter(email=email)
        if get_all_users_by_email:
            messages.error(request, 'Error, Email already exists, User another.')  # noqa
            return redirect('register')

        newUser = User.objects.create_user(
            username=username, email=email, password=password)
        newUser.save()
        
        messages.error(request, 'User successfully created,login now.')
        return redirect('loginpage')
    return render(request, 'todoapp/register.html', {})


def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')

        validate_user = authenticate(username=username, password=password)
        if validate_user is not None:
            login(request, validate_user)
            return redirect('home-page')
        else:
            messages.error(request, 'Error, wrong user details or user does not exist.')  # noqa
            return redirect('loginpage')

    return render(request, 'todoapp/login.html', {})
