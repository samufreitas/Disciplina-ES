from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseNotAllowed
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import AgendamentoForm
from .models import Agendamento


class AgendamentoCreateView(CreateView):
    model = Agendamento
    form_class = AgendamentoForm
    template_name = 'agenda.html'
    success_url = reverse_lazy('agenda')

    def form_valid(self, form):
        # Verificar se já existe um agendamento para o mesmo laboratório, data e horário
        laboratorio = form.cleaned_data['laboratorio']
        data = form.cleaned_data['data']
        hora_inicio = form.cleaned_data['hora_inicio']
        hora_fim = form.cleaned_data['hora_fim']
        if Agendamento.objects.filter(laboratorio=laboratorio, data=data, hora_inicio=hora_inicio, hora_fim=hora_fim).exists():
            form.add_error(None, 'Este laboratório já está agendado para esse horário.')
            return self.form_invalid(form)
        return super().form_valid(form)

def calendario(request):
    return render(request, 'calendario.html')


def adicionar_evento(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        data = request.POST.get('data')
        hora_inicio = request.POST.get('hora_inicio')
        hora_fim = request.POST.get('hora_fim')

        # Verificar se já existe um agendamento para a mesma data e horário
        agendamento_existente = Agendamento.objects.filter(
            Q(data=data) &
            (
                    (Q(hora_inicio__gte=hora_inicio) & Q(hora_inicio__lt=hora_fim)) |
                    (Q(hora_fim__gt=hora_inicio) & Q(hora_fim__lte=hora_fim)) |
                    (Q(hora_inicio__lte=hora_inicio) & Q(hora_fim__gte=hora_fim))
            )
        )
        if agendamento_existente.exists():
            error_message = "Já existe um agendamento para este horário. Por favor, escolha outro horário."
            return render(request, 'agendamento.html', {'error_message': error_message})

        agendamento = Agendamento(
            titulo=titulo,
            data=data,
            hora_inicio=hora_inicio,
            hora_fim=hora_fim
        )
        agendamento.save()
        messages.success(request, "Agendamento realizado com sucesso!")

        #return redirect('calendarteste:calendario')

    return render(request, 'agendamento.html')

def listar_agendamentos(request):
    agendamentos = Agendamento.objects.all()
    return render(request, 'listagem_agendamentos.html', {'agendamentos': agendamentos})


def excluir_agendamento(request, agendamento_id):
    agendamento = Agendamento.objects.get(id=agendamento_id)
    agendamento.delete()
    messages.success(request, "Agendamento excluído!")
    return redirect('calendar:lista')



def eventos(request):
    eventos = Agendamento.objects.all()
    data = []
    for evento in eventos:
        data.append({
            'id': evento.id,
            'title': evento.titulo,
            'start': evento.data,

        })
    return JsonResponse(data, safe=False)