from django import forms
from secretaria.models import Agendamento

class AgendamentoMonitorForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        exclude = ('status', 'user', 'opicional')