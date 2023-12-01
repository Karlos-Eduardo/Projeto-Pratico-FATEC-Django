from django.contrib import admin
from django.urls import path, include
#from usuarios.views import cadastro, login,
from tarefas.views import tarefas

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('usuarios.urls')),
    path('', include('tarefas.urls')),
]
