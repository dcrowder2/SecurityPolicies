from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from SecurityApp import models
from django.contrib.auth.models import User
import re


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        try:
            form.data['username'].encode('ascii')
            if not (re.match(r'(.*[A-Z].*)', form.data['password1']) and re.match(r'(.*[a-z].*)', form.data['password1'])
                    and re.match(r'(.*\d.*)', form.data['password1'])):
                messages.error(request, 'Password must contain an uppercase letter, a lowercase letter, and a digit')
                return redirect('register')
            elif form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                models.Logon(user=User.objects.get(username=username)).save()
                messages.success(request, f'Account created for {username}')
                return redirect('apps-home')
        except UnicodeEncodeError:
            messages.error(request, 'Letters, digits and @/./+/-/_ only.')
            return redirect('register')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})
