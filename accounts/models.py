from django.db import models
from django.contrib.auth.models import User
import random # Adicione esta importação no topo do arquivo

class Grupo(models.Model):
    nome = models.CharField(max_length=50, unique=True, help_text="Ex: Grupo A, Infantil, Adulto")

    def __str__(self):
        return self.nome

class Terapeuta(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='therapist_profile')
    nome_completo = models.CharField(max_length=255)
    especialidade = models.CharField(max_length=100, blank=True)
    cor_hex = models.CharField(max_length=7, default='#343a40')
    grupo = models.ForeignKey(Grupo, on_delete=models.SET_NULL, null=True, blank=True)
    must_change_password = models.BooleanField(default=True)

    def __str__(self):
        return self.nome_completo

    def save(self, *args, **kwargs):
        # Gera uma cor aleatória apenas na primeira vez que o objeto é criado
        if not self.pk:
            self.cor_hex = f'#{random.randint(0, 0xFFFFFF):06x}'
        super().save(*args, **kwargs)