from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.http import *
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
import random
import math
from .models import *
from django.db.models import Count, F, Value
# Create your views here.

def homepage(request):
    if(request.method=='GET'):
        
        return render(request,'sams.html')
def nots(request):
    if(request.method=='GET'):
        objs=notices.objects.all()
       
        return render(request,'announcements.html',{'objs':objs})
def contact(request):
    if(request.method=='GET'):
        return render(request,'contactus.html')
def studentlogin(request):
    if(request.method=='GET'):
        return render(request,'studentlogin.html')
    if(request.method=='POST'):
        
        username=request.POST['your_name']
        password=request.POST['your_pass']
        objo=auth.authenticate(username=username,password=password)
        print(request.user.is_authenticated)
        # returns user object if present
        if objo is not None:
            auth.login(request,objo)
            
            if objo.is_superuser==False and objo.is_staff==False:
                
                return redirect("/studentlogin/student")
            else:
                auth.logout(request)
                messages.info(request,"Student details not found or Access denied")
                return redirect("/studentlogin")
        else:
            messages.info(request,"STUDENT NOT FOUND ,PLEASE CHECK YOUR USERNAME AND PASSWORD AGAIN")
            return redirect("/studentlogin")
def sthome(request):
    if(request.method=='GET'):
        return render(request,'stproj.html')
def stlogout(request):
    auth.logout(request)
    
    return redirect("/")
def stafflogin(request):
    if(request.method=='GET'):
        return render(request,'stafflogin.html')
    if request.method=="POST":
        username=request.POST['your_name']
        password=request.POST['your_pass']
        objo=auth.authenticate(username=username,password=password,is_superuser=False,is_staff=True)
        print(request.user.is_authenticated)
        # returns user object if present
        if objo is not None:
            auth.login(request,objo)
            if objo.is_staff==True and objo.is_superuser==False:
                return redirect("/stafflogin/staff")
            else:
                auth.logout(request)
                messages.info(request,"Staff details not found or access denied")
                return redirect("/stafflogin")
        else:
            messages.info(request,"Staff NOT FOUND ,PLEASE CHECK YOUR USERNAME AND PASSWORD AGAIN")
            return redirect("/stafflogin")
def staffhome(request):
    if request.method=='GET':
        return render(request,'staffproj.html')
def stafflogout(request):
    auth.logout(request)
    
    return redirect("/")
def adminlogin(request):
    if(request.method=='GET'):
      
        return render(request,'adminlogin.html')
    if(request.method=='POST'):
        username=request.POST['admin_username']
        password=request.POST['admin_password']
        objo=auth.authenticate(username=username,password=password)
        print(request.user.is_authenticated)
        # returns user object if present
        if objo is not None:
            auth.login(request,objo)
            if objo.is_superuser==True:
                return redirect("/adminlogin/admin")
            else:
                auth.logout(request)
                messages.info(request,"Admin details not found or access denied")
                return redirect('/adminlogin')
        else:
            messages.info(request,"ADMIN NOT FOUND ,PLEASE CHECK YOUR USERNAME AND PASSWORD AGAIN")
            return redirect("/adminlogin")
def adlog(request):
    if(request.method=='GET'):
        return render(request,'proj.html')
def checkout(request):
    auth.logout(request)
    
    return redirect("/")
