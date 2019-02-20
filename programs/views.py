from django.shortcuts import render, redirect
from .models import Programs
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import time, datetime
# Create your views here.


@login_required
def programs(request):
	username = request.user.username
	group = request.user.groups.all()
	program_list = Programs.objects.all()
	try:
		context = {
			'programs': program_list,
			'user': username,
			'group': str(group[0])
		}
	except IndexError:
		messages.error(request, f'{username} is not in any group, contact an administrator')
		return redirect('/')
	if request.method == "POST":
		file = open("program_access.log", "a")
		file.write(log_write(username, request.POST.get('programs', 'nothing')))
		file.close()
		context['accessed'] = request.POST.get('programs', 'nothing')
		return render(request, 'programs.html', context=context)
	return render(request, 'programs.html', context=context)


def log_write(username, application):
	if application == 'nothing':
		return ''
	return_string = "Application access\n"
	return_string += "Time: " + str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')) + "\n"
	return_string += "Username: " + username + "\n"
	return_string += "Application: " + application + "\n----------------------------\n"
	return return_string
