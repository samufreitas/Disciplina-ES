from django import forms
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
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
                messages.success(request, 'Usuário cadastrado com sucesso!')
                return redirect('accounts:user_list')
    else:
        form = UserForm()

    context['form'] = form
    return render(request, template_name, context)
def list_user(request):
    users = User.objects.filter(is_superuser=False)
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

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, 'Usuário excluído com sucesso!')
        return response
def user_new_password(request):
    template_name = 'user_new_password.html'
    context = {}
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Senha alterada com sucesso!")
            update_session_auth_hash(request, form.user)
            if form.user.groups.filter(name='Secretaria').exists():
                return redirect('secretaria:pag_secretaria')
            elif form.user.groups.filter(name='Professor').exists():
                return redirect('accounts:add_user')
            elif form.user.groups.filter(name='Orientador').exists():
                return redirect('aluno:list_plano')
        else:
            messages.error(request, "Não foi possível trocar sua senha!")
    form = PasswordChangeForm(user=request.user)
    context['form'] = form
    return render(request, template_name, context)



def user_login(request):
    template_name = 'user_login.html'

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user.last_login is None:
            if user is not None:
                login(request, user)
                return redirect('accounts:user_new_password')
        if user is not None:
            login(request, user)
            if user.groups.filter(name='Secretaria').exists():
                return redirect('secretaria:pag_secretaria')
            elif user.groups.filter(name='Professor').exists():
                return redirect('accounts:add_user')
            elif user.groups.filter(name='Orientador').exists():
                return redirect('aluno:list_plano')
        else:
            messages.error(request, "Usuário ou senha inválidos.")
    return render(request, template_name, {})