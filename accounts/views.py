from django.shortcuts import render


def signin(request):
    return render(request, 'accounts/signin.html')


def register(request):
    return render(request, 'accounts/register.html')
