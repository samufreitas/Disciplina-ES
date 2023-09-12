from django.shortcuts import render, redirect
from django.http import JsonResponse, Http404
from django.utils import timezone
from django.db.models import Q
from django.db import transaction
from .forms import AgendamentoForm, TipoForm
from .models import Agendamento, Tipo
from laboratorio.models import Laboratorio
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from decouple import config
from datetime import date, timedelta
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404



# Função para verificar se o usuário pertence ao grupo "Secretaria"
def is_secretaria(user):
    return user.groups.filter(name='Secretaria').exists()



"""@login_required(login_url='/contas/login/')
@user_passes_test(is_secretaria)"""
def pag_secretaria(request):
    return render(request, 'secretaria/base_secretaria.html')

"""@login_required(login_url='/contas/login/')
@user_passes_test(is_secretaria)"""
def adicionar_evento(request):
    template_name = 'agenda.html'
    context = {}

    tipos = Tipo.objects.all()
    context = {'tipos': tipos}

    labs = Laboratorio.objects.all()
    context['labs'] = labs

    users = User.objects.all()
    context['users'] = users

    if request.method == 'POST':
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            # Verifica se há agendamentos que colidem com a proposta
            coliding_events = Agendamento.objects.filter(
                Q(data=f.data) &
                Q(laboratorio=f.laboratorio) &
                (
                        (Q(hora_inicio__lte=f.hora_inicio) & Q(hora_fim__gte=f.hora_inicio)) |
                        (Q(hora_inicio__lte=f.hora_fim) & Q(hora_fim__gte=f.hora_fim))
                )
            ).exclude(status='Cancelado')

            if coliding_events.exists():
                if f.tipo.titulo == 'Monitoria' and coliding_events.filter(tipo__titulo='Monitoria').exists():
                    f.status = 'Agendado'
                    f.titulo = f.titulo.capitalize()
                    f.save()
                    messages.success(request, 'Agendamento realizado com sucesso!')
                    return redirect('secretaria:lista')
                else:
                    messages.error(request, 'Existe um agendamento nesse horário')
            else:
                f.status = 'Agendado'
                f.titulo = f.titulo.capitalize()
                f.save()
                messages.success(request, 'Agendamento realizado com sucesso!')
                return redirect('secretaria:lista')
    else:
        form = AgendamentoForm()

    context['form'] = form
    return render(request, template_name, context)



"""@login_required(login_url='/contas/login/')
@user_passes_test(is_secretaria)"""
def listar_agendamentos(request):
    template_name = 'listagem_agendamentos.html'
    query = request.POST.get('query')
    status1 = request.POST.get('status1')
    data = request.POST.get('data')
    data_atual = timezone.now()
    consulta = Agendamento.objects.exclude(status='Solicitado')

    # Parte para retorna o filtro por datas
    if data == 'hoje':
        consulta = consulta.filter(data=data_atual.date())
    elif data == 'proxima_semana':
        data_futuro = data_atual + timedelta(days=7)
        consulta = consulta.filter(data__range=[data_atual.date(), data_futuro.date()])
    elif data == 'proxima_mes':
        data_futuro = data_atual + timedelta(days=30)
        consulta = consulta.filter(data__range=[(data_atual + timedelta(days=1)).date(), data_futuro.date()])
    elif data == 'semana_anterior':
        data_passado = data_atual - timedelta(days=7)
        consulta = consulta.filter(data__range=[data_passado.date(), (data_atual - timedelta(days=1)).date()])
    elif data == 'mes_anterior':
        data_passado = data_atual - timedelta(days=30)
        consulta = consulta.filter(data__range=[data_passado.date(), (data_atual - timedelta(days=1)).date()])
    elif data == 'todas':
        pass

    if query:
        consulta = consulta.filter(
            Q(titulo__icontains=query) |
            Q(tipo__titulo__icontains=query) |
            Q(laboratorio__name__icontains=query))

    if status1:
        consulta = consulta.filter(status=status1)
    paginator = Paginator(consulta, 8)
    page_number = request.GET.get("page")
    agendamentos = paginator.get_page(page_number)

    context = {
        'agendamentos': agendamentos,
        'query': query,
        'status1': status1,
        'data': data,
    }
    return render(request, template_name, context)

