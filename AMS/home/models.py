from django.db import models
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.db.models.deletion import SET_NULL
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
import random
from django.http.response import HttpResponse

from django.shortcuts import render,redirect
# Create your models here.
# Create your models here.
class Query(models.Model):
    question=models.TextField(null=True,blank=True)
    answer=models.TextField(blank=True,null=True)
    answered_status=models.BooleanField(default=False)
    send_status=models.IntegerField(blank=False,null=False)
    from_stu=models.ForeignKey("Student",on_delete=models.CASCADE,null=True)
    to_adm=models.ForeignKey("ADMIN",on_delete=models.CASCADE,null=True)
    to_course=models.ManyToManyField("Course")
    from_prof=models.ForeignKey("Professor",on_delete=models.CASCADE,null=True)
    #0-from student to course
    #1-from student to admin
    #2-from prof to admin
class notices(models.Model):
    Notice=models.TextField(null=True,blank=True)
from .forms import *
class Professor(models.Model):
    profprofilepic=models.FileField(upload_to="pictures/",null=True,blank=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    
    def VIEWSTAFFPROFILE(self,request):
        if request.method=="GET":

            s=Professor.objects.get(id=request.user.professor.id)
            q=s.course_set.all()
            li=[]
            for k in q:
                li.append(k.course_name)
            li=list(set(li))
            return render(request,"staffprofile.html",{'s':s,'li':li})
        if request.method=="POST":
            first_name=request.POST['firstname']
            last_name=request.POST['lastname']
            if len(request.FILES)>0:
                profprofilepic=request.FILES['profprofilepic']
                s=Professor.objects.get(id=request.user.professor.id)
                s.user.first_name=first_name
                s.user.last_name=last_name
                s.user.save()
                s.profprofilepic=profprofilepic
                s.save()
                messages.info(request,"updatedsuccessfully")
                return redirect("/stafflogin/staff/profile")
            else:
                s=Professor.objects.get(id=request.user.professor.id)
                s.user.first_name=first_name
                s.user.last_name=last_name
                s.user.save()
               
                s.save()
                messages.info(request,"updatedsuccessfully")
                return redirect("/stafflogin/staff/profile")
            return redirect("/studentlogin/student/profile")
    
    def VIEWTIMETABLE(self,request):
        if request.method=="GET":
            obj=Professor.objects.get(id=request.user.professor.id)
            q=obj.course_set.all()
            monday=dict()
            tuesday=dict()
            wednesday=dict()
            thursday=dict()
            friday=dict()
           
            t=[monday,tuesday,wednesday,thursday,friday]
            for k in q:
                if k.day=="MONDAY":
                    li=[[k.course_name,k.branch,k.semester]]
                    if k.time not in monday:
                        
                        monday[k.time]=li
                    else:
                        monday[k.time]=monday[k.time]+li
                if k.day=="TUESDAY":
                    li=[[k.course_name,k.branch,k.semester]]
                    if k.time not in tuesday:
                        
                        tuesday[k.time]=li
                    else:
                        tuesday[k.time]=tuesday[k.time]+li
                if k.day=="WEDNESDAY":
                    li=[[k.course_name,k.branch,k.semester]]
                    if k.time not in wednesday:
                        
                        wednesday[k.time]=li
                    else:
                        wednesday[k.time]=wednesday[k.time]+li
                if k.day=="THURSDAY":
                    li=[[k.course_name,k.branch,k.semester]]
                    if k.time not in thursday:
                        
                        thursday[k.time]=li
                    else:
                        thursday[k.time]=thursday[k.time]+li
                if k.day=="FRIDAY":
                    li=[[k.course_name,k.branch,k.semester]]
                    if k.time not in friday:
                        
                        friday[k.time]=li
                    else:
                        friday[k.time]=friday[k.time]+li
            di={'h':10}
            for i in t:
                if "10:00-11:00" not in i:
                    i["a"]=[]
                else:
                    p=i["10:00-11:00"]
                    del i["10:00-11:00"]
                    i["a"]=p
                if "11:00-12:00" not in i:
                    i["b"]=[]
                else:
                    p=i["11:00-12:00"]
                    del i["11:00-12:00"]
                    i["b"]=p
                if "14:00-15:00" not in i:
                    i["c"]=[]
                else:
                    p=i["14:00-15:00"]
                    del i["14:00-15:00"]
                    i["c"]=p
                if "15:00-16:00" not in i:
                    i["d"]=[]
                else:
                    p=i["15:00-16:00"]
                    del i["15:00-16:00"]
                    i["d"]=p
            
            print(monday)
            return render(request,"viewstafftimetable.html",{'obj':obj,'monday':monday,'tuesday':tuesday,'wednesday':wednesday,'thursday':thursday,'friday':friday})
    def STAFFMAKEAQUERY(self,request):
        if request.method=="GET":
            
            form=QueryFormRequest()
            return render(request,"staffmakeaquery.html",{'form':form})
        if request.method=="POST":
            if request.POST['question']=="":
                messages.info(request,"please fill something before submitting")
                return redirect("/stafflogin/staff/staffmakeaquery")
            else:
                to_who=request.POST['to_who']
                if to_who=="ADMIN":
                    question=request.POST['question']
                    send_status=2
                    from_prof=Professor.objects.get(id=request.user.professor.id)
                    to_adm=ADMIN.objects.all().first()
                    query=Query(question=question,send_status=send_status,from_prof=from_prof,to_adm=to_adm)
                    query.save()
                    messages.info(request,"query submitted successfully")
                    return redirect("/stafflogin/staff/staffqueries")
    def STAFFMANAGEQUERIES(self,request):
        if request.method=="GET":
            a=Professor.objects.get(id=request.user.professor.id)
            q=a.course_set.all()
            li=[]
            for i in q:
                li.append(i.course_name)
            li=list(set(li))
            d=dict()
            for j in li:
                l=list(Course.objects.filter(course_name=j).first().query_set.filter(answered_status=False))
                d[j]=l
            return render(request,"staffmanagequeries.html",{'d':d})
    def RESPONSESTUDENTCOURSE(self,request,id):
        if request.method=="GET":
            ki=Query.objects.get(id=id,answered_status=False)
            print(ki)
            question=ki.question
            f=QueryFormResponse()
            return render(request,"responsestudentcourse.html",{'ki':ki,'form':f})
        if request.method=="POST":
                if request.POST['answer']=="":
                    messages.info(request,"please respond")
                    return redirect("/stafflogin/staff/staffmanagequeries/"+str(id))
                else:
                    q=Query.objects.get(id=id)
                    q.answered_status=True
                    q.answer=request.POST['answer']
                    q.save()
                    messages.info(request,"response submitted")
                    return redirect("/stafflogin/staff/staffmanagequeries")
        

                
         
class Course(models.Model):
    COURSE_NAME=[
        ('CSN221','CSN221'),
        ('CSN291','CSN291'),
        ('PHN005','PHN005'),
        ('MAN005','MAN005'),
        ('CEN105','CEN105')
    ]
    COURSE_BRANCH=[
        ('CSE','CSE'),
        ('ECE','ECE'),
        ('EE','EE'),
        ('ME','ME')
    ]
    COURSE_SEMESTER=[
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8')
    ]
    COURSE_TEACHING_DAY=[
        ('MONDAY','MONDAY'),
        ('TUESDAY','TUESDAY'),
        ('WEDNESDAY','WEDNESDAY'),
        ('THURSDAY','THURSDAY'),
        ('FRIDAY','FRIDAY')
    ]
    COURSE_TEACHING_TIME=[
        ('10:00-11:00','10:00-11:00'),
        ('11:00-12:00','11:00-12:00'),
        ('14:00-15:00','14:00-15:00'),
        ('15:00-16:00','15:00-16:00'),

    ]

    professor=models.ForeignKey(Professor,on_delete=SET_NULL,null=True)
    course_syllabus=models.TextField(blank=False)
    course_name = models.CharField(
        max_length=10,
        choices=COURSE_NAME,
        default='1'
    )
    branch=models.CharField(
        max_length=10,
        choices=COURSE_BRANCH,
        default='CSE'
    )
    semester = models.CharField(
        max_length=10,
        choices=COURSE_SEMESTER,
        default='1'
    )
    day=models.CharField(
        max_length=20,
        choices=COURSE_TEACHING_DAY ,
        default='MONDAY'
    )
    time=models.CharField(
        max_length=20,
        choices=COURSE_TEACHING_TIME ,
        default='10:00-11:00'
    )



class Student(models.Model):
    SEMESTER_CHOICES = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8')
          

    ]
    BRANCH_CHOICES=[
        ('CSE','CSE'),
        ('ECE','ECE'),
        ('EE','EE'),
        ('ME','ME')
    ]
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    semester = models.CharField(
        max_length=2,
        choices=SEMESTER_CHOICES,
        default='1'
    )
    branch=models.CharField(
        max_length=5,
        choices=BRANCH_CHOICES,
        default='CSE'
    )
    courses=models.ManyToManyField(Course)
    studprofilepic=models.FileField(upload_to="pictures/",null=True,blank=True)

    def VIEWSTUDENTPROFILE(self,request):
        if request.method=="GET":
            s=Student.objects.get(id=request.user.student.id)
            return render(request,"studentprofile.html",{'s':s})
        if request.method=="POST":
            first_name=request.POST['firstname']
            last_name=request.POST['lastname']
            if len(request.FILES)>0:
                studprofilepic=request.FILES['studprofilepic']
                s=Student.objects.get(id=request.user.student.id)
                s.user.first_name=first_name
                s.user.last_name=last_name
                s.user.save()
                s.studprofilepic=studprofilepic
                s.save()
                messages.info(request,"updatedsuccessfully")
                return redirect("/studentlogin/student/profile")
            else:
                s=Student.objects.get(id=request.user.student.id)
                s.user.first_name=first_name
                s.user.last_name=last_name
                s.user.save()
               
                s.save()
                messages.info(request,"updatedsuccessfully")
                return redirect("/studentlogin/student/profile")
            return redirect("/studentlogin/student/profile")
    def VIEWTIMETABLE(self,request):
        if request.method=="GET":
            branch=request.user.student.branch
            semester=request.user.student.semester
            a=Course.objects.filter(branch=branch,semester=semester)
            monday=dict()
            tuesday=dict()
            wednesday=dict()
            thursday=dict()
            friday=dict()
            br=branch
            sem=semester
            li=[monday,tuesday,wednesday,thursday,friday]
            for k in a:
                if k.day=="MONDAY":
                    monday[k.time]=k.course_name
                if k.day=="TUESDAY":
                    tuesday[k.time]=k.course_name
                if k.day=="WEDNESDAY":
                    wednesday[k.time]=k.course_name
                if k.day=="THURSDAY":
                    thursday[k.time]=k.course_name
                if k.day=="FRIDAY":
                    friday[k.time]=k.course_name
            di={'h':10}
            for i in li:
                if "10:00-11:00" not in i:
                    i["a"]="-"
                else:
                    p=i["10:00-11:00"]
                    del i["10:00-11:00"]
                    i["a"]=p
                if "11:00-12:00" not in i:
                    i["b"]="-"
                else:
                    p=i["11:00-12:00"]
                    del i["11:00-12:00"]
                    i["b"]=p
                if "14:00-15:00" not in i:
                    i["c"]="-"
                else:
                    p=i["14:00-15:00"]
                    del i["14:00-15:00"]
                    i["c"]=p
                if "15:00-16:00" not in i:
                    i["d"]="-"
                else:
                    p=i["15:00-16:00"]
                    del i["15:00-16:00"]
                    i["d"]=p
            
            print(monday)
            #return render(request,"spotstimetable.html",{'branch':br,'semester':sem,'monday':monday,'tuesday':tuesday,'wednesday':wednesday,'thursday':thursday,'friday':friday,'di':di})
            return render(request,"viewstudenttimetable.html",{'branch':br,'semester':sem,'monday':monday,'tuesday':tuesday,'wednesday':wednesday,'thursday':thursday,'friday':friday,'di':di})
    def MAKEAQUERY(self,request):
        if request.method=="GET":
            semester=request.user.student.semester
            branch=request.user.student.branch
            q=Course.objects.filter(semester=semester,branch=branch)
            li=[]
            for k in q:
                li.append(k.course_name)
            li=list(set(li))
            form=QueryFormRequest()
            return render(request,"makeaquery.html",{'li':li,'form':form})
        if request.method=="POST":
            if request.POST['question']=="":
                messages.info(request,"please fill something before submitting")
                return redirect("/studentlogin/student/makeaquery")
            else:
                to_who=request.POST['to_who']
                if to_who=="ADMIN":
                    question=request.POST['question']
                    send_status=1
                    from_stu=Student.objects.get(id=request.user.student.id)
                    to_adm=ADMIN.objects.all().first()
                    query=Query(question=question,send_status=send_status,from_stu=from_stu,to_adm=to_adm)
                    query.save()
                    messages.info(request,"query submitted successfully")
                    return redirect("/studentlogin/student/queries")

                else:
                    question=request.POST['question']
                    send_status=0
                    from_stu=Student.objects.get(id=request.user.student.id)
                    query=Query(question=question,send_status=send_status,from_stu=from_stu)
                    query.save()
                    c=Course.objects.filter(course_name=to_who)
                    for k in c:
                        query.to_course.add(k)
                        query.save()
                    messages.info(request,"query submitted successfully")
                    return redirect("/studentlogin/student/queries")
    


