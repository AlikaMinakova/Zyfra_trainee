from django.contrib import admin

from item.models import Item


class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'pub_date'
    )
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


admin.site.register(Item, ItemAdmin)
