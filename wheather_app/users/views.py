from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import RegisterForm


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Вход в систему после регистрации
            return redirect("weather")  # Перенаправление на страницу погоды
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})
