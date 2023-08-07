from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.mail import send_mail
from django.db.models import Q
from django.contrib import messages
from datetime import datetime
from django.db import transaction
from .forms import AgendamentoForm
from .models import Agendamento
from laboratorio.models import Laboratorio
from django.contrib.auth.models import User
from decouple import config




def pag_secretaria(request):
    return render(request, 'secretaria/base_secretaria.html')


def adicionar_evento(request):
    template_name = 'agenda.html'
    context = {}

    tipos = Agendamento.TIPO_CHOICES
    context = {'tipos': tipos}

    labs = Laboratorio.objects.all()
    context['labs'] = labs

    users = User.objects.all()
    context['users'] = users
    eventos_a_agendar = []
    if request.method == 'POST':
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)

            if f.hora_fim <= f.hora_inicio:
                messages.error(request, 'Hora fim deve ser maior que a hora de inicio!')
            else:
                # Verifica se a data fornecida é menor que a data atual
                data_atual = datetime.now().date()
                if f.data < data_atual:
                    messages.error(request, 'A data deve ser maior ou igual à data atual!')
                else:
                    # Verifica se há agendamentos que colidem com a proposta
                    coliding_events = Agendamento.objects.filter(
                        Q(data=f.data) &
                        Q(laboratorio=f.laboratorio) &
                        (
                                (Q(hora_inicio__lte=f.hora_inicio) & Q(hora_fim__gte=f.hora_inicio)) |
                                (Q(hora_inicio__lte=f.hora_fim) & Q(hora_fim__gte=f.hora_fim))
                        )
                    )

                    if coliding_events.exists():
                        if f.tipo == 'Aula':
                            messages.error(request, 'Já existe um agendamento conflitante neste horário!')
                        elif f.tipo == 'Monitoria' and coliding_events.filter(tipo='Aula').exists():
                            messages.error(request, 'Já existe uma aula cadastrada nesse horário')
                        else:
                            # Se for outra monitoria ou não houver conflito, salva o novo agendamento
                            f.user = request.user
                            f.status = 'Agendado'
                            f.save()
                            messages.success(request, 'Agendamento realizado com sucesso!')
                            return redirect('secretaria:lista')
                    else:
                        # Se não houver conflitos, salva o novo agendamento
                        eventos_a_agendar = [f]
        else:
            messages.error(request, 'Todos os campos devem ser preenchidos corretamente.')
    else:
        form = AgendamentoForm()

    context['form'] = form
    if request.method == 'POST':
        with transaction.atomic():
            for evento in eventos_a_agendar:
                evento.user = request.user
                evento.status = 'Agendado'
                evento.save()

        messages.success(request, 'Agendamentos realizados com sucesso!')
        return redirect('secretaria:lista')

    return render(request, template_name, context)


def listar_agendamentos(request):
    agendamentos = Agendamento.objects.filter(status='Agendado')
    return render(request, 'listagem_agendamentos.html', {'agendamentos': agendamentos})


def listar_solicitacao(request):
    agendamentos = Agendamento.objects.filter(tipo='Monitoria', status='Solicitado')
    return render(request, 'solicitacao.html', {'agendamentos': agendamentos})

def conf_solicitacao(request, agendamento_id):
    agendamento = Agendamento.objects.get(id=agendamento_id)
    agendamento.status = 'Agendado'
    agendamento.save()  # Salva a atualização no banco de dado

    # Formata a data para o formato "D/M/A"
    data = agendamento.data.strftime('%d/%m/%Y')

    # Formata as horas de início e fim para o formato "HH:mm"
    hora_inicio = agendamento.hora_inicio.strftime('%H:%M')
    hora_fim = agendamento.hora_fim.strftime('%H:%M')

    # Envia um e-mail para o usuário que fez a solicitação
    assunto = 'Coordenação Sistemas de Informação: Agendamento Confirmado'
    mensagem = f'Sua solicitação de agendamento para dia {data} ' \
               f'com início às {hora_inicio} e termino as {hora_fim} foi aceita!'
    remetente = config('EMAIL_HOST_USER')
    destinatario = agendamento.user.email  # Supondo que o campo de e-mail do usuário seja "email"
    send_mail(assunto, mensagem, remetente, [destinatario])

    messages.warning(request, "Solicitação confirmada!")
    return redirect('secretaria:listar_solicitacao')

def negar_solicitacao(request, agendamento_id):
    try:
        agendamento = Agendamento.objects.get(id=agendamento_id)
        data = agendamento.data.strftime('%d/%m/%Y')

        # Formata as horas de início e fim para o formato "HH:mm"
        hora_inicio = agendamento.hora_inicio.strftime('%H:%M')
        hora_fim = agendamento.hora_fim.strftime('%H:%M')
        agendamento.delete()
        assunto = 'Coordenação Sistemas de Informação: Agendamento negado'
        mensagem = f'Sua solicitação de agendamento para dia {data} ' \
                   f'com início às {hora_inicio} e termino as {hora_fim} foi negada!'
        remetente = config('EMAIL_HOST_USER')
        destinatario = agendamento.user.email  # Supondo que o campo de e-mail do usuário seja "email"
        send_mail(assunto, mensagem, remetente, [destinatario])
        messages.warning(request, "Solicitação de agendamento negada!")

    except Agendamento.DoesNotExist:
        messages.error(request, "Solicitação não encontrado.")

    return redirect('secretaria:listar_solicitacao')

def excluir_agendamento(request, agendamento_id):
    try:
        agendamento = Agendamento.objects.get(id=agendamento_id)
        agendamento.delete()
        messages.success(request, "Agendamento excluído!")
    except Agendamento.DoesNotExist:
        messages.error(request, "Agendamento não encontrado.")

    return redirect('secretaria:lista')



def eventos(request):
    eventos = Agendamento.objects.all()
    data = []
    for evento in eventos:
        print(evento.id)
        print(evento.titulo)
        data.append({
            'id': evento.id,
            'title': evento.titulo,
        })
    return JsonResponse(data, safe=False)


