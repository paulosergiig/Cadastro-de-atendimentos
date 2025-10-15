import json
from datetime import date, datetime
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_str
from crum import get_current_request

from .models import AuditLog
from patients.models import Patient, FichaEvolucao, FichaTriagem, Anamnese
from accounts.models import Terapeuta

# Lista dos modelos que queremos auditar
AUDITED_MODELS = [Patient, FichaEvolucao, FichaTriagem, Anamnese, Terapeuta]

def json_serializable(value):
    """Converte valores que não são JSON serializáveis (como data/hora) para string."""
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    return force_str(value, strings_only=True)

@receiver(pre_save)
def capture_old_state(sender, instance, **kwargs):
    if sender in AUDITED_MODELS and instance.pk:
        try:
            instance._old_state = sender.objects.get(pk=instance.pk).__dict__
        except sender.DoesNotExist:
            instance._old_state = None

@receiver(post_save)
def log_create_update(sender, instance, created, **kwargs):
    if sender not in AUDITED_MODELS:
        return

    request = get_current_request()
    user = request.user if request and request.user.is_authenticated else None
    
    changes = {}
    
    if created:
        action = AuditLog.Action.CREATE
        new_state = instance.__dict__
        for field, value in new_state.items():
            if field not in ['_state', '_old_state', 'id', '_pre_save_state']:
                changes[field] = {'new': json_serializable(value)}
    else:
        action = AuditLog.Action.UPDATE
        if hasattr(instance, '_old_state') and instance._old_state is not None:
            old_state = instance._old_state
            new_state = instance.__dict__
            for key, value in old_state.items():
                if key in new_state and new_state[key] != value:
                    changes[key] = {
                        'old': json_serializable(value),
                        'new': json_serializable(new_state[key])
                    }
    
    if not changes and action == AuditLog.Action.UPDATE:
        return # Nenhuma alteração real foi feita

    AuditLog.objects.create(
        user=user,
        action=action,
        content_type=ContentType.objects.get_for_model(sender),
        object_id=instance.pk,
        object_repr=str(instance),
        changes=changes
    )

@receiver(post_delete)
def log_delete(sender, instance, **kwargs):
    if sender not in AUDITED_MODELS:
        return
        
    request = get_current_request()
    user = request.user if request and request.user.is_authenticated else None
    
    AuditLog.objects.create(
        user=user,
        action=AuditLog.Action.DELETE,
        content_type=ContentType.objects.get_for_model(sender),
        object_id=instance.pk,
        object_repr=str(instance),
        changes={'deleted_object': str(instance)}
    )