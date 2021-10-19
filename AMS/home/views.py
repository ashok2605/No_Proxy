from django.shortcuts import render

# Create your views here.

def homepage(request):
    if(request.method=='GET'):
        return render(request,'sams.html')
def notices(request):
    if(request.method=='GET'):
        return render(request,'announcements.html')
def contact(request):
    if(request.method=='GET'):
        return render(request,'contactus.html')
def studentlogin(request):
    if(request.method=='GET'):
        return render(request,'studentlogin.html')
def stafflogin(request):
    if(request.method=='GET'):
        return render(request,'stafflogin.html')
def adminlogin(request):
    if(request.method=='GET'):
        return render(request,'adminlogin.html')
