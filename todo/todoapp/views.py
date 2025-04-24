from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages
from .models import Todo

from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404

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


class RegisterView(View, LoginRequiredMixin):
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

class LoginpageView(View, LoginRequiredMixin):
    template_name = 'todoapp/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('uname')
        password = request.POST.get('pass')

        user = authenticate(
            username=username,
            password=password
        )
        if user is not None:
            login(request, user)
            return redirect('home-page')
        else:
            messages.error(request, 'Error, wrong user details or user does not exist.')
            return redirect('loginpage')


class LogoutpageView(View, LoginRequiredMixin):
    def get(self, request):
        logout(request)
        return redirect('loginpage')


class DeleteTaskView(LoginRequiredMixin, View):
    def get(self, request, pk):
        todo = get_object_or_404(Todo, pk=pk, user=request.user)
        todo.delete()
        return redirect('home-page')


class UpdateTaskView(LoginRequiredMixin, View):
    def get(self, request, pk):
        todo = get_object_or_404(Todo, pk=pk, user=request.user)
        todo.status = True
        todo.save()
        return redirect('home-page')
