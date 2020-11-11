from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login, authenticate
from django.contrib import messages


# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            messages.success(request, 'Logged in successfully!')
            login(request, user)
            return redirect("logger:index")
        messages.error(request, 'Error creating user')
        
    form = RegisterForm()

    return render(request, "register/register.html", {"form": form})
