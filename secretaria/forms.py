from django import forms
from .models import Agendamento, Tipo
from datetime import datetime
import re
from django.core.exceptions import ValidationError

class TipoForm(forms.ModelForm):
    class Meta:
        model = Tipo
        fields = ['titulo']

    def clean_titulo(self):
        titulo = self.cleaned_data['titulo']
        if not titulo:
            raise forms.ValidationError("Campo obrigatório.")
        if Tipo.objects.filter(titulo__iexact=titulo).exists():
            raise forms.ValidationError('Já existe um tipo com esse mesmo título.')
        if re.match(r'^[0-9!@#$%^&*()_+{}\[\]:;<>,.?~\\/\\\'"\\-]*$', titulo):
            raise forms.ValidationError('O título não pode conter apenas números ou caracteres especiais.')
        return titulo


class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        exclude = ('status',)



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

""" def clean_data(self):
        data = self.cleaned_data['data']
        if not data:
            raise forms.ValidationError("Campo obrigatório.")
        data_atual = datetime.now().date()
        if data < data_atual:
            data_atual_formatada = data_atual.strftime('%d/%m/%Y')
            raise forms.ValidationError(f"A data informada já passou, hoje é dia {data_atual_formatada}!")
        return data

    def clean_hora_inicio(self):
        self.hora_inicio = self.cleaned_data['hora_inicio']
        if not self.hora_inicio:
            raise forms.ValidationError("Campo obrigatório.")

        hora_atual = datetime.now()
        hora_atual = hora_atual.replace(second=0, microsecond=0)
        data_atual = datetime.now().date()
        if self.cleaned_data['data'] == data_atual:
            if self.hora_inicio < hora_atual.time():
                raise forms.ValidationError(f"Este horário é menor que o horário atual!")

        if self.hora_inicio == hora_atual:
            raise forms.ValidationError(f"Este horário é igual ao horário atual!")
        return self.hora_inicio


    def clean_hora_fim(self):
        hora_fim = self.cleaned_data['hora_fim']
        if not hora_fim:
            raise forms.ValidationError("Campo obrigatório.")

        hora_atual = datetime.now()
        hora_atual = hora_atual.replace(second=0, microsecond=0)
        data_atual = datetime.now().date()
        if self.cleaned_data['data'] == data_atual:
            if hora_fim < hora_atual.time():
                raise forms.ValidationError(f"Este horário é menor que o horário atual!")

        if hora_fim < self.hora_inicio:
            raise forms.ValidationError(f"Este horário é menor que o horário de início!")

        if hora_fim == self.hora_inicio:
            raise forms.ValidationError(f"Horário de incio igual o horário de fim!")
        return hora_fim

     def clean_titulo(self):
            titulo = self.cleaned_data['titulo']
            if not titulo:
                raise forms.ValidationError("Campo obrigatório.")
                raise forms.ValidationError('O título não pode conter apenas números ou caracteres especiais.')
            return titulo
    def clean_laboratorio(self):
        laboratorio = self.cleaned_data['laboratorio']
        if not laboratorio:
            raise forms.ValidationError("Campo obrigatório.")
        return laboratorio"""