from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from .forms import AgendamentoMonitorForm
from secretaria.models import Agendamento, Tipo
from laboratorio.models import Laboratorio
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator

def is_monitor(user):
    return user.groups.filter(name='Monitor').exists()

@login_required(login_url='/contas/login/')
@user_passes_test(is_monitor)
def pag_monitor(request):
    return render(request, 'monitor/base_monitor.html')


@login_required(login_url='/contas/login/')
@user_passes_test(is_monitor)
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
            ).exclude(status='Cancelado')

            if coliding_events.exists():
                if coliding_events.filter(tipo__titulo='Monitoria').exists():
                    f.user = request.user
                    f.status = 'Solicitado'
                    f.titulo = f.titulo.capitalize()
                    f.tipo = get_object_or_404(Tipo, titulo='Monitoria')
                    f.save()
                    messages.success(request, 'Solicitação de agendamento realizado com sucesso!')
                    return redirect('monitor:lista_monitor')
                else:
                    messages.error(request, 'Já existe uma agendamento nesse horário!')
            else:
                f.user = request.user
                f.status = 'Solicitado'
                f.titulo = f.titulo.capitalize()
                f.tipo = get_object_or_404(Tipo, titulo='Monitoria')
                f.save()
                messages.success(request, 'Solicitação de agendamento realizado com sucesso!')
                return redirect('monitor:lista_monitor')
    else:
        form = AgendamentoMonitorForm()
    context['form'] = form
    return render(request, template_name, context)

@login_required(login_url='/contas/login/')
@user_passes_test(is_monitor)
def listar_monitor(request):
    template_name = 'monitor/lista_agendamento_monitor.html'
    consulta = Agendamento.objects.filter(user=request.user)
    paginator = Paginator(consulta, 8)

    page_number = request.GET.get("page")
    agendamentos = paginator.get_page(page_number)
    context = {
        'agendamentos': agendamentos
    }
    return render(request, template_name, context)

@login_required(login_url='/contas/login/')
@user_passes_test(is_monitor)
def excluir_agendamento(request, agendamento_id):
    try:
        agendamento = Agendamento.objects.get(id=agendamento_id)
        if agendamento.status != 'Agendado':
            agendamento.delete()
            messages.success(request, "Agendamento excluído!")
        else:
            messages.error(request, 'Essa solicitação estar agendada por esse motivo não pode ser excluída!')
    except Agendamento.DoesNotExist:
        messages.error(request, "Agendamento não encontrado.")

    return redirect('monitor:lista_monitor')





