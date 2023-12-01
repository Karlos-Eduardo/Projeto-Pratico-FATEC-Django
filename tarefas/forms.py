from django import forms

from .models import Tarefa

class FormularioTarefa(forms.ModelForm):

    class Meta:
        model = Tarefa
        fields = ('titulo', 'descricao')