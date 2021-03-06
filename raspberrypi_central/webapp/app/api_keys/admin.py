from django.contrib import admin, messages
from .models import APIKey


class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ('id', 'label', 'key', 'created_at', 'modified_at')

    fieldsets = (
        ('Required Information', {'fields': ('label',)}),
        ('Additional Information', {'fields': ('key_message',)}),
    )
    readonly_fields = ('key_message',)
    search_fields = ('id', 'label')


    def has_delete_permission(self, request, obj=None):
        return False


    def key_message(self, obj):
        if obj.key:
            return "Hidden"
        return "The API Key will be generated once you click save."


admin.site.register(APIKey, ApiKeyAdmin)