from adminfunctionalities.forms import *
class ADMIN(models.Model):
        admin_user=models.OneToOneField(User,null=True,on_delete=models.CASCADE)
        def ADDNOTICE(self,request):
            if request.method=="GET":
                
             
                form=NoticeForm()
                return render(request,'addnotice.html',{'form':form})
            if request.method=="POST":
                if request.POST['Notice']=="":
                    messages.info(request,"please add notice before submitting")
                    return redirect("/adminlogin/admin/addnotice")
                else:

                    f=NoticeForm(request.POST)
                
                    f.save()
                
                
                    return redirect("/adminlogin/admin/addnotice")
        def DELETENOTICE(self,request):
            if request.method=="GET":
                obj=notices.objects.all()
                return render(request,'deletenotice.html',{'obj':obj})
            if request.method=="POST":
                querylist=request.POST.getlist('noticedelete')

                for i in querylist:
                    notices.objects.get(id=int(i)).delete()
                return redirect("/adminlogin/admin/deletenotice")
       
        def GENERATEPASSWORD(self):
            s="0123456789"
            b=""
            for i in range(8):
                b=b+s[int(random.random()*10)]
            print(b)
            return b
        def ADDSTUDENT(self,request):
            if request.method=="GET":
                
                f=StudentForm()
                return render(request,'addstudent.html',{'form':f})
            if request.method=="POST":
                first_name=request.POST["firstname"]
                last_name=request.POST["lastname"]
                username=request.POST["id"]
                #password1=request.POST["password1"]
                #password2=request.POST["password2"]
                email=request.POST["email"]
                semester=request.POST["semester"]
                branch=request.POST["branch"]
                studprofilepic=request.FILES['studprofilepic']
                user=None
                #if password1==password2:
                if 1>0:
                    if not User.objects.filter(username=username).exists():
                        if not User.objects.filter(email=email).exists():
                            
                            password1=self.GENERATEPASSWORD()
                            
                            subject = 'Do not reply'
                            
                          
                            message = 'Hi '+username+"   YOUR PASSWORD IS    "+password1
                            recipient_list = [email]
                            email_from = settings.EMAIL_HOST_USER
                            send_mail(subject,message, email_from, recipient_list )
           
                            
                            user=User.objects.create_user(username=username,email=email,password=password1,first_name=first_name,last_name=last_name)
                            user.save()
                            s=Student(user=user,semester=semester,branch=branch,studprofilepic=studprofilepic)
                            s.save()
                            if Course.objects.filter(semester=semester,branch=branch).exists():
                                for i in Course.objects.filter(semester=semester,branch=branch):
                                    s.courses.add(i)
                                    s.save()
                        else:
                            messages.info(request,"email taken,please register again")
                            return redirect('/adminlogin/admin/addstudent')

                    else:
                        messages.info(request,"username Taken,please register again")
                        return redirect("/adminlogin/admin/addstudent")

        
                else:
                    #messages.info(request,"Passwords Not matching,Please Register again")
                    #return redirect("/adminlogin/admin/addstudent")
                    pass
                messages.info(request,"Student added Successfully")
                return redirect("/adminlogin/admin/addstudent")
        def ADDCOURSE(self,request):
            if request.method=='GET':
                
                f=CourseForm()
                return render(request,'addcourse.html',{'form':f})
            if request.method=="POST":
                if request.POST["course_syllabus"]=='':
                    messages.info(request,"please add course syllabus before submitting")
                    return redirect("/adminlogin/admin/addcourse")
                else:

                #course_name=request.POST['course_name']

                #branch=request.POST['branch']
                #semester=request.POST['semester']
                #day=request.POST['day']
                #time=request.POST['time']
                #course_syllabus=request.POST['course_syllabus']
                #if Course.objects.filter(course_name=course_name).exists() and (Course.objects.filter(course_name=course_name).first().semester !=semester or Course.objects.filter(course_name=course_name).first().branch !=branch):
                #    messages.info(request,"course,semester,branch are not matching")
                #    return redirect("/adminlogin/admin/addcourse")
                #else:
                #    if Course.objects.filter(course_name=course_name,branch=branch,semester=semester,day=day,time=time).exists():
                #        messages.info(request,"Course already registered")
                    
                #        return redirect("/adminlogin/admin/addcourse")
                
                
                
                #    else:
                #        if Course.objects.filter(branch=branch,semester=semester,day=day,time=time).exists():
                #           messages.info(request,"spot already taken by another course")
                #           return redirect("/adminlogin/admin/addcourse")

                #        else:
                #            c=Course(course_name=course_name,branch=branch,semester=semester,day=day,time=time,course_syllabus=course_syllabus)
                #            c.save()
                #            if Student.objects.filter(semester=semester,branch=branch).exists():
                #               o=Student.objects.filter(semester=semester,branch=branch)
                #                for ob in o:
                #                    ob.courses.add(c)
                #                    ob.save()
                                
                #                print(Course.objects.get(course_name=course_name).student_set.all())
                #                messages.info(request,"course is scheduled successfully")
                #                return redirect("/adminlogin/admin/addcourse")
                #            else:
                #                return redirect("/adminlogin/admin/addcourse")
                
                    course_name=request.POST['course_name']
                    branch=request.POST['branch']
                    semester=request.POST['semester']
                    if Course.objects.filter(course_name=course_name).exists():
                        messages.info(request,"course already scheduled")
                        return redirect("/adminlogin/admin/addcourse")
                    else:
                        monlen=len(request.POST.getlist("MONDAY"))
                        tueslen=len(request.POST.getlist("TUESDAY"))
                        wedlen=len(request.POST.getlist("WEDNESDAY"))
                        thulen=len(request.POST.getlist("THURSDAY"))
                        frilen=len(request.POST.getlist("FRIDAY"))
                        li=["MONDAY","TUESDAY","WEDNESDAY","THURSDAY","FRIDAY"]
                        spots=dict()
                        f=0
                        flag=""
                        if monlen+tueslen+wedlen+thulen+frilen>0:
                            for i in li:
                                if len(request.POST.getlist(i))>0:
                                    for j in request.POST.getlist(i):
                                        if Course.objects.filter(semester=semester,branch=branch,day=i,time=j).exists():
                                            if i in spots:
                                                spots[i]=spots[i]+","+j
                                            else:
                                                spots[i]=j
                                            f=1
                                            continue
                                    

                                else:
                                    continue
                            if f==1:
                                for key in spots:
                                    flag=flag+key+"-"+spots[key]+","
                        
                                messages.info(request,"These spots are already taken:-"+flag+"all other spots are ok, please schedule again")
                                return redirect("/adminlogin/admin/addcourse")
                            else:
                                for i in li:
                                    if len(request.POST.getlist(i))>0:
                                        for j in request.POST.getlist(i):
                                                c=Course(course_name=course_name,branch=branch,semester=semester,day=i,time=j,course_syllabus=request.POST["course_syllabus"])
                                                c.save()
                                                if Student.objects.filter(semester=semester,branch=branch).exists():
                                                    o=Student.objects.filter(semester=semester,branch=branch)
                                                    for ob in o:
                                                        ob.courses.add(c)
                                                    
                                                        ob.save()
                                messages.info(request,"course scheduled successfully")
                                return redirect("/adminlogin/admin/addcourse")
                        else:
                            messages.info(request,"select atleast one spot")
                            return redirect("/adminlogin/admin/addcourse")
                

        def ADDPROFESSOR(self,request):
            if request.method=='GET':
               
                return render(request,'addprofessor.html')
            if request.method=="POST":
                first_name=request.POST["firstname"]
                last_name=request.POST["lastname"]
                username=request.POST["professorid"]
                #password1=request.POST["password1"]
                #password2=request.POST["password2"]
                email=request.POST["email"]
                profprofilepic=request.FILES['profprofilepic']
                user=None
                k=""
                #if password1==password2:
                if len(request.POST.getlist('allcourses'))>0:
                    if not User.objects.filter(username=username).exists():
                        if not User.objects.filter(email=email).exists():
                            
                            password1=self.GENERATEPASSWORD()
                            
                            subject = 'Donot reply'
                            
                          
                            message = 'Hi'+username+"YOUR PASSWORD IS "+password1
                            recipient_list = [email]
                            email_from = settings.EMAIL_HOST_USER
                            send_mail(subject,message, email_from, recipient_list )
           
                            
                            user=User.objects.create_user(username=username,email=email,password=password1,first_name=first_name,last_name=last_name,is_staff=True,is_superuser=False)
                            user.save()
                            p=Professor(user=user,profprofilepic=profprofilepic)
                            p.save()
                            q=request.POST.getlist('allcourses')
                            di=[]
                            k=""
                            print(q)
                            for obj in q:
                                if Course.objects.filter(course_name=obj).exists():
                                    if Course.objects.filter(course_name=obj).first().professor is None:
                                        x=Course.objects.filter(course_name=obj)
                                        print(x)
                                        for y in x:
                                            y.professor=p
                                            y.save()
                                    else:
                                        k=k+obj+'takenby'+Course.objects.filter(course_name=obj).first().professor.user.username+","
                                    
                                else:
                                    continue
                        else:
                            messages.info(request,"email taken,please register again")
                            return redirect('/adminlogin/admin/professor')

                    else:
                        messages.info(request,"username Taken,please register again")
                        return redirect("/adminlogin/admin/addprofessor")

        
                else:
                    messages.info(request,"Please select atleast one checkbox")
                    return redirect("/adminlogin/admin/addprofessor")
                s="This courses are already taken:"+k+"for all other courses registered "
                messages.info(request,s)
                return redirect("/adminlogin/admin/addprofessor")
        def REMOVESTUDENT(self,request):
            if request.method=='GET':
                obj=Student.objects.all()
                semesters=['1','2','3','4','5','6','7','8']
                branches=['CSE','ECE','ME','EE']
                return render(request,"removestudent.html",{'obj':obj,'semesters':semesters,'branches':branches})
            if request.method=='POST':
                if len(request.POST.getlist('removestudents'))>0:

                    listofpk=request.POST.getlist('removestudents')
                    for i in listofpk:
                        User.objects.filter(id=Student.objects.get(id=int(i)).user.id).delete()
                    return redirect("/adminlogin/admin/removestudent")

                    
                    




                    
                    
                    

                else:
                    
                    messages.info(request,"please select atleast one student")
                    return redirect("/adminlogin/admin/removestudent")
                    
        def REMOVEPROFESSOR(self,request):
            if request.method=="GET":
                k=Professor.objects.all()
              
                maindi=dict()

                for j in k:
                    li=[]
                    if j.course_set.all().exists():
                        for p in j.course_set.all():
                            li.append(p.course_name)
                    
                    li=list(set(li))
                    maindi[j]=li
                    
                    
                    
                return render(request,"removeprofessor.html",{'maindi':maindi})
            if request.method=="POST":
                if len(request.POST.getlist('removeprofessors'))>0:
                    querylist=request.POST.getlist('removeprofessors')

                    for i in querylist:
                        User.objects.filter(id=Professor.objects.get(id=int(i)).user.id).delete()
                    return redirect("/adminlogin/admin/removeprofessor")
                else:
                    messages.info(request,"please select atleast one option before submitting")
                    return redirect("/adminlogin/admin/removeprofessor")

        def UPDATESTUDENTINFO(self,request,name):
            if request.method=='GET':
                k=User.objects.get(username=name)
                return render(request,"updatestudentinfo.html",{'k':k})
            if request.method=='POST':
                a=User.objects.get(username=name).username
                b=User.objects.get(username=name).email
                if User.objects.filter(username=request.POST['studentid']).exists() and a!=request.POST['studentid']:
                        messages.info(request,"studentid already taken")
                        return redirect("/adminlogin/admin/updatestudentinfo/"+name)
                else:
                    if User.objects.filter(email=request.POST['email']).exists() and b!=request.POST['email']:
                            messages.info(request,"email already taken")
                            return redirect("/adminlogin/admin/updatestudentinfo/"+name)
                    else:

                        s=Student.objects.get(id=User.objects.get(username=name).student.id)
                        s.courses.clear()
                        s.save()
                        s.user.email=request.POST["email"]
                        s.semester=request.POST["semester"]
                        s.branch=request.POST["branch"]
                        s.user.username=request.POST["studentid"]
                        s.user.save()
                        s.save()
                        for i in Course.objects.filter(semester=request.POST['semester'],branch=request.POST['branch']):
                            s.courses.add(i)
                            s.save()
                        messages.info(request,"updated successfully")
                        return redirect("/adminlogin/admin")
        def UPDATEPROFESSORINFO(self,request,name):
            if request.method=="GET":
                k=User.objects.get(username=name)
                q=k.professor.course_set.all()
                l=[]
                for i in q:
                    l.append(i.course_name)
                l=list(set(l))
                
                return render(request,"updateprofessorinfo.html",{'k':k,'l':l})
            if request.method=="POST":
                a=User.objects.get(username=name).username
                b=User.objects.get(username=name).email
                if len(request.POST.getlist("allcourses")) >0:
                    if User.objects.filter(username=request.POST['professorid']).exists() and a!=request.POST['professorid']:
                        messages.info(request,"Professorid already taken")
                        return redirect("/adminlogin/admin/updateprofessorinfo/"+name)
                    
                    else:
                        if User.objects.filter(email=request.POST['email']).exists() and b!=request.POST['email']:
                            messages.info(request,"email already taken")
                            return redirect("/adminlogin/admin/updateprofessorinfo/"+name)
                        else:
                            p=Professor.objects.get(id=User.objects.get(username=name).professor.id)
                            p.course_set.clear()
                            p.save()
                            p.user.email=request.POST["email"]
                            p.user.username=request.POST["professorid"]
                            p.user.save()
                            p.save()
                            q=request.POST.getlist('allcourses')
                            print(q)
                            for obj in q:
                                if Course.objects.filter(course_name=obj).exists():
                                    x=Course.objects.filter(course_name=obj)
                                    print(x)
                                    for y in x:
                                        y.professor=p
                                        y.save()
                                else:
                                    continue
                            messages.info(request,"Updated Successfully")
                            return redirect("/adminlogin/admin")

                else:
                    messages.info(request,"Courses not selected")
                    return redirect("/adminlogin/admin/updateprofessorinfo/"+name)
        def RESCHEDULECOURSE(self,request):
            if request.method=="GET":
                f=CourseForm()
                return render(request,"reschedulecourse.html",{'form':f})
            if request.method=="POST":
                course_name=request.POST['course_name']
                if Course.objects.filter(course_name=course_name).exists():
                    monlen=len(request.POST.getlist("MONDAY"))
                    tueslen=len(request.POST.getlist("TUESDAY"))
                    wedlen=len(request.POST.getlist("WEDNESDAY"))
                    thulen=len(request.POST.getlist("THURSDAY"))
                    frilen=len(request.POST.getlist("FRIDAY"))
                    li=["MONDAY","TUESDAY","WEDNESDAY","THURSDAY","FRIDAY"]
                    spots=dict()
                    sem=Course.objects.filter(course_name=course_name).first().semester
                    bran=Course.objects.filter(course_name=course_name).first().branch
                    f=0
                    flag=""
                    prof=Course.objects.filter(course_name=course_name).first().professor
                    if monlen+tueslen+wedlen+thulen+frilen>0:
                        for i in li:
                            if len(request.POST.getlist(i))>0:
                                
                                Course.objects.filter(course_name=course_name,day=i).delete()
                                for j in request.POST.getlist(i):
                                    if Course.objects.filter(semester=sem,branch=bran,day=i,time=j).exists():
                                        if i in spots:
                                            spots[i]=spots[i]+","+j
                                        else:
                                            spots[i]=j
                                        f=1
                                        continue
                                    else:
                                        c=Course(course_name=course_name,semester=sem,branch=bran,day=i,time=j,professor=prof)
                                        c.save()
                                        s=Student.objects.filter(semester=sem,branch=bran)
                                        for stu in s:
                                            stu.courses.add(c)
                                            stu.save()
                            else:
                                continue

                        if f==1:
                            for key in spots:
                                flag=flag+key+"-"+spots[key]+","
                        
                            messages.info(request,"These spots are already taken:-"+flag+"all other spots are rescheduled successfully")
                            return redirect("/adminlogin/admin/reschedulecourse")




                        messages.info(request,"course rescheduled successfully")
                        return redirect("/adminlogin/admin/reschedulecourse")
                    else:
                        messages.info(request,"select atleast one spot")
                        return redirect("/adminlogin/admin/reschedulecourse")
                else:
                    messages.info(request,"course not found")
                    return redirect("/adminlogin/admin/reschedulecourse")
        
        def SHOWTIMETABLE(self,request,branch,semester):
            a=Course.objects.filter(branch=branch,semester=semester)
            monday=dict()
            tuesday=dict()
            wednesday=dict()
            thursday=dict()
            friday=dict()
            br=branch
            sem=semester
            li=[monday,tuesday,wednesday,thursday,friday]
            for k in a:
                if k.day=="MONDAY":
                    monday[k.time]=k.course_name
                if k.day=="TUESDAY":
                    tuesday[k.time]=k.course_name
                if k.day=="WEDNESDAY":
                    wednesday[k.time]=k.course_name
                if k.day=="THURSDAY":
                    thursday[k.time]=k.course_name
                if k.day=="FRIDAY":
                    friday[k.time]=k.course_name
            di={'h':10}
            for i in li:
                if "10:00-11:00" not in i:
                    i["a"]="-"
                else:
                    p=i["10:00-11:00"]
                    del i["10:00-11:00"]
                    i["a"]=p
                if "11:00-12:00" not in i:
                    i["b"]="-"
                else:
                    p=i["11:00-12:00"]
                    del i["11:00-12:00"]
                    i["b"]=p
                if "14:00-15:00" not in i:
                    i["c"]="-"
                else:
                    p=i["14:00-15:00"]
                    del i["14:00-15:00"]
                    i["c"]=p
                if "15:00-16:00" not in i:
                    i["d"]="-"
                else:
                    p=i["15:00-16:00"]
                    del i["15:00-16:00"]
                    i["d"]=p
            
            print(monday)
            return render(request,"spotstimetable.html",{'branch':br,'semester':sem,'monday':monday,'tuesday':tuesday,'wednesday':wednesday,'thursday':thursday,'friday':friday,'di':di})


        def QUERIESFROMSTUDENTS(self,request):
            if request.method=='GET':
                q=Query.objects.filter(send_status=1,answered_status=False)
                return render(request,"queriesfromstudents.html",{'q':q})
        def QUERIESFROMSTUDENTSANDRESPOND(self,request,id):
            if request.method=="GET":
                question=Query.objects.get(id=id).question
                f=QueryFormResponse()
                return render(request,"respondtoqueriesfromstudents.html",{'question':question,'form':f})
            if request.method=="POST":
                if request.POST['answer']=="":
                    messages.info(request,"pleaserespond")
                    return redirect("/adminlogin/admin/queriesfromstudents/"+str(id))
                else:
                    q=Query.objects.get(id=id)
                    q.answered_status=True
                    q.answer=request.POST['answer']
                    q.save()
                    messages.info(request,"response submitted")
                    return redirect("/adminlogin/admin/managequeries")
        
        def QUERIESFROMPROFESSORS(self,request):
            if request.method=='GET':
                q=Query.objects.filter(send_status=2,answered_status=False)
                d=dict()
                for i in q:
                    li=[]
                    se=i.from_prof.course_set.all()
                    for j in se:
                        li.append(j.course_name)
                    li=list(set(li))

                    d[i]=li
                return render(request,"queriesfromprofessors.html",{'d':d})
        def QUERIESFROMPROFESSORSANDRESPOND(self,request,id):
            if request.method=="GET":
                question=Query.objects.get(id=id).question
                f=QueryFormResponse()
                return render(request,"resquefromprof.html",{'question':question,'form':f})
            if request.method=="POST":
                if request.POST['answer']=="":
                    messages.info(request,"pleaserespond")
                    return redirect("/adminlogin/admin/queriesfromprofessors/"+str(id))
                else:
                    q=Query.objects.get(id=id)
                    q.answered_status=True
                    q.answer=request.POST['answer']
                    q.save()
                    messages.info(request,"response submitted")
                    return redirect("/adminlogin/admin/managequeries")