from django.contrib import admin
from . import models


class AreaAdmin(admin.ModelAdmin):
	list_display = ('auto', 'name')
	list_display_links = ('auto', 'name')


class CityAdmin(admin.ModelAdmin):
	list_display = ('area', 'name')
	list_display_links = ('area', 'name')


class EvaluareFormAdmin(admin.ModelAdmin):
	list_display  = ('reference_no', 'property_type', 'street', 'city')


class PresentationDataAdmin(admin.ModelAdmin):
	list_display = ('ref_no', 'cadastral_no', 'land_book_no')


class ConstructionAdmin(admin.ModelAdmin):
	list_display = ('ref_no', 'structure', 'foundation')


class SuprafeteAdmin(admin.ModelAdmin):
	list_display = ('ref_no', 'room_name', 'area')


class AnexaAdmin(admin.ModelAdmin):
	list_display = ('ref_no', 'refer_to', 'file_name')


class ResidentialAttrAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'has_photo', 'has_nr')
	list_display_links = ('id', 'name')


class ResidentialAttrValueAdmin(admin.ModelAdmin):
	list_display = ('ref_no', 'attr_id', 'attr_value', 'mav', 'iav')
	list_display_links = ('ref_no', 'attr_value', 'mav', 'iav')


class ResidentialAttrFileAdmin(admin.ModelAdmin):
	list_display = ('ref_no', 'attr_id', 'file_name')
	list_display_links = ('ref_no', 'file_name')


class CustomFieldValueAdmin(admin.ModelAdmin):
	list_display = ('ref_no', 'attr_name', 'attr_value')
	list_display_links = ('ref_no', 'attr_name', 'attr_value')


class CustomFieldFileAdmin(admin.ModelAdmin):
	list_display = ('ref_no', 'attr_id', 'file_name')
	list_display_links = ('ref_no', 'file_name')


class PhotoAdmin(admin.ModelAdmin):
	list_display = ('ref_no', 'refer_to', 'image', 'image_order')
	list_display_links = ('ref_no', 'image')


class ValuationSummaryAdmin(admin.ModelAdmin):
	list_display = ('ref_no', 'purpose', 'approach')
	list_display_links = ('ref_no', 'purpose', 'approach')


class SourceofInformationAdmin(admin.ModelAdmin):
	list_display = ('ref_no', 'source')


admin.site.register(models.Area, AreaAdmin)
admin.site.register(models.City, CityAdmin)
admin.site.register(models.EvaluareForm, EvaluareFormAdmin)
admin.site.register(models.PresentationData, PresentationDataAdmin)
admin.site.register(models.Construction, ConstructionAdmin)
admin.site.register(models.Suprafete, SuprafeteAdmin)
admin.site.register(models.Anexa, AnexaAdmin)
admin.site.register(models.ResidentialAttr, ResidentialAttrAdmin)
admin.site.register(models.ResidentialAttrValue, ResidentialAttrValueAdmin)
admin.site.register(models.ResidentialAttrFile, ResidentialAttrFileAdmin)
admin.site.register(models.CustomFieldValue, CustomFieldValueAdmin)
admin.site.register(models.CustomFieldFile, CustomFieldFileAdmin)
admin.site.register(models.Photo, PhotoAdmin)
admin.site.register(models.ValuationSummary, ValuationSummaryAdmin)
admin.site.register(models.SourceofInformation, SourceofInformationAdmin)