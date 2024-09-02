from django.contrib import admin
from air_pollution.models import Pollution


@admin.register(Pollution)
class PollutionAdmin(admin.ModelAdmin):
    list_display = [
        "entity",
        "iso",
        "year",
        "nitrogen_oxide",
        "sulphur_dioxide",
        "carbon_monoxide",
        "organic_carbon",
        "non_methane_volatile_organic_compounds",
        "black_carbon",
        "ammonia",
    ]
    search_fields = ["entity", "year"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
