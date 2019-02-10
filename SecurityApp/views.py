from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect


def home(request):

    if request.method == "POST":
        if request.POST['logon']:
            return logon(request)

    return render(request, 'SecurityApp/home.html')
# Create your views here.


def logon(request):
    username = request.POST['username']
    password = request.POST['password']
    authentication = authenticate(request, username=username, password=password)
    if authentication is not None:
        login(request, authentication)
        # the only page we can redirct to is the program page, so no need for it to be dynamic
        return HttpResponseRedirect('programs')
    context = {'logon_failed': True}
    return render(request, 'SecurityApp/home.html', context=context)
