from django.contrib import admin
from .models import Task, Producto

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created",)

class ProductoAdmin(admin.ModelAdmin):
    readonly_fields = ("createdProduct",)
# Register your models here.

admin.site.register(Task, TaskAdmin)
admin.site.register(Producto, ProductoAdmin)