from email import message
from pickle import NONE
from urllib import request, response
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.views.decorators.cache import never_cache
# Create your views here.
@never_cache
def login(request):
   if 'username' in request.session and 'username' in request.COOKIES:
      if request.session['username']==request.COOKIES['username']:
         name= request.COOKIES['username']
         getuser=User.objects.get(username=name)
         if getuser is not None:
            if getuser.is_superuser is True:
               return redirect('adminhome')
            else :
               return render(request,'home.html',{'name':name})
         else:
            return render(request,'login.html')
   else:
      return render(request,'login.html') #showing login page

@never_cache
def home(request):
    if 'username' in request.session or 'username' in request.COOKIES:
      name=request.session['username']
      getuser=User.objects.get(username=name)
      if getuser is not None:
         if getuser.is_superuser is True:
            return redirect('adminhome')
         else:      
            return render(request,'home.html',{'name':name})
      else:      
         return render(request,'home.html',{'name':name})
    else:
      return render(request,'login.html') 

def signup(request):
   return render(request,'signup.html')

def signedup(request):
   if request.method=="POST":
      name=request.POST.get('name')
      email=request.POST.get('email')
      password1=request.POST.get('password1')
      password2=request.POST.get('password2')

      if password1==password2:
         if User.objects.filter(username=name).exists():
           messages.info(request,"User exist")
           return render(request,'signup.html')
         elif User.objects.filter(email=email).exists():
            messages.info(request,"Email exist")
            return render(request,'signup.html')
         else:
            user= User.objects.create_user(username=name,email=email,password=password1)
            user.save()
   
      else:
         messages.info(request,"Invalid password")
         return render(request,'signup.html')
      return render(request,'login.html') #showing login page
   else:
      print("nice")
      return render(request,'login.html') #showing login page

@never_cache
def loggedin(request):
   name=request.POST.get('name')
   password=request.POST.get('password')
   
   
   user=auth.authenticate(username=name,password=password)
   response = redirect('/home')
   if user is not None:
      bool=user.is_superuser
      if bool is True: 
         messages.info(request,"Login using Admin panel")
         return render(request,'login.html')
      
      response.set_cookie('username',name)
      request.session['username']=name
      return response
   
   else:
      messages.info(request,"Invalid Credentials")
      return render(request,'login.html') #showing login page

def logout(request):
   response=redirect('/')
   if 'username' in request.session or 'username' in request.COOKIES:
      
      request.session.flush()
      response.delete_cookie('username')
   return response

def adminlogin(request):
   #-----------------------

   return render(request,'adminlogin.html')

@never_cache
def adminloggedin(request):
   name=request.POST.get('name')
   password=request.POST.get('password')
   
   
   user=auth.authenticate(username=name,password=password)
   if user is not None and user.is_superuser:
      #response = redirect('/adminhome',{'name':name})
      #key1=User.objects.all()
      response = redirect('/adminhome')
      #auth.login(request,user)
      response.set_cookie('username',name)
      request.session['username']=name
      
      return response
      
   else:
      messages.info(request,"Invalid Credentials")
      return render(request,'adminlogin.html') 

@never_cache
def adminhome(request):
   
   if request.method=='POST':
       if 'username' in request.session and 'username' in request.COOKIES:
         if request.session['username']==request.COOKIES['username']:
            name= request.COOKIES['username']
            sear=request.POST['search']
            print(sear)
            if sear != "search" :
               
               getsearcheddata=User.objects.filter(username__contains=sear)
               return render(request,'adminhome.html',{'key1':getsearcheddata,'name':name})
            
            elif sear == "search" or sear =="":
               getsearcheddata=User.objects.all().order_by('is_superuser')
               print("getingin")
               return render(request,'adminhome.html',{'key1':getsearcheddata,'name':name})
            
            
            name= request.COOKIES['username']
            key1=User.objects.all()
            return render(request,'adminhome.html',{'key1':key1,'name':name})
   
   
   else:
      print('GET')
      if 'username' in request.session and 'username' in request.COOKIES:
         if request.session['username']==request.COOKIES['username']:
            name= request.COOKIES['username']
            key1=User.objects.all()
            return render(request,'adminhome.html',{'key1':key1,'name':name})
            #return render(request,'home.html',{'name':name})
   
      else:
         return render(request,'login.html')
      #------------------------------------
   name= request.COOKIES['username']
   key1=User.objects.all()
   return render(request,'adminhome.html',{'key1':key1,'name':name})

@never_cache
def edit(request,pk):
   
   get_data=User.objects.get(id=pk)
   if 'username' in request.session and 'username' in request.COOKIES:
         if request.session['username']==request.COOKIES['username']:
            return render(request,'editpage.html',{'key2':get_data})
   else:
      return render(request,'login.html')
      
@never_cache
def update(request,pk):
   
   
   get_data=User.objects.get(id=pk)
   get_data.username=request.POST["name"]
   get_data.email=request.POST["email"]
   get_data.is_superuser=request.POST["is_superuser"]
   if(get_data.is_superuser!=True or get_data.is_superuser!=False):
      get_data.is_superuser=False

   get_data.save()
   key1=User.objects.all()
   name= request.COOKIES['username']
   return render(request,'adminhome.html',{'key1':key1,'name':name})

@never_cache
def shoulddelete(request,pk):
   
   if 'username' in request.session and 'username' in request.COOKIES:
         if request.session['username']==request.COOKIES['username']:
            
            ddata=User.objects.get(id=pk)
            dname=ddata.username
            name= request.COOKIES['username']
            # kname=request.User.objects.username
            # kname=request.username
            # print(kname +" success ") 
            return render(request,'shoulddelete.html',{'dname':dname,'pk':pk,'name':name})
   else:
      return render(request,'login.html')

@never_cache
def delete(request,pk):
   
   response= redirect('adminhome')
   ddata=User.objects.get(id=pk)
   ddata.delete()
   key1=User.objects.all()
   name= request.COOKIES['username']
   return response
   return render(request,'adminhome.html',{'key1':key1,'name':name})

def createsuperuser(request):
   if 'username' in request.session and 'username' in request.COOKIES:
         if request.session['username']==request.COOKIES['username']:
            return render(request,'createuser.html')
   else:
      return render(request,'login.html')

def adminsignedup(request):
    if request.method=="POST":
      name=request.POST.get('name')
      email=request.POST.get('email')
      password1=request.POST.get('password1')
      password2=request.POST.get('password2')

      if password1==password2:
         if User.objects.filter(username=name).exists():
           messages.info(request,"User exist")
           return render(request,'signup.html')
         elif User.objects.filter(email=email).exists():
            messages.info(request,"Email exist")
            return render(request,'signup.html')
         else:
            user= User.objects.create_user(username=name,email=email,password=password1,is_superuser=True)
            user.save()
   
      else:
         messages.info(request,"Invalid password")
         return render(request,'createuser.html')
      key1=User.objects.all()
      return render(request,'adminhome.html',{'key1':key1})
     
    else:
      print("nice")
      return render(request,'login.html') #showing login page
   
def adminlogout(request):
   return redirect('/')