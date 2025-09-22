from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Admin configuration for the custom User model.
    
    This class customizes the Django admin interface for the User model,
    extending the default UserAdmin to include custom fields and optimize display.
    """
    model = User
    list_display = ('username', 'email', 'name', 'preferred_language', 'is_staff', 'is_active')
    list_filter = ('preferred_language', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'name')
    ordering = ('username',)
    
    # Customize fieldsets to include custom fields
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('name', 'email', 'preferred_language')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Customize add fieldsets for user creation
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'name', 'preferred_language', 'password1', 'password2'),
        }),
    )
    
    def get_queryset(self, request):
        """
        Customize the queryset to optimize database queries.
        
        Returns:
            Queryset: A queryset with related groups and user_permissions prefetched to reduce database hits.
        """
        return super().get_queryset(request).prefetch_related('groups', 'user_permissions')