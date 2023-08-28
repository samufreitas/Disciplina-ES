# forms.py
from django import forms
from django.contrib.auth.models import User, Group
import re
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class UserForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'groups', 'password']

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if not first_name:
            raise ValidationError("Campo obrigatório.")
        if re.match(r'^[0-9!@#$%^&*()_+{}\[\]:;<>,.?~\\/\\\'"\\-]*$', first_name):
            raise forms.ValidationError('O nome não pode conter apenas números ou caracteres especiais.')
        if not last_name:
            raise ValidationError("Campo obrigatório.")
        if re.match(r'^[0-9!@#$%^&*()_+{}\[\]:;<>,.?~\\/\\\'"\\-]*$', last_name):
            raise forms.ValidationError('O sobrenome não pode conter apenas números ou caracteres especiais.')

        if not username:
            raise ValidationError("Campo obrigatório.")
        if re.match(r'^[a-zA-Z!@#$%^&*()_+{}\[\]:;<>,.?~\\/\\\'"\\-]*$', username):
            raise ValidationError('A matricula deve ser composta apenas por números!')

        if not email:
            raise ValidationError("Campo obrigatório.")
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError('Insira um endereço de email válido.')
        if not password:
            raise ValidationError("Campo obrigatório.")