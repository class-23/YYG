"""message admin - 消息管理"""
from django.contrib import admin

from .models import Message, MessageReceipt


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'business_id', 'user', 'type', 'title', 'created_at')
    list_filter = ('type',)
    search_fields = ('business_id', 'title', 'content', 'user__nickname')
    date_hierarchy = 'created_at'
    raw_id_fields = ('user',)


@admin.register(MessageReceipt)
class MessageReceiptAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'user', 'is_read', 'is_pushed', 'read_at', 'pushed_at')
    list_filter = ('is_read', 'is_pushed')
    date_hierarchy = 'read_at'
    raw_id_fields = ('message', 'user')
