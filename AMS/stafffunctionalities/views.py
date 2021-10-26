from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.http import *
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
import random
import math

from home.models import *

def profile(request):
    
        a=Professor.objects.get(id=request.user.professor.id)
        return a.VIEWSTAFFPROFILE(request)
def timetable(request):
        a=Professor.objects.get(id=request.user.professor.id)
        return a.VIEWTIMETABLE(request)
def staffqueries(request):
        if request.method=="GET":
                
                return render(request,"staffinitialqueries.html")
        if request.method=="POST":
                a=request.POST['to_who']
                if a=="ADMIN":
                        q=Query.objects.filter(send_status=2)
                        return render(request,"responsestaffadmin.html",{'q':q})
                else:
                        pass
def staffmakeaquery(request):
        a=Professor.objects.get(id=request.user.professor.id)
        return a.STAFFMAKEAQUERY(request)
def staffmanagequeries(request):
        a=Professor.objects.get(id=request.user.professor.id)
        return a.STAFFMANAGEQUERIES(request)
def responsestudentcourse(request,id):
        a=Professor.objects.get(id=request.user.professor.id)
        return a.RESPONSESTUDENTCOURSE(request,id)