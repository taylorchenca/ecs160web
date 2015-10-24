from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader, Context
from django.shortcuts import render, render_to_response, redirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import JsonResponse
import re
from simple_email_confirmation import *
from django.contrib.auth import login as django_login, authenticate, logout as django_logout
from django.core.mail import send_mail


from .forms import AuthenticationForm, RegistrationForm

media = '/home/apmishra100/ecs160/media'
# Create your views here.

def index(request):
    template = loader.get_template('warcraft/index.html')
    return HttpResponse(template.render())
    

def prototype_form(request):
    template = loader.get_template('warcraft/prototype_form.html')
    return HttpResponse(template.render())

def prototype(request):
    error = False
    message=""
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            error = True
            message = "BAD INPUT"
            return render(request, 'warcraft/prototype_form.html', {'error':error, 'message':message})
        else:
            message = '%s' %request.GET['q']
            if message == "":
                message = "BAD INPUT"
                return render(request, 'warcraft/prototype_form.html', {'error':True, 'message':message})
            else:
                return render(request, 'warcraft/prototype_form.html', {'error':error, 'message':message})
    else:
        return render(request, 'warcraft/prototype_form.html', {'error':error, 'message':message})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(userName=request.POST['userName'], password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    django_login(request, user)
                    return redirect('/accounts/loggedin')
                else:
                    message = "You are not a verified user, please check your email."
                    return render(request, 'warcraft/invalid_login.html', {'user_name': "",'message':message})
            else:
                return HttpResponseRedirect('/accounts/invalid')
        else:
            print form.errors
    else:
        form = AuthenticationForm()
    return render_to_response('warcraft/login.html', {'form': form,}, context_instance=RequestContext(request))

'''def auth_view(request):
    username = request.POST.get('username','')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        if user.is_active is not False:
            auth.login(request, user)
            return HttpResponseRedirect('/accounts/loggedin')
        else:
            message="You are not a verified user, please check your email."
            return render(request, 'warcraft/invalid_login.html', {'user_name': request.user.username,'message':message})  
    else:
        return HttpResponseRedirect('/accounts/invalid')'''
        
def logout(request):
    django_logout(request)
    return render_to_response('warcraft/logout.html')

def loggedin(request):
    picture = request.user.picture
    fname = request.user.firstName
    lname = request.user.lastName
    return render(request, 'warcraft/loggedin.html', {'full_name': fname+" "+lname, 'avatar':picture})

def invalid_login(request):
    message= "Invalid login credentials"
    emptystring=""
    return render(request, 'warcraft/invalid_login.html', {'user_name':emptystring, 'message':message})
    
    
def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            message = "Please visit http://apmishra100.koding.io/accounts/activate and use the key %s to activate your account." % user.confirmation_key
            send_mail('Activate your account', message, None, [user.email])
            return redirect('/accounts/register_success')
    else:
        form = RegistrationForm()
    return render_to_response('warcraft/register.html', {'form': form,}, context_instance=RequestContext(request))
    

def register_success (reqest):
    return render_to_response('warcraft/register_success.html')

def internalLogin (request):
    if request.method == 'GET':
        username = request.META['HTTP_USERNAME']
        password = request.META['HTTP_PASSWORD']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active is not False:
                auth.login(request, user)
                return JsonResponse({'LoginStatus': 'Success'})
            else:
                return JsonResponse({'LoginStatus': user.confirmation_key, 'Email': user.email} )
        else:
            return JsonResponse({'LoginStatus': 'Incorrect Credentials'})
