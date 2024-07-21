from django.contrib import admin

from .models import UrlsTemplateView as Model


class ModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "url",
        "template_name",
    ]
    search_fields = [
        "url",
        "template_name",
    ]


admin.site.register(Model, ModelAdmin)
