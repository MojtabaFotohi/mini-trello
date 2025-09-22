from django.contrib import admin
from .models import Invitation

@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Invitation model.
    
    This class customizes the Django admin interface for the Invitation model,
    defining how invitations are displayed, filtered, and searched in the admin panel.
    """
    list_display = ('board', 'invited_user', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'board')
    search_fields = ('board__title', 'invited_user__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    def get_queryset(self, request):
        """
        Customize the queryset to optimize database queries.
        
        Returns:
            Queryset: A queryset with related board and invited_user selected to reduce database hits.
        """
        return super().get_queryset(request).select_related('board', 'invited_user')