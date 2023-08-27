from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from datetime import datetime
from django.db import transaction
from .forms import AgendamentoMonitorForm
from secretaria.models import Agendamento, Tipo
from laboratorio.models import Laboratorio
from django.contrib.auth.decorators import login_required, user_passes_test

def is_monitor(user):
    return user.groups.filter(name='Monitor').exists()

"""@login_required(login_url='/contas/login/')
@user_passes_test(is_monitor)"""
def pag_monitor(request):
    return render(request, 'monitor/base_monitor.html')


"""@login_required(login_url='/contas/login/')
@user_passes_test(is_monitor)"""
def agendar_monitor(request):
    template_name = 'monitor/agendar_monitor.html'
    context = {}

    labs = Laboratorio.objects.all()
    context['labs'] = labs

    if request.method == 'POST':
        form = AgendamentoMonitorForm(request.POST)
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
            )

            if coliding_events.exists():
                if f.tipo.titulo == 'Aula':
                    messages.error(request, 'Já existe um agendamento conflitante neste horário!')
                elif f.tipo.titulo == 'Monitoria' and coliding_events.filter(tipo__titulo='Aula').exists():
                    messages.error(request, 'Já existe uma aula cadastrada nesse horário')
                else:
                    # Se for outra monitoria ou não houver conflito, salva o novo agendamento
                    f.user = request.user
                    f.status = 'Solicitado'
                    f.tipo = get_object_or_404(Tipo, titulo='Monitoria')
                    f.save()
                    messages.success(request, 'Solicitação de agendamento realizado com sucesso!')

            else:
                f.user = request.user
                f.status = 'Solicitado'
                f.tipo = get_object_or_404(Tipo, titulo='Monitoria')
                f.save()
                messages.success(request, 'Solicitação de agendamento realizado com sucesso!')
                return redirect('monitor:lista_monitor')
        else:
            context['form'] = form

    else:
        form = AgendamentoMonitorForm()
        context['form'] = form
    return render(request, template_name, context)


"""@login_required(login_url='/contas/login/')
@user_passes_test(is_monitor)"""
def listar_monitor(request):
    agendamentos = Agendamento.objects.all()   #filter(user=request.user)
    return render(request, 'monitor/lista_agendamento_monitor.html', {'agendamentos': agendamentos})

"""@login_required(login_url='/contas/login/')
@user_passes_test(is_monitor)"""
def excluir_agendamento(request, agendamento_id):
    try:
        agendamento = Agendamento.objects.get(id=agendamento_id)
        agendamento.delete()
        messages.success(request, "Agendamento excluído!")
    except Agendamento.DoesNotExist:
        messages.error(request, "Agendamento não encontrado.")

    return redirect('monitor:lista_monitor')





