from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.http import *
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
import random
import math
import os

import face_recognition
from home.models import *
import base64
def find(details,request):
        image_data=request.POST.get("content").split(",")[1]
        print("hjsbdvhjsjdbvjsdbvjb")
        name=request.user.username
        with open(name+'.png','wb') as f:
                f.write(base64.b64decode(image_data))
        print(os.path.isfile(name+".png"))
        unknown_image=face_recognition.load_image_file(name+'.png')
        unknown_face_encoding = face_recognition.face_encodings(unknown_image)
        if len(unknown_face_encoding) > 0:
                    unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]

        else:
                   print("No faces found in the image!")
                   os.remove(name+".png")
                   return "USERNOTFOUND"
        
        known_face_encodings = []
        

        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # os.chdir("..")
        base_dir = os.getcwd()
        image_dir = os.path.join(base_dir,"{}\{}\{}\{}".format('media','Student_Images',details['semester'],details['branch']))
        print(image_dir)
       
        # print(image_dir)
        
        known_face_names = []
        
        

        for root,dirs,files in os.walk(image_dir):
                for file in files:
                        if file.endswith('jpg') or file.endswith('png') or file.endswith('jpeg') :
                                path = os.path.join(root, file)
                                img = face_recognition.load_image_file(path)
                                label = file[:len(file)-4]
                                img_encoding = face_recognition.face_encodings(img)[0]
                                known_face_names.append(label)
                                known_face_encodings.append(img_encoding)
        for j in known_face_encodings:
                result = face_recognition.compare_faces([j], unknown_face_encoding)
                if result[0]==True:
                        os.remove(name+".png")
                        return "USERFOUND"
        os.remove(name+".png")
        return "USERNOTFOUND"
        
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
                ob=None
                obj=a.attendance_set.all()
                for j in obj:
                        if j.cour.filter(attendance_taking_status=True).exists():
                                ob=j
                                break
                if Course.objects.filter(semester=semester,branch=branch,attendance_taking_status=True).exists() and ob.attended_status==False:
                        name=Course.objects.filter(semester=semester,branch=branch,attendance_taking_status=True).first().course_name
                        return render(request,'markattendance.html',{'name':name})
                else:
                        messages.info(request,"no subject is ongoing or ur attendance is noted")
                        return redirect("/studentlogin/student")


        if request.method=="POST":
                if Course.objects.filter(semester=request.user.student.semester,branch=request.user.student.branch,attendance_taking_status=True).exists():
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
                #names = Recognizer(details)
                #students=Student.objects.filter(semester=request.user.student.semester,branch=request.user.student.branch)
                #flag=0
                #for student in students:
                        #if student.user.username==names:
#                               # break
                        s=find(details,request)
                        print(s)
                        if s=="USERFOUND":
                                ob.attended_status=True
                                ob.code=''
                                ob.attended_classes_count=ob.attended_classes_count+1
                                ob.save()
                                return JsonResponse({'success':'FOUND'})
                        else:
                                return JsonResponse({'success':'NOTFOUND'})
                else:
                        messages.info(request,"sorry time is over,attendance not noted")
                        return JsonResponse({'success':'timeover'})
                
                
                
                

                #if ob.code==request.POST['code']:
                       # ob.attended_status=True
                       # ob.code=''
                       # ob.attended_classes_count=ob.attended_classes_count+1
                       # ob.save()
                       # messages.info(request,"attendance noted")
                       # return redirect("/studentlogin/student")
                #if flag==1 :
                        #ob.attended_status=True
                        #ob.code=''
                        #ob.attended_classes_count=ob.attended_classes_count+1
                        #ob.save()
                        #messages.info(request,"attendance noted")
                        #return redirect("/studentlogin/student")
                #else:
                       # messages.info(request,"try again profile not found is wrong")
                        #return redirect("/studentlogin/student/markattendance")
               
def attended(request):
        messages.info(request,"Ur attendance is noted")
        return redirect("/studentlogin/student")
def stats(request):
        s=request.user.student
        li=s.courses.all()
        listofcourses=[]
        for j in li:
                listofcourses.append(j.course_name)
        l=list(set(listofcourses))
        d=dict()
        for j in l:
                prof=Course.objects.filter(course_name=j).first().professor
                d[j]=prof
        return render(request,"studentstats.html",{'l':l,'d':d})
def specificstats(request,coursename):
        a=Student.objects.get(id=request.user.student.id)
        return a.VIEWSTATS(request,coursename)
