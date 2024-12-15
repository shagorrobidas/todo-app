from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomepageView, name="home-page"),
    path('register/', views.RegisterView, name="register"),
    path('login/', views.LoginpageView, name="loginpage"),
    path('logout/', views.LogoutpageView, name="logoutpage"),
    path('delete-tesk/<int:pk>/', views.DeleteTaskView, name="delete"),
    path('update-tesk/<int:pk>/', views.UpdateTaksView, name="update"),
]