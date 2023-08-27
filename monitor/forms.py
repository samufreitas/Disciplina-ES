from django import forms
import re
from datetime import datetime,date
from secretaria.models import Agendamento
from django.core.exceptions import ValidationError
class AgendamentoMonitorForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        exclude = ('status', 'user', 'tipo')

    def clean(self):
        cleaned_data = super().clean()
        hora_inicio = cleaned_data.get("hora_inicio")
        hora_fim = cleaned_data.get("hora_fim")
        data = cleaned_data.get("data")
        laboratorio = cleaned_data.get("laboratorio")
        titulo = cleaned_data.get("titulo")
        if not titulo:
            raise ValidationError("Campo obrigatório.")
        if re.match(r'^[0-9!@#$%^&*()_+{}\[\]:;<>,.?~\\/\\\'"\\-]*$', titulo):
            raise ValidationError('O título não pode conter apenas números ou caracteres especiais.')


        if not laboratorio:
            raise ValidationError("Campo obrigatorio!")
        if not hora_inicio:
            raise ValidationError("Campo obrigatorio!")

        hora_atual = datetime.now()
        hora_atual = hora_atual.replace(second=0, microsecond=0)
        data_atual = datetime.now().date()
        if data == data_atual:
            if hora_inicio < hora_atual.time():
                raise ValidationError(f"Este horário é menor que o horário atual!")
        if not hora_fim:
            raise ValidationError("Campo obrigatorio!")
        if not data:
            raise ValidationError("Campo obrigatorio!")

        data_atual = datetime.now().date()
        if data < data_atual:
            data_atual_formatada = data_atual.strftime('%d/%m/%Y')
            raise ValidationError(f"Essa data ja passou hoje é dia {data_atual_formatada}!")

        if hora_fim == hora_inicio:
            raise ValidationError("Os dois horário de início e fim são iguais!")
        if hora_fim < hora_inicio:
            raise ValidationError("O horário de início é menor que o final!")