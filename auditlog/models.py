from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class AuditLog(models.Model):
    class Action(models.TextChoices):
        CREATE = 'CREATE', 'Criação'
        UPDATE = 'UPDATE', 'Atualização'
        DELETE = 'DELETE', 'Remoção'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name="Usuário")
    action = models.CharField(max_length=10, choices=Action.choices, verbose_name="Ação")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Timestamp")

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name="Tipo de Objeto")
    object_id = models.PositiveIntegerField(verbose_name="ID do Objeto")
    content_object = GenericForeignKey('content_type', 'object_id')
    
    object_repr = models.CharField(max_length=255, verbose_name="Representação do Objeto")
    changes = models.JSONField(default=dict, verbose_name="Alterações")

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Log de Auditoria'
        verbose_name_plural = 'Logs de Auditoria'

    def __str__(self):
        return f"{self.get_action_display()} em {self.object_repr} por {self.user}"