from django.contrib import admin
from .models import List, Task

@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    """
    Admin configuration for the List model.
    
    This class customizes the Django admin interface for the List model,
    defining how lists are displayed, filtered, and searched in the admin panel.
    """
    list_display = ('title', 'board', 'created_at', 'updated_at')
    list_filter = ('board', 'created_at', 'updated_at')
    search_fields = ('title', 'board__title')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    def get_queryset(self, request):
        """
        Customize the queryset to optimize database queries.
        
        Returns:
            Queryset: A queryset with related board selected to reduce database hits.
        """
        return super().get_queryset(request).select_related('board')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Task model.
    
    This class customizes the Django admin interface for the Task model,
    defining how tasks are displayed, filtered, and searched in the admin panel.
    """
    list_display = ('title', 'list', 'due_date', 'order', 'created_at', 'updated_at')
    list_filter = ('list', 'due_date', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'list__title')
    ordering = ('-created_at',)
    filter_horizontal = ('assigned_users',)
    readonly_fields = ('created_at', 'updated_at')

    def get_queryset(self, request):
        """
        Customize the queryset to optimize database queries.
        
        Returns:
            Queryset: A queryset with related list and assigned_users prefetched to reduce database hits.
        """
        return super().get_queryset(request).select_related('list').prefetch_related('assigned_users')

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """
        Customize the form field for the 'assigned_users' ManyToMany field.
        
        Args:
            db_field: The database field being processed.
            request: The current request object.
            **kwargs: Additional keyword arguments.
        
        Returns:
            FormField: Customized form field for the ManyToMany relationship.
        """
        if db_field.name == 'assigned_users':
            kwargs['queryset'] = db_field.related_model.objects.order_by('username')
        return super().formfield_for_manytomany(db_field, request, **kwargs)