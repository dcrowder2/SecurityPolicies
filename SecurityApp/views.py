from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect



def home(request):

    if request.method == "POST":
        if request.POST['logon']:
            context = { 'logon_attempts': user.attempts}
            return logon(request, context)

    return render(request, 'SecurityApp/home.html')
# Create your views here.


def logon(request, context):
    username = request.POST['username']
    password = request.POST['password']
    authentication = authenticate(request, username=username, password=password)
    if authentication is not None:
        login(request, authentication)
        # the only page we can redirct to is the program page, so no need for it to be dynamic
        return HttpResponseRedirect('programs')
    context['logon_failed'] = True
    context['logon_attempts']
    return render(request, 'SecurityApp/home.html', context=context)
