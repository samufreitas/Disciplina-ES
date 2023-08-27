from django.shortcuts import render, redirect,get_object_or_404
from django.db.models import Q
from django.contrib import messages
from .forms import AgendamentoProfessorForm
from secretaria.models import Agendamento, Tipo
from laboratorio.models import Laboratorio
from django.core.paginator import Paginator



def pag_professor(request):
    return render(request, 'professor/base_professor.html')


def agendar_professor(request):
    template_name = 'professor/agendar_professor.html'
    context = {}

    labs = Laboratorio.objects.all()
    context['labs'] = labs
    if request.method == 'POST':
        form = AgendamentoProfessorForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            coliding_events = Agendamento.objects.filter(
                Q(data=f.data) &
                Q(laboratorio=f.laboratorio) &
                (
                        (Q(hora_inicio__lte=f.hora_inicio) & Q(hora_fim__gte=f.hora_inicio)) |
                        (Q(hora_inicio__lte=f.hora_fim) & Q(hora_fim__gte=f.hora_fim))
                )
            ).exclude(status='Cancelado')

            if coliding_events.exists():
                messages.error(request, 'Já existe um agendamento nesse horário!')
            else:
                f.user = request.user
                f.status = 'Agendado'
                f.titulo = f.titulo.capitalize()
                f.tipo = get_object_or_404(Tipo, titulo='Aula')
                f.save()
                messages.success(request, 'Agendamento realizado com sucesso!')
                return redirect('professor:listar_professor')
    else:
        form = AgendamentoProfessorForm()

    context['form'] = form
    return render(request, template_name, context)


def listar_professor(request):
    template_name = 'professor/lista_agendamento_professor.html'
    consulta = Agendamento.objects.filter(status='Agendado')
    paginator = Paginator(consulta, 10)

    page_number = request.GET.get("page")
    agendamentos = paginator.get_page(page_number)
    context = {
        'agendamentos': agendamentos
    }
    return render(request, template_name, context)


def excluir_agendamento(request, agendamento_id):
    try:
        agendamento = Agendamento.objects.get(id=agendamento_id)
        agendamento.delete()
        messages.success(request, "Agendamento excluído!")
    except Agendamento.DoesNotExist:
        messages.error(request, "Agendamento não encontrado.")

    return redirect('professor:listar_professor')





