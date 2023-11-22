from django.contrib import admin

from weather.models import BotUser, Message, APIRequestLog


@admin.register(APIRequestLog)
class APIRequestLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'remote_addr', 'path', 'request_method', 'status_code')


@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'name')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'bot_user', 'request_msg', 'response_msg', 'created_at')
