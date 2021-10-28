from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.http import *
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
import random
import math
from .recognizer import Recognizer
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
def markattendance(request):
        if request.method=="GET":
                a=Student.objects.get(id=request.user.student.id)
                semester=a.semester
                branch=a.branch
                
                if Course.objects.filter(semester=semester,branch=branch,attendance_taking_status=True).exists():
                        name=Course.objects.filter(semester=semester,branch=branch,attendance_taking_status=True).first().course_name
                        return render(request,'markattendance.html',{'name':name})
                else:
                        messages.info(request,"no subject is ongoing or ur attendance is noted")
                        return redirect("/studentlogin/student")


        if request.method=="POST":
                a=Student.objects.get(id=request.user.student.id)
                ob=None
                obj=a.attendance_set.all()
                for j in obj:
                        if j.cour.filter(attendance_taking_status=True).exists():
                                ob=j
                                break
                details = {
            'branch':request.user.student.branch,
            'semester': request.user.student.semester
            
            }
                names = Recognizer(details)
                students=Student.objects.filter(semester=request.user.student.semester,branch=request.user.student.branch)
                flag=0
                for student in students:
                        if student.user.username==names:
                                flag=1
                                break

                if flag==1:
                        ob.attended_status=True
                        ob.code=''
                        ob.attended_classes_count=ob.attended_classes_count+1
                        ob.save()
                        messages.info(request,"attendance noted")
                        return redirect("/studentlogin/student")
                #if ob.code==request.POST['code']:
                        #ob.attended_status=True
                        #ob.code=''
                        #ob.attended_classes_count=ob.attended_classes_count+1
                        #ob.save()
                        #messages.info(request,"attendance noted")
                        #return redirect("/studentlogin/student")
                else:
                        messages.info(request,"try again profile not found is wrong")
                        return redirect("/studentlogin/student/markattendance")
               
