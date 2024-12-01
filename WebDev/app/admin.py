from django.contrib import admin
from .models import Prizes, UserKey, UserPrize


@admin.register(Prizes)
class PrizesAdmin(admin.ModelAdmin):
    """Призы"""
    list_display = ('id', 'text', 'quantity', 'probability')
    search_fields = ('text',)
    list_display_links = ('text',)
    fieldsets = (
        (None, {
            'fields': ('text', 'quantity', 'probability'),
          }),)

@admin.register(UserKey)
class PrizesAdmin(admin.ModelAdmin):
    """Ключ и пользователь"""
    list_display = ('id', 'full_name', 'secret_key', 'created_at')
    search_fields = ('full_name', 'secret_key')
    list_display_links = ('full_name',)


@admin.register(UserPrize)
class UserPrizeAdmin(admin.ModelAdmin):
    """Выигранные призы"""
    list_display = ('user', 'prize', 'user_secret_key', 'redeemed_at')
    search_fields = ('user__full_name', 'prize__text', 'user__secret_key',)
    readonly_fields = ('user', 'prize', 'redeemed_at')  # Только для чтения
    list_display_links = ('user',)
    fieldsets = (
        (None, {
            'fields': ('user', 'prize', 'redeemed_at'),
        }),
    )

    def user_secret_key(self, obj):
        return obj.user.secret_key  # возвращаем ключ пользователя

    user_secret_key.short_description = 'Ключ пользователя'