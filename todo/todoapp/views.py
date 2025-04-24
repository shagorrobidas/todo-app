from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages
from .models import Todo

from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class HomepageView(LoginRequiredMixin, View):
    def get(self, request):
        all_todos = Todo.objects.filter(user=request.user)
        context = {
            'todos': all_todos
        }
        return render(request, 'todoapp/todo.html', context)

    def post(self, request):
        task = request.POST.get('task')
        description = request.POST.get('description')

        if task and description:
            Todo.objects.create(
                user=request.user,
                name=task,
                description=description
            )
        return redirect('home-page')


class RegisterView(View):
    template_name = 'todoapp/register.html'

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if len(password) < 4:
            messages.error(request, 'Password must be at least 4 characters')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Error, username already exists. Use another.')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Error, Email already exists. Use another.')
            return redirect('register')

        User.objects.create_user(
            username=username, email=email, password=password
        )
        messages.success(request, 'User successfully created. Login now.')
        return redirect('loginpage')

def LoginpageView(request):
    # if request.user.is_authenticeted:
    #     return redirect('home-page')

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


def LogoutpageView(request):
    logout(request)
    return redirect('loginpage')


@login_required
def DeleteTaskView(request, pk):
    get_todo = Todo.objects.get(user=request.user, pk=pk)
    get_todo.delete()
    return redirect('home-page')


@login_required
def UpdateTaksView(request, pk):
    get_todo = Todo.objects.get(user=request.user, pk=pk)
    get_todo.status = True
    get_todo.save()
    return redirect('home-page')
