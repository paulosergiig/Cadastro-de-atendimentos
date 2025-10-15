from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView # <-- Importação necessária

from .models import Terapeuta, Grupo
from .forms import TerapeutaForm

# Função para verificar se o usuário é um supervisor (staff)
def is_supervisor(user):
    return user.is_authenticated and user.is_staff

# --- CLASSE QUE ESTAVA FALTANDO ---
class CustomPasswordChangeView(PasswordChangeView):
    def form_valid(self, form):
        response = super().form_valid(form)
        profile = self.request.user.therapist_profile
        if profile.must_change_password:
            profile.must_change_password = False
            profile.save()
        messages.success(self.request, "Sua senha foi alterada com sucesso!")
        return response
# ------------------------------------

class SupervisorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return is_supervisor(self.request.user)

class TerapeutaListView(SupervisorRequiredMixin, ListView):
    model = Terapeuta
    template_name = 'accounts/therapist_list.html'
    context_object_name = 'terapeutas'

    def get_queryset(self):
        # Retorna todos os terapeutas, exceto aqueles cujo usuário é um superusuário
        return Terapeuta.objects.filter(user__is_superuser=False)


@user_passes_test(is_supervisor)
def therapist_create(request):
    if request.method == 'POST':
        form = TerapeutaForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            
            # Cria o User primeiro
            user = User.objects.create_user(
                username=data['username'],
                password=data['password']
            )
            
            # Cria o Terapeuta e associa ao User
            Terapeuta.objects.create(
                user=user,
                nome_completo=data['nome_completo'],
                especialidade=data['especialidade'],
                grupo=data['grupo'],
                must_change_password=True
            )
            
            messages.success(request, "Terapeuta cadastrado com sucesso.")
            return redirect('accounts:therapist_list')
    else:
        # Formulário em branco para um novo terapeuta
        form = TerapeutaForm()
        
    return render(request, 'accounts/therapist_form.html', {'form': form, 'is_new': True})

@user_passes_test(is_supervisor)
def therapist_update(request, pk):
    terapeuta = get_object_or_404(Terapeuta, pk=pk)
    if request.method == 'POST':
        form = TerapeutaForm(request.POST, instance=terapeuta)
        if form.is_valid():
            # Salva os dados do modelo Terapeuta
            form.save() 
            
            data = form.cleaned_data
            # Atualiza os dados do User separadamente
            user = terapeuta.user
            user.username = data['username']
            if data.get('password'): # Só atualiza a senha se uma nova foi digitada
                user.set_password(data['password'])
                terapeuta.must_change_password = True # Força a troca de senha se ela foi resetada
                terapeuta.save()
            user.save()
            
            messages.success(request, "Dados do terapeuta atualizados com sucesso.")
            return redirect('accounts:therapist_list')
    else:
        # Formulário preenchido com os dados existentes do terapeuta
        form = TerapeutaForm(instance=terapeuta)

    return render(request, 'accounts/therapist_form.html', {'form': form, 'is_new': False})

@user_passes_test(is_supervisor)
def reset_password(request, pk):
    terapeuta = get_object_or_404(Terapeuta, pk=pk)
    if request.method == 'POST':
        new_password = User.objects.make_random_password(length=8)
        terapeuta.user.set_password(new_password)
        terapeuta.must_change_password = True
        terapeuta.user.save()
        terapeuta.save()
        messages.warning(request, f'A senha de {terapeuta.nome_completo} foi resetada para: {new_password}. O usuário deverá alterá-la no próximo login.')
        return redirect('accounts:therapist_list')
    
    return render(request, 'accounts/therapist_list.html')

class TerapeutaDeleteView(SupervisorRequiredMixin, DeleteView):
    model = Terapeuta
    template_name = 'accounts/therapist_confirm_delete.html'
    success_url = reverse_lazy('accounts:therapist_list')

    def form_valid(self, form):
        messages.success(self.request, f"Terapeuta {self.object.nome_completo} removido com sucesso.")
        return super().form_valid(form)