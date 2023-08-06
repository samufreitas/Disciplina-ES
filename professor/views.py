from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from datetime import datetime
from django.db import transaction
from .forms import AgendamentoMonitorForm
from secretaria.models import Agendamento
from laboratorio.models import Laboratorio




def pag_professor(request):
    return render(request, 'professor/base_professor.html')


def agendar_professor(request):
    template_name = 'professor/agendar_professor.html'
    context = {}

    labs = Laboratorio.objects.all()
    context['labs'] = labs

    eventos_a_agendar = []
    if request.method == 'POST':
        form = AgendamentoMonitorForm(request.POST)
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
                            f.tipo = 'Aula'
                            f.save()
                            messages.success(request, 'Agendamento realizado com sucesso!')
                            return redirect('professor:listar_professor')
                    else:
                        # Se não houver conflitos, salva o novo agendamento
                        eventos_a_agendar = [f]
        else:
            messages.error(request, 'Todos os campos devem ser preenchidos corretamente.')
    else:
        form = AgendamentoMonitorForm()

    context['form'] = form
    if request.method == 'POST':
        with transaction.atomic():
            for evento in eventos_a_agendar:
                evento.user = request.user
                evento.status = 'Agendado'
                evento.tipo = 'Aula'
                evento.save()

        messages.success(request, 'Agendamentos realizados com sucesso!')
        return redirect('professor:listar_professor')

    return render(request, template_name, context)


def listar_professor(request):
    agendamentos = Agendamento.objects.filter(status='Agendado')
    return render(request, 'professor/lista_agendamento_professor.html', {'agendamentos': agendamentos})


def excluir_agendamento(request, agendamento_id):
    try:
        agendamento = Agendamento.objects.get(id=agendamento_id)
        agendamento.delete()
        messages.success(request, "Agendamento excluído!")
    except Agendamento.DoesNotExist:
        messages.error(request, "Agendamento não encontrado.")

    return redirect('professor:listar_professor')





