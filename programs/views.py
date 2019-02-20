from django.shortcuts import render
from .models import Programs
from django.contrib.auth.decorators import login_required
import time, datetime
from django.http import HttpResponseRedirect
# Create your views here.


@login_required
def programs(request):
	username = request.user.username
	group = request.user.groups.all()
	program_list = Programs.objects.all()
	context = {
		'programs': program_list,
		'user': username,
		'group': str(group[0])
	}
	if request.method == "POST":
		file = open("program_access.log", "a")
		file.write(log_write(username, request.POST['programs']))
		file.close()
		context['accessed'] = request.POST['programs']
		return render(request, 'programs.html', context=context)
	return render(request, 'programs.html', context=context)



def log_write(username, application):
	return_string = "Application access\n"
	return_string += "Time: " + str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')) + "\n"
	return_string += "Username: " + username + "\n"
	return_string += "Application: " + application + "\n----------------------------\n"
	return return_string
