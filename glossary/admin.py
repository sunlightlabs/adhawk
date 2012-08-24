from django.contrib import admin
from models import Item

class ItemAdmin(admin.ModelAdmin):
    list_display = ('term', 'acronym', 'synonym', )
    fieldsets = (
            (None, {
                'fields': ('term', 'acronym', 'synonym', 'definition', 'sectors')
            }),
        )
    
    def save_model(self, request, obj, form, change):
         obj.update_term_length()
         obj.autogenerate_slug_if_blank()
         obj.save()


admin.site.register(Item, ItemAdmin)