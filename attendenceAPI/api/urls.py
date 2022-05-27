from django.urls import path
from .views import *

urlpatterns = [
    path('cors-test', CorsTest.as_view()),
    path('', Home.as_view()),
    path('signup', SignUp.as_view()),
    path('login', Login.as_view()),
    path('logout', LogOut.as_view()),
    path('myattendance', MyAttendance.as_view()),
    path('export', ExportData.as_view()),
    path('profile',UserProfile.as_view()),
    path('editprofile',EditProfile.as_view()),
    path('data', AttendaceData.as_view()),
]