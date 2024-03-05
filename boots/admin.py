from django.contrib import admin

from boots.models import Boots, BootsImage


class BootsImageAdmin(admin.StackedInline):
    model = BootsImage


class BootsAdmin(admin.ModelAdmin):
    inlines = [BootsImageAdmin]

    class Meta:
        model = Boots


admin.site.register(BootsImage)
admin.site.register(Boots, BootsAdmin)
