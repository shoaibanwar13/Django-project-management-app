
from django.urls import path
from . import views

urlpatterns = [
    path('', views.show,name="show"),
    path('about/', views.about,name="blogs-about"),
    path('signup/', views.signup,name="signup-page"),
    path('login/', views.login,name="login-page"),
    path('forms/', views.forms,name="form-page"),
    
]
