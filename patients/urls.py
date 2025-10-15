from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    path('', views.PatientListView.as_view(), name='patient_list'),
    path('novo/', views.PatientCreateView.as_view(), name='patient_create'),
    path('<int:pk>/', views.PatientDetailView.as_view(), name='patient_detail'),
    path('<int:pk>/editar/', views.PatientUpdateView.as_view(), name='patient_update'),
    
    # Fichas de Evolução
    path('<int:patient_pk>/evolucao/adicionar/', views.FichaEvolucaoCreateView.as_view(), name='evolution_create'),
    

    # Relatórios
    path('exportar/', views.export_view, name='export_form'),
]