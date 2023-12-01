from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Tarefa
from .forms import FormularioTarefa

from django.core import serializers
from django.http import HttpResponse
import json
import zipfile
from io import BytesIO
import datetime

@login_required
def tarefas(request):
    search = request.GET.get('search')
    filter = request.GET.get('filter')

    if search:
        tarefas = Tarefa.objects.filter(titulo__icontains=search, user=request.user)

    elif filter:
        tarefas = Tarefa.objects.filter(status=filter, user=request.user)

    else:

        lista_tarefas = Tarefa.objects.all().order_by('-criado').filter(user=request.user)

        paginator = Paginator(lista_tarefas, 6) # Limita a quantidade de tarefas que serão exibidas na tela

        page = request.GET.get('page')

        tarefas = paginator.get_page(page)

    return render(request, 'tarefas.html', {'tarefas': tarefas})

@login_required
def detalhes(request, id):
    tarefa = get_object_or_404(Tarefa, pk=id)
    return render(request, 'detalhes.html', {'tarefa': tarefa})

@login_required
def novaTarefa(request):
    if request.method == 'POST':
        formulario = FormularioTarefa(request.POST)
        
        if formulario.is_valid():
            tarefa = formulario.save(commit=False)
            tarefa.status = 'fazendo'
            tarefa.user = request.user
            tarefa.save()
            return redirect('/tarefas/')
    else:
        formulario = FormularioTarefa()
        return render(request, 'novatarefa.html', {'form': formulario})
    
@login_required   
def editar(request, id):
    tarefa = get_object_or_404(Tarefa, pk=id)
    formulario = FormularioTarefa(instance=tarefa)

    if(request.method == 'POST'):
        formulario = FormularioTarefa(request.POST, instance=tarefa)

        if(formulario.is_valid()):
            tarefa.save()
            return redirect('/tarefas/')
        else:
            return render(request, 'editartarefa.html', {'form': formulario, 'tarefa': tarefa})
    else:
        return render(request, 'editartarefa.html', {'form': formulario, 'tarefa': tarefa})

@login_required
def delete(request, id):
    tarefa = get_object_or_404(Tarefa, pk=id)
    tarefa.delete()

    messages.info(request, 'Tarefa deletada com sucesso')

    return redirect('/tarefas/')

@login_required
def mudarStatus(request, id):
    tarefa = get_object_or_404(Tarefa, pk=id)

    if tarefa.status == 'fazendo':
        tarefa.status = 'concluido'
    else:
        tarefa.status = 'fazendo'

    tarefa.save()

    return redirect('/tarefas/')

def exportar_dados_para_json(request):
    # Substitua isso pelos dados da sua aplicação

    # Substitua isso pela query do seu modelo
    queryset = Tarefa.objects.all().order_by('-criado').filter(user=request.user) # Filtra as tarefas que pertencem ao usuário logado

    # Convertendo o QuerySet para uma lista de dicionários
    lista_tarefas = serializers.serialize('python', queryset, fields=('titulo', 'descricao', 'status', 'user', 'criado', 'atualizado'))  # Substitua 'campo1', 'campo2' pelos campos do seu modelo

    # Convertendo objetos datetime para strings
    for item in lista_tarefas:
        for campo, valor in item['fields'].items():
            if isinstance(valor, datetime.datetime):
                item['fields'][campo] = valor.isoformat()

    # Convertendo os dados para JSON
    dados_json = json.dumps(lista_tarefas)

    # Criando um objeto BytesIO para armazenar o arquivo ZIP
    arquivo_zip = BytesIO()

    # Criando um arquivo ZIP
    with zipfile.ZipFile(arquivo_zip, 'w') as zf:
        zf.writestr('dados_exportados.json', dados_json)

    # Obtendo o conteúdo do arquivo ZIP
    conteudo_zip = arquivo_zip.getvalue()

    # Criando uma resposta com o arquivo ZIP
    response = HttpResponse(conteudo_zip, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=dados_exportados.zip'

    return response
