from django.contrib import messages
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Laboratorio
from .forms import LaboratorioForm

def list_lab(request):
    labs = Laboratorio.objects.all()
    return render(request, 'laboratorio_list.html', {'labs': labs})

class LaboratorioCreateView(CreateView):
    model = Laboratorio
    template_name = 'laboratorio_create.html'  # Nome do template a ser usado para exibir o formulário
    form_class = LaboratorioForm
    success_url = reverse_lazy('laboratorio:laboratorio_list')  # URL de redirecionamento após a criação bem-sucedida

    def form_valid(self, form):
        if Laboratorio.objects.filter(name=form.cleaned_data['name']).exists():
            messages.error(self.request, "Já exixte um laboratório com esse nome!")
            return self.form_invalid(form)
        messages.success(self.request, "Laboratório cadastrado com sucesso!")
        return super().form_valid(form)

class LaboratorioUpdateView(UpdateView):
    model = Laboratorio
    template_name = 'laboratorio_update.html'
    fields = ['qt_monitor', 'qt_notebook', 'qt_teclado', 'qt_mouse']
    success_url = reverse_lazy('laboratorio:laboratorio_list')

    def form_valid(self, form):
        messages.success(self.request, "Atualização realizada com sucesso!")
        return super().form_valid(form)


    def get_form_kwargs(self):
        insere = super().get_form_kwargs()
        insere['instance'] = self.get_object()
        return insere


class LaboratorioDeleteView(DeleteView):
    model = Laboratorio
    success_url = reverse_lazy('laboratorio:laboratorio_list')