"""@login_required(login_url='/contas/login/')
@user_passes_test(is_secretaria)"""
def cancelar_agendamento(request, agendamento_id):
    try:
        agendamento = Agendamento.objects.get(id=agendamento_id)
        if agendamento.status != 'Cancelado':
            agendamento.status = 'Cancelado'
            agendamento.save()
            messages.warning(request, "Agendamento cancelado!")
        else:
            messages.error(request, 'Esse agendamento já está cancelado!')
    except Agendamento.DoesNotExist:
        messages.error(request, "Solicitação não encontrado.")

    return redirect('secretaria:lista')


"""@login_required(login_url='/contas/login/')
@user_passes_test(is_secretaria)"""
def listar_solicitacao(request):
    template_name = 'solicitacao.html'
    query = request.POST.get('query')
    status1 = request.POST.get('status1')
    data = request.POST.get('data')
    data_atual = timezone.now()
    consulta = Agendamento.objects.filter(tipo__titulo='Monitoria')

    if data == 'hoje':
        consulta = consulta.filter(data=data_atual.date())
    elif data == 'proxima_semana':
        data_futuro = data_atual + timedelta(days=7)
        consulta = consulta.filter(data__range=[data_atual.date(), data_futuro.date()])
    elif data == 'proxima_mes':
        data_futuro = data_atual + timedelta(days=30)
        consulta = consulta.filter(data__range=[(data_atual + timedelta(days=1)).date(), data_futuro.date()])
    elif data == 'semana_anterior':
        data_passado = data_atual - timedelta(days=7)
        consulta = consulta.filter(data__range=[data_passado.date(), (data_atual - timedelta(days=1)).date()])
    elif data == 'mes_anterior':
        data_passado = data_atual - timedelta(days=30)
        consulta = consulta.filter(data__range=[data_passado.date(), (data_atual - timedelta(days=1)).date()])
    elif data == 'todas':
        pass

    if query:
        consulta = consulta.filter(
            Q(titulo__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(laboratorio__name__icontains=query))
    if status1:
        consulta = consulta.filter(status=status1)

    paginator = Paginator(consulta, 10)
    page_number = request.GET.get("page")
    agendamentos = paginator.get_page(page_number)
    context = {
        'agendamentos': agendamentos
    }
    return render(request, template_name, context)

"""@login_required(login_url='/contas/login/')
@user_passes_test(is_secretaria)"""
def conf_solicitacao(request, agendamento_id):
    agendamento = Agendamento.objects.get(id=agendamento_id)
    if agendamento.status != 'Agendado':
        agendamento.status = 'Agendado'
        agendamento.save()  # Salva a atualização no banco de dado

        # Formata a data para o formato "D/M/A"
        data = agendamento.data.strftime('%d/%m/%Y')

        # Formata as horas de início e fim para o formato "HH:mm"
        hora_inicio = agendamento.hora_inicio.strftime('%H:%M')
        hora_fim = agendamento.hora_fim.strftime('%H:%M')

        if agendamento.user and agendamento.user.email:
            assunto = 'Coordenação Sistemas de Informação: Agendamento Confirmado'
            mensagem = f'Sua solicitação de agendamento para dia {data} ' \
                       f'com início às {hora_inicio} e termino as {hora_fim} foi aceita!'
            remetente = config('EMAIL_HOST_USER')
            destinatario = agendamento.user.email  # Supondo que o campo de e-mail do usuário seja "email"
            send_mail(assunto, mensagem, remetente, [destinatario])

            messages.success(request, "Solicitação confirmada!")
        else:
            messages.success(request, "Solicitação confirmada!")
    else:
        messages.error(request, 'Essa solicitação já foi agendada!')
    return redirect('secretaria:listar_solicitacao')


"""@login_required(login_url='/contas/login/')
@user_passes_test(is_secretaria)"""
def negar_solicitacao(request, agendamento_id):
    try:
        agendamento = Agendamento.objects.get(id=agendamento_id)
        data = agendamento.data.strftime('%d/%m/%Y')
        hora_inicio = agendamento.hora_inicio.strftime('%H:%M')
        hora_fim = agendamento.hora_fim.strftime('%H:%M')
        if agendamento.status != 'Negado':
            agendamento.status = 'Negado'
            agendamento.save()

            if agendamento.user and agendamento.user.email:  # Verifica se o usuário tem um e-mail
                assunto = 'Coordenação Sistemas de Informação: Agendamento negado'
                mensagem = f'Sua solicitação de agendamento para o dia {data} ' \
                           f'com início às {hora_inicio} e término às {hora_fim} foi negada!'
                remetente = config('EMAIL_HOST_USER')
                destinatario = agendamento.user.email
                send_mail(assunto, mensagem, remetente, [destinatario])
                messages.warning(request, "Solicitação de agendamento negada e e-mail enviado!")
            else:
                messages.warning(request, "Solicitação de agendamento negada! Não foi enviado um E-mail pois nessa solicitação o usuário não possuí E-mail!")
        else:
            messages.error(request, 'Essa solicitação já foi negada!')
    except Agendamento.DoesNotExist:
        messages.error(request, "Solicitação não encontrada.")

    return redirect('secretaria:listar_solicitacao')

"""@login_required(login_url='/contas/login/')
@user_passes_test(is_secretaria)"""
def excluir_agendamento(request, agendamento_id):
    try:
        agendamento = Agendamento.objects.get(id=agendamento_id)
        agendamento.delete()
        messages.success(request, "Agendamento excluído!")
    except Agendamento.DoesNotExist:
        messages.error(request, "Agendamento não encontrado.")

    return redirect('secretaria:lista')



"""@login_required(login_url='/contas/login/')
@user_passes_test(is_secretaria)"""
def add_tipo(request):
    template_name = 'tipo_form.html'
    context = {}

    if request.method == 'POST':
        form = TipoForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                f = form.save(commit=False)
                f.titulo = f.titulo.capitalize()
                f.save()
            messages.success(request, 'Tipo salvo com sucesso!')
            return redirect('secretaria:list_tipo')
        else:
            # Caso o formulário não seja válido, ele é renderizado novamente com as mensagens de erro
            context['form'] = form
    else:
        form = TipoForm()

    context['form'] = form
    return render(request, template_name, context)


"""@login_required(login_url='/contas/login/')
@user_passes_test(is_secretaria)"""
def list_tipo(request):
    template_name = 'list_tipo_form.html'
    query = request.POST.get('query')
    consulta = Tipo.objects.all()
    if query:
        consulta = consulta.filter(
            Q(titulo__icontains=query))
    paginator = Paginator(consulta, 10)
    page_number = request.GET.get("page")
    tipos = paginator.get_page(page_number)
    context = {
        'tipos': tipos
    }
    return render(request, template_name, context)

"""@login_required(login_url='/contas/login/')
@user_passes_test(is_secretaria)"""
def excluir_tipo(request, tipo_id):
    try:
        tipo = Tipo.objects.get(id=tipo_id)
        if Agendamento.objects.filter(tipo=tipo).exists():
            messages.error(request, "Este tipo está relacionado a agendamentos e não pode ser excluído.")
        else:
            tipo.delete()
            messages.success(request, "Tipo excluído!")
    except Tipo.DoesNotExist:
        messages.error(request, "Tipo não encontrado.")

    return redirect('secretaria:list_tipo')


def eventos(request):
    eventos = Agendamento.objects.all()
    data = []
    for evento in eventos:
        data.append({
            'id': evento.id,
            'title': evento.titulo,
        })
    return JsonResponse(data, safe=False)


