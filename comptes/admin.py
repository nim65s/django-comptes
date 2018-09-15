from django.contrib.admin import HORIZONTAL, ModelAdmin, site

from .models import Dette, Occasion, Remboursement


class DetteAdmin(ModelAdmin):
    filter_horizontal = ('debiteurs', )
    radio_fields = {"occasion": HORIZONTAL}
    readonly_fields = ('scribe', )


class RemboursementAdmin(ModelAdmin):
    radio_fields = {"occasion": HORIZONTAL}
    readonly_fields = ('scribe', )


site.register(Occasion)
site.register(Dette, DetteAdmin)
site.register(Remboursement, RemboursementAdmin)
