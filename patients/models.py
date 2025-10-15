import os
from django.db import models
from django.contrib.auth.models import User

from datetime import date
from django.utils import timezone
from accounts.models import Terapeuta, Grupo

class Patient(models.Model):
    nome_paciente = models.CharField(max_length=255)
    nome_responsavel = models.CharField(max_length=255, blank=True)
    data_nascimento = models.DateField()
    laudo_medico = models.TextField(blank=True, verbose_name="Laudo Médico")
    grupo = models.ForeignKey(Grupo, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Grupo")
    
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    @property
    def idade(self):
        today = date.today()
        return today.year - self.data_nascimento.year - ((today.month, today.day) < (self.data_nascimento.month, self.data_nascimento.day))

    def __str__(self):
        return self.nome_paciente

class FichaEvolucao(models.Model):
    class EmojiChoices(models.TextChoices):
        EXCELENTE = '🟢😀', '🟢😀 Excelente'
        BOM = '🟡🙂', '🟡🙂 Bom'
        NEUTRO = '⚪😐', '⚪😐 Neutro'
        RUIM = '🔴😟', '🔴😟 Ruim'
        PESSIMO = '🚨😢', '🚨😢 Péssimo'

    paciente = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='fichas_evolucao')
    terapeuta_autor = models.ForeignKey(Terapeuta, on_delete=models.PROTECT, related_name='fichas_criadas')
    data = models.DateTimeField(default=timezone.now)
    emoji_evolucao = models.CharField(max_length=10, choices=EmojiChoices.choices, default=EmojiChoices.NEUTRO)
    comentarios = models.TextField()
    
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-data']

    def __str__(self):
        return f"Evolução de {self.paciente.nome_paciente} em {self.data.strftime('%d/%m/%Y')}"

# Os modelos de Triagem e Anamnese são deixados simples de propósito, para serem expandidos conforme a necessidade.
class FichaTriagem(models.Model):
    paciente = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='ficha_triagem')
    terapeuta_autor = models.ForeignKey(Terapeuta, on_delete=models.SET_NULL, null=True)
    historico_paciente = models.TextField(blank=True)
    observacoes_iniciais = models.TextField(blank=True)
    anexo = models.FileField(upload_to='triagens/', blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

class Anamnese(models.Model):
    paciente = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='anamnese')
    terapeuta_autor = models.ForeignKey(Terapeuta, on_delete=models.SET_NULL, null=True)
    queixa_principal = models.TextField(blank=True)
    historico_doenca_atual = models.TextField(blank=True)
    outras_observacoes = models.TextField(blank=True)
    anexo = models.FileField(upload_to='anamneses/', blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

# O modelo Anotação foi omitido para simplicidade, pois sua funcionalidade pode ser coberta pela FichaEvolucao e AuditLog.
# Caso necessário, seria um modelo simples com FK para Terapeuta e um TextField.