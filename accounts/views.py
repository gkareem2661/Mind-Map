from django.contrib.auth import login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def signup(request):
    """User registration view using Django's built-in form."""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})


def logout_view(request):
    """Log out and return to login page."""
    auth_logout(request)
    return redirect('login')
