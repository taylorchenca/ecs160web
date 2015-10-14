from django.http import HttpResponse
from django.template import RequestContext, loader, Context
from django.shortcuts import render, render_to_response, redirect
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