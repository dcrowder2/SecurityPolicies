from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        try:
            name = form.data['username'].encode('ascii')
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'Account created for {username}')
                return redirect('apps-home')
        except UnicodeEncodeError:
            messages.error(request, 'Letters, digits and @/./+/-/_ only.')
            return redirect('register')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})
