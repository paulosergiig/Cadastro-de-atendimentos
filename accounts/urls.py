from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    # URLs para Terapeutas (Supervisor)
    path('terapeutas/', views.TerapeutaListView.as_view(), name='therapist_list'),
    
    # --- LINHAS CORRIGIDAS ---
    path('terapeutas/novo/', views.therapist_create, name='therapist_create'),
    path('terapeutas/<int:pk>/editar/', views.therapist_update, name='therapist_update'),
    # -------------------------

    path('terapeutas/<int:pk>/resetar-senha/', views.reset_password, name='therapist_reset_password'),
    path('terapeutas/<int:pk>/remover/', views.TerapeutaDeleteView.as_view(), name='therapist_delete'),

    # URL para o próprio usuário alterar a senha
    path('mudar-senha/', views.CustomPasswordChangeView.as_view(
        template_name='accounts/password_change_form.html',
        success_url=reverse_lazy('accounts:password_change_done')
    ), name='password_change'),
    
    path('mudar-senha/concluido/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html'
    ), name='password_change_done'),
]