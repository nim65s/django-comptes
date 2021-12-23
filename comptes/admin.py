"""Add models to the admin interface."""
from django.contrib.admin import HORIZONTAL, ModelAdmin, site

from .models import Dette, Occasion, Remboursement


class DetteAdmin(ModelAdmin):
    """Style admin interface for Dette."""

    filter_horizontal = ("debiteurs",)
    radio_fields = {"occasion": HORIZONTAL}
    readonly_fields = ("scribe",)


class RemboursementAdmin(ModelAdmin):
    """Style admin interface for Remboursement."""

    radio_fields = {"occasion": HORIZONTAL}
    readonly_fields = ("scribe",)


site.register(Occasion)
site.register(Dette, DetteAdmin)
site.register(Remboursement, RemboursementAdmin)
