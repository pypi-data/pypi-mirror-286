from django.contrib import admin
from .models import Ally, Alliance, AllianceStatusChange
from artd_location.models import City  # Asumiendo que City es importado para otra funcionalidad

@admin.register(Ally)
class AllyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "dni",
        "email",
        "city_new",
        "address",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "city_new",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "name",
        "dni",
        "email",
        "city_new__name",
        "address",
        "created_at",
        "updated_at",
    )

@admin.register(Alliance)
class AllianceAdmin(admin.ModelAdmin):
    list_display = (
        "ally",
        "partner",
        "service",
        "benefit",
        "benefit_type",
        "alliance_status",
        "code_alliance",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "benefit_type",
        "alliance_status",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "ally__name",
        "partner__name",
        "service",
        "benefit",
        "code_alliance",
        "created_at",
        "updated_at",
    )

@admin.register(AllianceStatusChange)
class AllianceStatusChangeAdmin(admin.ModelAdmin):
    list_display = (
        "alliance",
        "new_status",
        "old_status",
        "change_date",
        "changed_by",
    )
    list_filter = (
        "change_date",
        "alliance__partner",
    )
    search_fields = (
        "alliance__partner__name",
        "new_status",
        "change_date",
        "changed_by__name",
    )
