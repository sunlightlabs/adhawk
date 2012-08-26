from django.contrib import admin
from models import Item

class ItemAdmin(admin.ModelAdmin):
    list_display = ('term', 'acronym', 'synonym', 'slug')
    list_editable = ('acronym', 'synonym', 'slug')
    fieldsets = (
            (None, {
                'fields': ('term', 'acronym', 'synonym', 'definition',)
            }),
        )
    
    def save_model(self, request, obj, form, change):
         obj.update_term_length()
         obj.autogenerate_slug_if_blank()
         obj.save()


admin.site.register(Item, ItemAdmin)
