from django.shortcuts import render

# Create your views here.
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    
    path('profile',views.profile,name="profile"),
    path('timetable',views.timetable,name="timetable"),
    path('staffqueries',views.staffqueries,name="staffqueries"),
    path('staffmakeaquery',views.staffmakeaquery,name="staffmakeaquery"),
    path('staffmanagequeries',views.staffmanagequeries,name="staffmanagequeries"),
    path('staffmanagequeries/<int:id>',views.responsestudentcourse,name="responsestudentcourse")
    



]
