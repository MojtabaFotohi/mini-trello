from django.contrib import admin
from .models import Board

@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Board model.
    
    This class customizes the Django admin interface for the Board model,
    defining how the model is displayed, filtered, and searched in the admin panel.
    """
    list_display = ('title', 'owner', 'color', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'owner')
    search_fields = ('title', 'owner__username')
    ordering = ('-created_at',)
    filter_horizontal = ('members',)
    readonly_fields = ('created_at', 'updated_at')

    def get_queryset(self, request):
        """
        Customize the queryset to optimize database queries.
        
        Returns:
            Queryset: A queryset with related owner and members selected to reduce database hits.
        """
        return super().get_queryset(request).select_related('owner').prefetch_related('members')

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """
        Customize the form field for the 'members' ManyToMany field.
        
        Args:
            db_field: The database field being processed.
            request: The current request object.
            **kwargs: Additional keyword arguments.
        
        Returns:
            FormField: Customized form field for the ManyToMany relationship.
        """
        if db_field.name == 'members':
            kwargs['queryset'] = db_field.related_model.objects.order_by('username')
        return super().formfield_for_manytomany(db_field, request, **kwargs)