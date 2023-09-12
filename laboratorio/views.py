from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from secretaria.models import Agendamento
from .models import Laboratorio
from .forms import LaboratorioForm
from django.core.paginator import Paginator
from django.db.models import Q

def list_lab(request):
    template_name = 'laboratorio_list.html'
    query = request.POST.get('query')
    consulta = Laboratorio.objects.all()
    if query:
        consulta = consulta.filter(
            Q(name__icontains=query))
    paginator = Paginator(consulta, 8)

    page_number = request.GET.get("page")
    labs = paginator.get_page(page_number)
    context = {
        'labs': labs
    }
    return render(request, template_name, context)

class LaboratorioCreateView(CreateView):
    model = Laboratorio
    template_name = 'laboratorio_create.html'  # Nome do template a ser usado para exibir o formulário
    form_class = LaboratorioForm
    success_url = reverse_lazy('laboratorio:laboratorio_list')  # URL de redirecionamento após a criação bem-sucedida

    def form_valid(self, form):
        if Laboratorio.objects.filter(name=form.cleaned_data['name']).exists():
            messages.error(self.request, "Já existe um laboratório com esse nome!")
            return self.form_invalid(form)
        messages.success(self.request, "Laboratório cadastrado com sucesso!")
        return super().form_valid(form)

class LaboratorioUpdateView(UpdateView):
    model = Laboratorio
    template_name = 'laboratorio_update.html'
    fields = ['name', 'qt_maquinas',]
    success_url = reverse_lazy('laboratorio:laboratorio_list')

    def form_valid(self, form):
        if Laboratorio.objects.filter(name=form.cleaned_data['name']).exists():
            messages.error(self.request, "Já existe um laboratório com esse nome!")
            return self.form_invalid(form)
        messages.success(self.request, "Atualização realizada com sucesso!")
        return super().form_valid(form)


    def get_form_kwargs(self):
        insere = super().get_form_kwargs()
        insere['instance'] = self.get_object()
        return insere


def excluir_lab(request, lab_id):
    try:
        lab = Laboratorio.objects.get(id=lab_id)
        if Agendamento.objects.filter(laboratorio=lab).exists():
            messages.error(request, "Este laboratório está relacionado a agendamentos e não pode ser excluído.")
        else:
            lab.delete()
            messages.success(request, "Laboratório excluído com sucesso!")
    except Laboratorio.DoesNotExist:
        messages.error(request, "Laboratório não encontrado.")

    return redirect('laboratorio:laboratorio_list')
