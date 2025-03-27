from django.contrib import admin
from .models import Guest, Task, Vendor, Budget, WeddingColor

# Register your models here.
admin.site.register(Guest)
admin.site.register(Task)
admin.site.register(Vendor)
admin.site.register(Budget)
admin.site.register(WeddingColor)
class WeddingColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'hex_code')