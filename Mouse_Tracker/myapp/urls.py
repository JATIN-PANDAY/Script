from django.contrib import admin
from django.urls import path
from myapp import views

# for use restframework

# from .views import UserLoginView


urlpatterns = [
     path('', views.index,name='index'),
     path('signup',views.signup,name="signup"),
     path('signin',views.signin,name='signin'),
     # path('api/login/', UserLoginView.as_view(), name='user-login'),
     # path('testsignin',views.testsignin),

]