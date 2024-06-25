from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm


# Create your views here.

def logout(request):
    """Logs out the user."""
    auth.logout(request)
    return HttpResponseRedirect(reverse('home'))


def register(request):
    """Registers a new user."""
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            authenticated = auth.authenticate(username=new_user.username,
                                          password=request.POST['password1'])
            auth.login(request, authenticated)
            return HttpResponseRedirect(reverse('home'))
    
    context = {'form': form}
    return render(request, 'register.html', context)
