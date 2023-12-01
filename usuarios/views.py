from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages

def home(request):
    return render(request, 'home.html')

def cadastro(request): # TODO !!Fazer o cadastro com o próprio django!!
    if request.method == "GET":
        return render(request, 'cadastro.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        user = User.objects.filter(username=username).first()

        if user:
            messages.success(request, 'Usuário já cadastrado!')
            return render(request, 'cadastro.html') #mensagem que existe um usuario com esse nome
        
        user = User.objects.create_user(username=username, email=email, password=senha)
        user.save()

        return render(request, 'registration/login.html')
    
def sobre(request):
    return render(request, 'sobre.html')
                    