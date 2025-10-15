from django import forms
from django.contrib.auth.models import User
from .models import Grupo, Terapeuta

# Dentro de accounts/forms.py

class TerapeutaForm(forms.ModelForm):
    # Campos que não estão no modelo Terapeuta, mas que precisamos no formulário
    username = forms.CharField(max_length=100, label="Nome de Usuário")
    password = forms.CharField(widget=forms.PasswordInput, required=False, help_text="Deixe em branco para não alterar.")

    class Meta:
        model = Terapeuta
        # Inclui os campos do modelo que queremos no formulário
        fields = ['nome_completo', 'especialidade', 'grupo']

    def __init__(self, *args, **kwargs):
        # Pega a instância do terapeuta, se estiver editando
        instance = kwargs.get('instance')
        
        # Se for uma edição, preenchemos os campos de usuário com os dados existentes
        if instance:
            initial = kwargs.get('initial', {})
            initial['username'] = instance.user.username
            kwargs['initial'] = initial
        
        super().__init__(*args, **kwargs)

        # --- CÓDIGO NOVO PARA CORRIGIR O AUTOFILL ---
        # Adiciona atributos ao widget para instruir o navegador a não preencher
        # automaticamente os campos de um novo usuário.
        if not instance:
            self.fields['username'].widget.attrs.update(
                {'autocomplete': 'off'}
            )
            self.fields['password'].widget.attrs.update(
                {'autocomplete': 'new-password'} # 'new-password' é o padrão moderno para isso
            )
        # ----------------------------------------------
        
        # Se for um formulário de criação (sem instância), a senha é obrigatória
        if not instance:
            self.fields['password'].required = True
            self.fields['password'].help_text = "Senha temporária para o primeiro acesso."