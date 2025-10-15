from django.contrib import admin
from .models import Terapeuta, Grupo # Adicione Grupo aqui

admin.site.register(Terapeuta)
admin.site.register(Grupo) # Adicione esta linha