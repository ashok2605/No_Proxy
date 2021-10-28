from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.http import *
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import send_mail
import random
import math
from datetime import date
from home.models import *
def GENERATEPASSWORD():
            s="0123456789"
            b=""
            for i in range(8):
                b=b+s[int(random.random()*10)]
            print(b)
            return b
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
def takeattendance(request):
        if request.method=="GET":
                a=Professor.objects.get(id=request.user.professor.id)
                q=a.course_set.all()
                li=[]
                for j in q:
                        li.append(j.course_name)
                li=list(set(li))
                b=False
                x=None
                if a.course_set.filter(attendance_taking_status=True).exists():
                        x=a.course_set.filter(attendance_taking_status=True).first().course_name
                        #t=a.course_set.filter(attendance_taking_status=True).first().attendance_set.all()
                        #for j in t:
                        #       j.total_classes_count=j.total_classes_count+1
                        #       j.save()
                        b=True
        
                return render(request,'takeattendance.html',{'li':li,'x':x,'b':b})
        if request.method=="POST":
                print(request.POST['course'])
                q=Course.objects.filter(course_name=request.POST['course'])
                print(q)
                for j in q:
                        j.attendance_taking_status=True
                        j.save()
                k=Course.objects.filter(course_name=request.POST['course']).first().attendance_set.all()
                for m in k:
                        m.total_classes_count=m.total_classes_count+1
                        code=GENERATEPASSWORD()
                        m.code=code
                        m.save()
                            
                        subject = 'Do not reply'
                            
                          
                        message = 'Hi '+m.stud.user.username+"   YOUR CODE FOR TAKING ATTENDACE FOR COURSE" +request.POST['course']+ "IS    "+code
                        recipient_list = [m.stud.user.email]
                        email_from = settings.EMAIL_HOST_USER
                        send_mail(subject,message, email_from, recipient_list )

                
                return HttpResponse("taking attendance")

def stoptakingattendance(request):
        if request.method=="POST":
                a=Professor.objects.get(id=request.user.professor.id) 
                x=a.course_set.filter(attendance_taking_status=True).first()
                li=x.attendance_set.filter(attended_status=False)
                liofstuabs=[]

                for z in li:
                        liofstuabs.append(z.stud)
                dt=date.today()
                y=Absentdates.objects.get(dates_of_absent__day=dt.day,dates_of_absent__month=dt.month,dates_of_absent__year=dt.year)
                print(li,"hello")
                for b in li:
                        if not b.absentdates.filter(dates_of_absent__day=dt.day,dates_of_absent__month=dt.month,dates_of_absent__year=dt.year).exists():
                                b.absentdates.add(y)
                                y.save()
                
                print(liofstuabs,"bye")
                print(li)

                for j in x.attendance_set.all():
                       j.attended_status=False
                       j.save()
                print(li)
                for k in a.course_set.filter(attendance_taking_status=True):
                        k.attendance_taking_status=False
                        k.save()
                
                return render(request,"showlist.html",{'li':liofstuabs})

