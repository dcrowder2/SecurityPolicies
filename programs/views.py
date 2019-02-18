from django.shortcuts import render
from .models import Programs
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def programs(request):
	username = request.user.username
	group = request.user.groups.all()
	context = {
		'programs': Programs.objects.all(),
		'user' : username,
		'group' : group[0]
	}
	if request.method == "POST":
		return render(request, 'programs.html', context=context)
	return render(request, 'programs.html', context=context)
