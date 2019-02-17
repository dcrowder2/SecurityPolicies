from django.shortcuts import render
from django.contrib.auth import authenticate, login, user_login_failed
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
import datetime, time


__attempts = 0
__exists = False


def home(request):
    if request.method == "POST":
        if request.POST['logon']:
            return logon(request)

    return render(request, 'SecurityApp/home.html')
# Create your views here.


def login_failed(sender, **kwargs):
    global __attempts
    global __exists
    name = kwargs['credentials']['username']
    __exists = False
    if User.objects.exclude().filter(username=name).exists():
        __exists = True
        user = User.objects.get(username=name)
        user.logon.logon_attempts += 1
        user.logon.save()
        if user.logon.logon_attempts >= 5:
            user.logon.user_lockout = True
            user.logon.save()
        __attempts = user.logon.logon_attempts
    return


def logon(request):
    file = open("login.log", "a")
    global __attempts
    username = request.POST['username']
    password = request.POST['password']
    user_login_failed.connect(login_failed)
    authentication = authenticate(request, username=username, password=password)
    if authentication is not None:
        if not authentication.logon.user_lockout:
            file.write(log_write(username, True))
            file.close()
            authentication.logon.logon_attempts = 0
            authentication.logon.save()
            login(request, authentication)
            return HttpResponseRedirect('programs')
        else:
            file.write(log_write(username, False))
            file.close()
            context = {'user_locked_out': True}
            return render(request, 'SecurityApp/home.html', context=context)
    if __exists:
        file.write(log_write(username, False))
        file.close()
        if User.objects.get(username=username).logon.user_lockout:
            context = {'user_locked_out': True}
        else:
            context = {
                'incorrect_login': True,
                'login_attempts': 5 - __attempts
            }
    else:
        file.write(log_write(username, False))
        file.close()
        context = {'not_found': True}
    return render(request, 'SecurityApp/home.html', context=context)


def log_write(username, success):
    return_string = "Login attempt: " + str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d '
                                                                                                  '%H:%M:%S')) + "\n"
    return_string += "Username: " + username + "\n"
    if success:
        return_string += "Successfully logged on\n----------------------------\n"
    elif __exists:
        user = User.objects.get(username=username)
        if user.logon.user_lockout:
            return_string += "User locked out\n----------------------------\n"
        else:
            return_string += "Incorrect password, " + str(user.logon.logon_attempts) + " unsuccessful attempt(s)\n----------------------------\n"
    else:
        return_string += "User does not exist\n----------------------------\n"
    return return_string
