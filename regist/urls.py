from . import views
from django.urls import path
urlpatterns = [

    path('',views.login,name='login'),
    path("home",views.home,name='home'),
    path("signup",views.signup,name='signup'),
    path("signedup",views.signedup,name='signedup'),
    path("loggedin",views.loggedin,name='loggedin'),
    path("logout",views.logout,name='logout'),
    path("adminlogin",views.adminlogin,name='adminlogin'),
    path("adminloggedin",views.adminloggedin,name='adminloggedin'),
    path("adminhome",views.adminhome,name='adminhome'),
    path('edit/<int:pk>',views.edit,name='edit'),
    path('update/<int:pk>',views.update,name='update'),
    path('delete/<int:pk>',views.delete,name='delete'),
    path('adminlogout',views.logout,name='logout'),
    path('createsuperuser',views.createsuperuser,name='createsuperuser'),
    path('adminsignedup',views.adminsignedup,name='adminsignedup'),
    path('adminlogout',views.adminlogout,name='adminlogout'),
    path('shoulddelete/<int:pk>',views.shoulddelete,name='shoulddelete')
   
]
