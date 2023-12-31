from django.shortcuts import render, redirect,get_object_or_404
from django.db.models import Q
from django.contrib import messages
from .forms import AgendamentoProfessorForm
from secretaria.models import Agendamento, Tipo
from laboratorio.models import Laboratorio
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from datetime import date, timedelta
def is_professor(user):
    return user.groups.filter(name='Professor').exists()

@login_required(login_url='/contas/login/')
@user_passes_test(is_professor)
def pag_professor(request):
    return render(request, 'professor/base_professor.html')


@login_required(login_url='/contas/login/')
@user_passes_test(is_professor)
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


@login_required(login_url='/contas/login/')
@user_passes_test(is_professor)
def listar_professor(request):
    template_name = 'professor/lista_agendamento_professor.html'
    query = request.POST.get('query')
    status1 = request.POST.get('status1')
    data = request.POST.get('data')
    data_atual = timezone.now()
    consulta = Agendamento.objects.all()#filter(user=request.user)

    #Parte dos filtros
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
        consulta = consulta.filter(data__range=[data_passado.date(), (data_atual - timedelta(days=0)).date()])
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
    #Parte de paginação
    paginator = Paginator(consulta, 8)
    page_number = request.GET.get("page")
    agendamentos = paginator.get_page(page_number)
    context = {
        'agendamentos': agendamentos
    }
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
@user_passes_test(is_professor)
def excluir_agendamento(request, agendamento_id):
    try:
        agendamento = Agendamento.objects.get(id=agendamento_id)
        agendamento.delete()
        messages.success(request, "Agendamento excluído!")
    except Agendamento.DoesNotExist:
        messages.error(request, "Agendamento não encontrado.")

    return redirect('professor:listar_professor')





