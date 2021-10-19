from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.homepage,name="homepage"),
    path('notices',views.notices,name="notices"),
    path('contact',views.contact,name="contact"),
    path('studentlogin',views.studentlogin,name="studentlogin"),
    path('stafflogin',views.stafflogin,name="stafflogin"),
    path('adminlogin',views.adminlogin,name="adminlogin"),
    

]
