from django.contrib.admin import HORIZONTAL, ModelAdmin, site

from .models import Dette, Occasion, Remboursement, User


class DetteAdmin(ModelAdmin):
    filter_horizontal = ('debiteurs',)
    radio_fields = {"occasion": HORIZONTAL}

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "debiteurs" and not Occasion.objects.filter(membres__isnull=True).exists():
            kwargs['queryset'] = User.objects.filter(occasion__clos=False).distinct()
        return super(DetteAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "creancier" and not Occasion.objects.filter(membres__isnull=True).exists():
            kwargs['queryset'] = User.objects.filter(occasion__clos=False).distinct()
        if db_field.name == "occasion":
            kwargs['queryset'] = Occasion.objects.filter(clos=False)
            kwargs['initial'] = kwargs['queryset'][0]
        return super(DetteAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class RemboursementAdmin(ModelAdmin):

    radio_fields = {"occasion": HORIZONTAL}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in ["crediteur", "credite"] and not Occasion.objects.filter(membres__isnull=True).exists():
            kwargs['queryset'] = User.objects.filter(occasion__clos=False).distinct()
        if db_field.name == "occasion":
            kwargs['queryset'] = Occasion.objects.filter(clos=False)
            kwargs['initial'] = kwargs['queryset'][0]
        return super(RemboursementAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

site.register(Occasion)
site.register(Dette, DetteAdmin)
site.register(Remboursement, RemboursementAdmin)
