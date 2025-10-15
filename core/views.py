from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from patients.models import Patient, FichaEvolucao

@login_required
def home(request):
    today = timezone.now().date()
    
    # Contagem de fichas de evolução criadas hoje
    fichas_hoje_count = FichaEvolucao.objects.filter(data__date=today).count()
    
    # Contagem de pacientes ativos (pode ser ajustado para um status específico se houver)
    pacientes_ativos_count = Patient.objects.count()

    context = {
        'fichas_hoje_count': fichas_hoje_count,
        'pacientes_ativos_count': pacientes_ativos_count,
    }
    return render(request, 'core/home.html', context)