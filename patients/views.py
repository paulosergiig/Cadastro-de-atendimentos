from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from .models import Patient, FichaEvolucao
from .forms import PatientForm, FichaEvolucaoForm, ExportForm
from accounts.models import Terapeuta
from django.db.models import Q
from accounts.models import Grupo


class PatientListView(LoginRequiredMixin, ListView):
    model = Patient
    template_name = 'patients/patient_list.html'
    context_object_name = 'pacientes'
    paginate_by = 20 # Opcional: para paginar se a lista for muito grande

    def get_queryset(self):
        queryset = super().get_queryset().order_by('nome_paciente')
        
        # Pega os parâmetros da URL
        search_query = self.request.GET.get('q', '')
        group_id = self.request.GET.get('grupo', '')

        # Filtra pela busca, se houver
        if search_query:
            queryset = queryset.filter(
                Q(nome_paciente__icontains=search_query) |
                Q(nome_responsavel__icontains=search_query)
            )

        # Filtra pelo grupo, se houver
        if group_id:
            queryset = queryset.filter(grupo_id=group_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Envia a lista de todos os grupos e os filtros ativos para o template
        context['grupos'] = Grupo.objects.all()
        context['active_filter_q'] = self.request.GET.get('q', '')
        context['active_filter_grupo'] = self.request.GET.get('grupo', '')
        return context

class PatientCreateView(LoginRequiredMixin, CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'patients/patient_form.html'
    success_url = reverse_lazy('patients:patient_list')

class PatientUpdateView(LoginRequiredMixin, UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = 'patients/patient_form.html'
    
    def get_success_url(self):
        return reverse('patients:patient_detail', kwargs={'pk': self.object.pk})

class PatientDetailView(LoginRequiredMixin, DetailView):
    model = Patient
    template_name = 'patients/patient_detail.html'
    context_object_name = 'paciente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['evolution_form'] = FichaEvolucaoForm()
        context['fichas_evolucao'] = self.object.fichas_evolucao.all()
        return context

class FichaEvolucaoCreateView(LoginRequiredMixin, CreateView):
    model = FichaEvolucao
    form_class = FichaEvolucaoForm
    template_name = 'patients/evolution_form.html'

    def form_valid(self, form):
        form.instance.paciente = get_object_or_404(Patient, pk=self.kwargs['patient_pk'])
        form.instance.terapeuta_autor = get_object_or_404(Terapeuta, user=self.request.user)
        messages.success(self.request, "Ficha de evolução adicionada com sucesso.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('patients:patient_detail', kwargs={'pk': self.kwargs['patient_pk']})



# ---- Exportação para Excel ----
from django.contrib.auth.decorators import login_required

@login_required
def export_view(request):
    if request.method == 'POST':
        form = ExportForm(request.POST)
        if form.is_valid():
            data_inicio = form.cleaned_data['data_inicio']
            data_fim = form.cleaned_data['data_fim']
            pacientes = form.cleaned_data['pacientes']
            
            fichas = FichaEvolucao.objects.filter(data__date__range=[data_inicio, data_fim]).select_related('paciente', 'terapeuta_autor')
            if pacientes:
                fichas = fichas.filter(paciente__in=pacientes)
            
            # Gerar o arquivo Excel
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename="relatorio_evolucao_{data_inicio}_a_{data_fim}.xlsx"'

            wb = Workbook()
            ws = wb.active
            ws.title = "Relatório de Evolução"

            # Cabeçalho
            columns = ['Data', 'Paciente', 'Terapeuta Autor', 'Emoji', 'Comentários']
            ws.append(columns)
            for col_num, column_title in enumerate(columns, 1):
                cell = ws.cell(row=1, column=col_num)
                cell.font = Font(bold=True)
                cell.alignment = Alignment(horizontal='center', vertical='center')

            # Dados
            for ficha in fichas:
                ws.append([
                    ficha.data.strftime('%d/%m/%Y %H:%M'),
                    ficha.paciente.nome_paciente,
                    ficha.terapeuta_autor.nome_completo,
                    ficha.emoji_evolucao,
                    ficha.comentarios
                ])
            
            wb.save(response)
            return response
    else:
        form = ExportForm()
        
    return render(request, 'patients/export_form.html', {'form': form})