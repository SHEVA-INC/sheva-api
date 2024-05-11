from django.contrib import admin
from boots.models import Boots, BootsImage, Size

class BootsImageInline(admin.StackedInline):
    model = BootsImage
    extra = 1

class SizeInline(admin.TabularInline):
    model = Size
    extra = 1

class BootsAdmin(admin.ModelAdmin):
    inlines = [BootsImageInline, SizeInline]
    list_display = ['name', 'price', 'color', 'brand', 'new', 'popular', 'main_image']
    search_fields = ['name', 'brand', 'color']

admin.site.register(Boots, BootsAdmin)
admin.site.register(BootsImage)
admin.site.register(Size)
