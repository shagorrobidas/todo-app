from django.urls import path
from . import views


urlpatterns = [
    path(
        '', 
        views.HomepageView.as_view(),
        name='home-page'
    ),
    path(
        'register/',
        views.RegisterView.as_view(),
        name="register"
    ),
    path(
        'login/',
        views.LoginpageView.as_view(),
        name="loginpage"
    ),
    path(
        'logout/',
        views.LogoutpageView.as_view(),
        name="logoutpage"
    ),
    path(
        'delete-tesk/<int:pk>/',
        views.DeleteTaskView.as_view(),
        name="delete"
    ),
    path(
        'update-tesk/<int:pk>/',
        views.UpdateTaskView.as_view(),
        name="update"
    ),
]