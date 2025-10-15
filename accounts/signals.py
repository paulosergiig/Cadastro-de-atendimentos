from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Terapeuta

# Garante que um perfil de terapeuta seja criado ao criar um superusuário pelo createsuperuser
@receiver(post_save, sender=User)
def create_therapist_profile_for_superuser(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        if not hasattr(instance, 'therapist_profile'):
            Terapeuta.objects.create(
                user=instance, 
                nome_completo=instance.username,
                must_change_password=False # Superuser não precisa trocar senha
            )

# Quando o usuário troca a senha, desmarca a flag must_change_password
@receiver(post_save, sender=User)
def user_password_changed(sender, instance, **kwargs):
    if hasattr(instance, 'therapist_profile'):
        # Verifica se a senha foi realmente alterada
        try:
            old_user = User.objects.get(pk=instance.pk)
            if instance.password != old_user.password:
                profile = instance.therapist_profile
                if profile.must_change_password:
                    profile.must_change_password = False
                    profile.save()
        except User.DoesNotExist:
            pass # Usuário sendo criado