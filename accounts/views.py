from django import forms
from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.context_processors import request
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.models import User, Group
from .forms import UserForm

def add_user(request):
    template_name = 'user_create.html'
    context = {}

    groups = Group.objects.all()
    context['groups'] = groups

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']

            # Verificar se já existe um usuário com o mesmo username e email
            if User.objects.filter(username=username, email=email).exists():
                # Se existir, mostrar uma mensagem de erro e não salvar o usuário
                messages.error(request, 'Já existe um usuário com esse username e email!')
            else:
                # Se não existir, salvar o usuário normalmente
                user = form.save(commit=False)
                password = form.cleaned_data['password']
                user.set_password(password)
                user.save()
                form.save_m2m()  # Salvar associação de grupos do formulário
                messages.success(request, 'Usuário salvo com sucesso!')
                return redirect('accounts:user_list')
    else:
        form = UserForm()

    context['form'] = form
    return render(request, template_name, context)
def list_user(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class UserUpdateView(UpdateView):
    model = User
    form_class = UserEditForm
    template_name = 'user_edit.html'
    success_url = reverse_lazy('accounts:user_list')

    def get_form_kwargs(self):
        insere = super().get_form_kwargs()
        insere['instance'] = self.get_object()
        return insere
class UserDeleteView(DeleteView):
    model = User
    template_name = 'user_confirm_delete.html'
    success_url = reverse_lazy('accounts:user_list')