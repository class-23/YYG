"""admin_panel admin"""
from django.contrib import admin

from .models import AdminUser, AdminRoleDefinition, AdminPermission, AdminRolePermission, AdminAuditLog, DataDictionaryEntry


@admin.register(AdminUser)
class AdminUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'nickname', 'role_code', 'is_active', 'last_login_at')
    list_filter = ('is_active', 'role_code')
    search_fields = ('username', 'nickname', 'email', 'phone')


@admin.register(AdminRoleDefinition)
class AdminRoleDefinitionAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name')
    search_fields = ('code', 'name')


@admin.register(AdminPermission)
class AdminPermissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name', 'module')
    list_filter = ('module',)
    search_fields = ('code', 'name')


@admin.register(AdminRolePermission)
class AdminRolePermissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'role', 'permission')


@admin.register(AdminAuditLog)
class AdminAuditLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'operator', 'action', 'target_type', 'target_id', 'result', 'created_at')
    list_filter = ('action', 'target_type', 'result')
    search_fields = ('operator__username', 'target_id')
    readonly_fields = ('created_at',)


@admin.register(DataDictionaryEntry)
class DataDictionaryEntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'code', 'name', 'sort', 'is_active')
    list_filter = ('type', 'is_active')
    search_fields = ('code', 'name')
