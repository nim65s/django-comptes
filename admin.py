#-*- coding: utf-8 -*-

from django.contrib.admin import site, ModelAdmin, HORIZONTAL
from models import *


class DetteAdmin(ModelAdmin):

    radio_fields = {"occasion": HORIZONTAL}

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "debiteurs":
            kwargs['queryset'] = User.objects.filter(occasion__clos=False).distinct()
        return super(DetteAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "creancier":
            kwargs['queryset'] = User.objects.filter(occasion__clos=False).distinct()
        if db_field.name == "occasion":
            kwargs['queryset'] = Occasion.objects.filter(clos=False)
            if len(kwargs['queryset']) == 1:
                kwargs['initial'] = kwargs['queryset'][0]
        return super(DetteAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class RemboursementAdmin(ModelAdmin):

    radio_fields = {"occasion": HORIZONTAL}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in ["crediteur", "credite"]:
            kwargs['queryset'] = User.objects.filter(occasion__clos=False).distinct()
        if db_field.name == "occasion":
            kwargs['queryset'] = Occasion.objects.filter(clos=False)
            if len(kwargs['queryset']) == 1:
                kwargs['initial'] = kwargs['queryset'][0]
        return super(RemboursementAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

site.register(Occasion)
site.register(Dette, DetteAdmin)
site.register(Remboursement)
site.register(Couple)
