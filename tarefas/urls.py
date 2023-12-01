from django.urls import path
from . import views

urlpatterns = [
    path('tarefas/', views.tarefas, name='tarefas'),
    path('novatarefa/', views.novaTarefa, name='nova-tarefa'),
    path('detalhes/<int:id>', views.detalhes, name='detalhes'),
    path('editartarefa/<int:id>', views.editar, name='editar-tarefa'),
    path('delete/<int:id>', views.delete, name='delete-tarefa'),
    path('mudarstatus/<int:id>', views.mudarStatus, name='mudar-status'),
    path('exportar/', views.exportar_dados_para_json, name='exportar_dados_para_json'),
]