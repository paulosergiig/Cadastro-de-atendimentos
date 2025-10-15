from django import forms
from .models import Patient, FichaEvolucao

class PatientForm(forms.ModelForm):
    data_nascimento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Data de Nascimento"
    )
    class Meta:
        model = Patient
        fields = ['nome_paciente', 'nome_responsavel', 'data_nascimento', 'laudo_medico', 'grupo']
        labels = {
            'nome_paciente': 'Nome do Paciente',
            'nome_responsavel': 'Nome do Responsável',
            'laudo_medico': 'Laudo Médico (Texto)',
            'grupo': 'Grupo',
        }

class FichaEvolucaoForm(forms.ModelForm):
    data = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="Data e Hora da Evolução"
    )
    class Meta:
        model = FichaEvolucao
        fields = ['data', 'emoji_evolucao', 'comentarios']
        labels = {
            'emoji_evolucao': 'Status da Evolução',
            'comentarios': 'Comentários e Observações',
        }

class ExportForm(forms.Form):
    data_inicio = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}), 
        required=True, 
        label="Data de Início"
    )
    data_fim = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}), 
        required=True, 
        label="Data Final"
    )
    pacientes = forms.ModelMultipleChoiceField(
        queryset=Patient.objects.all(), 
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Filtrar por Pacientes (opcional)"
    )