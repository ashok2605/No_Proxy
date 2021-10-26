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
    
        a=Student.objects.get(id=request.user.student.id)
        return a.VIEWSTUDENTPROFILE(request)
def timetable(request):
        a=Student.objects.get(id=request.user.student.id)
        return a.VIEWTIMETABLE(request)
def queries(request):
        if request.method=="GET":
                semester=request.user.student.semester
                branch=request.user.student.branch
                q=Course.objects.filter(semester=semester,branch=branch)
                li=[]
                for k in q:
                        li.append(k.course_name)
                li=list(set(li))
                return render(request,"stinitialqueries.html",{'li':li})
        if request.method=="POST":
                a=request.POST['to_who']
                if a=="ADMIN":
                        q=Query.objects.filter(send_status=1)
                        return render(request,"responsestudentadmin.html",{'q':q})
                else:
                        l=Course.objects.filter(course_name=request.POST['to_who']).first().query_set.all()
                        q=[]
                        for j in l:
                                if j.from_stu.user.id==request.user.id:
                                        q.append(j)
                                else:
                                        continue
                          


                        return render(request,"courserespondtostudent.html",{'q':q})


def makeaquery(request):
        a=Student.objects.get(id=request.user.student.id)
        return a.MAKEAQUERY(request) 

