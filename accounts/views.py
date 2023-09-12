from django import forms
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User, Group
from .forms import UserForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q

# Função para verificar se o usuário pertence ao grupo "Secretaria"
def is_secretaria(user):
    return user.groups.filter(name='Secretaria').exists()



"""@login_required(login_url='/contas/login/')
@user_passes_test(is_secretaria)"""
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

"""@login_required(login_url='/contas/login/')
@user_passes_test(is_secretaria)"""
def list_user(request):
    template_name = 'user_list.html'
    consulta = User.objects.filter(is_superuser=False)
    query = request.POST.get('query')
    groups = request.POST.get('groups')
    if query:
        consulta = consulta.filter(
            Q(last_name__icontains=query) |
            Q(first_name__icontains=query) |
            Q(username__icontains=query))
    if groups:
        consulta = consulta.filter(groups__name__icontains=groups)
    paginator = Paginator(consulta, 10)
    page_number = request.GET.get("page")
    users = paginator.get_page(page_number)
    context = {
        'users': users
    }
    return render(request, template_name, context)


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

@login_required(login_url='/contas/login/')
@user_passes_test(is_secretaria)
def user_delete(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        messages.success(request, "Usuário excluído com sucesso!")
    except User.DoesNotExist:
        messages.error(request, "Usuário não encontrado!")

    return redirect('accounts:user_list')

@login_required(login_url='/contas/login/')
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
            elif form.user.groups.filter(name='Monitor').exists():
                return redirect('monitor:pag_monitor')
            elif form.user.groups.filter(name='Professor').exists():
                return redirect('professor:pag_professor')
            else:
                return redirect('accounts:user_login')
        else:
            messages.error(request, "Não foi possível trocar sua senha!")
    form = PasswordChangeForm(user=request.user)
    context['form'] = form
    return render(request, template_name, context)



def user_login(request):
    template_name = 'user_login.html'
    try:
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
                elif user.groups.filter(name='Monitor').exists():
                    return redirect('monitor:pag_monitor')
                elif user.groups.filter(name='Professor').exists():
                    return redirect('professor:pag_professor')
                else:
                    messages.error(request, "Você não tem acesso a essa parte do sistema!")
            else:
                messages.error(request, "Usuário ou senha inválidos.")
        return render(request, template_name, {})
    except:
        messages.error(request, 'Matrícula ou senha incorretas!')
        return redirect('accounts:user_login')
def voltar(request):
    user = request.user

    if user.groups.filter(name='Secretaria').exists():
        return redirect('secretaria:pag_secretaria')
    elif user.groups.filter(name='Professor').exists():
        return redirect('professor:pag_professor')
    elif user.groups.filter(name='Monitor').exists():
        return redirect('monitor:pag_monitor')
    else:
        return redirect('accounts:user_login')

@login_required(login_url='/contas/login/')
def user_logout(request):
    logout(request)
    return redirect('accounts:user_login')