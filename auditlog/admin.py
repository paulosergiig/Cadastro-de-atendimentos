from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'action', 'object_repr', 'content_type')
    list_filter = ('action', 'timestamp', 'content_type')
    search_fields = ('object_repr', 'user__username')
    readonly_fields = ('timestamp', 'user', 'action', 'content_type', 'object_id', 'object_repr', 'changes')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False