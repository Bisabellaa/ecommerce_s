from django.shortcuts import render, redirect
from django.contrib import messages, auth
from .models import Account


def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Has iniciado sesión correctamente.')
            return redirect('home')
        else:
            messages.error(request, 'Credenciales inválidas.')
            return redirect('signin')
    return render(request, 'accounts/signin.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        user = Account.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            password=password
        )
        messages.success(request, 'Registro exitoso. Ahora podés iniciar sesión.')
        return redirect('signin')
    return render(request, 'accounts/register.html')


def logout(request):
    auth.logout(request)
    messages.success(request, 'Has cerrado sesión.')
    return redirect('home')
