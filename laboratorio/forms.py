from django import forms
from .models import Laboratorio
from django.core.exceptions import ValidationError
import re
class LaboratorioForm(forms.ModelForm):
    class Meta:
        model = Laboratorio
        fields = '__all__'

    """def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        qt_maquinas = cleaned_data.get("qt_maquinas")
        if not name:
            raise ValidationError("Campo titulo é obrigatório.")
        if not qt_maquinas:
            raise ValidationError("Campo quantidade máquina é obrigatório.")
        if Laboratorio.objects.filter(name__iexact=name).exists():
            raise ValidationError('Já existe um laboratório com esse mesmo nome.')
        """