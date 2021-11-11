from django.contrib import admin
from valuation.models import * 



class AreaAdmin(admin.ModelAdmin):
    list_display = ('name',)

class CityAdmin(admin.ModelAdmin):
    list_display = ('area', 'name',)

class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ('type',)

class CompartmentTypeAdmin(admin.ModelAdmin):
    list_display = ('type',)
    
class StatusAdmin(admin.ModelAdmin):
    list_display = ('status',)

class ValuationPurposeAdmin(admin.ModelAdmin):
    list_display = ('purpose',)

class ValuationApproachAdmin(admin.ModelAdmin):
    list_display = ('approach',)

class StradaTypeAdmin(admin.ModelAdmin):
    list_display = ('type',)

class TransportAdmin(admin.ModelAdmin):
    list_display = ('name',)

class ConformTypeAdmin(admin.ModelAdmin):
    list_display = ('type',)

class StructureTypeAdmin(admin.ModelAdmin):
    list_display = ('type',)

class FoundationTypeAdmin(admin.ModelAdmin):
    list_display = ('type',)

class FloorTypeAdmin(admin.ModelAdmin):
    list_display = ('type',)

class ClouserTypeAdmin(admin.ModelAdmin):
    list_display = ('type',)

class SubcompartmentTypeAdmin(admin.ModelAdmin):
    list_display = ('type',)

class RoofTypeAdmin(admin.ModelAdmin):
    list_display = ('type',)

class InvelitoareTypeAdmin(admin.ModelAdmin):
    list_display = ('type',)

class MobilaTypeAdmin(admin.ModelAdmin):
    list_display = ('type',)

class PropertyRightTypeAdmin(admin.ModelAdmin):
    list_display = ('type',)

class HeatingSystemAdmin(admin.ModelAdmin):
    list_display = ('name',)

class FinishTypeAdmin(admin.ModelAdmin):
    list_display = ('type',)

class UtilityAdmin(admin.ModelAdmin):
    list_display = ('name',)

class AdditionalEquipmentAdmin(admin.ModelAdmin):
    list_display = ('name',)

class CompartimentareAdmin(admin.ModelAdmin):
    list_display = ('name', 'property_type')

# milton
admin.site.register(ScreenShot)
admin.site.register(Anexa1)
admin.site.register(Anexa2)
admin.site.register(Anexa3)
admin.site.register(Anexa4)
admin.site.register(Construction)

admin.site.register(Area, AreaAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(PropertyType, PropertyTypeAdmin)
admin.site.register(CompartmentType, CompartmentTypeAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(ValuationPurpose, ValuationPurposeAdmin)
admin.site.register(ValuationApproach, ValuationApproachAdmin)
admin.site.register(StradaType, StradaTypeAdmin)
admin.site.register(Transport, TransportAdmin)
admin.site.register(ConformType, ConformTypeAdmin)
admin.site.register(StructureType, StructureTypeAdmin)
admin.site.register(FoundationType, FoundationTypeAdmin)
admin.site.register(FloorType, FloorTypeAdmin)
admin.site.register(ClouserType, ClouserTypeAdmin)
admin.site.register(SubcompartmentType, SubcompartmentTypeAdmin)
admin.site.register(RoofType, RoofTypeAdmin)
admin.site.register(InvelitoareType, InvelitoareTypeAdmin)
admin.site.register(MobilaType, MobilaTypeAdmin)
admin.site.register(PropertyRightType, PropertyRightTypeAdmin)
admin.site.register(HeatingSystem, HeatingSystemAdmin)
admin.site.register(FinishType, FinishTypeAdmin)
admin.site.register(Utility, UtilityAdmin)
admin.site.register(AdditionalEquipment, AdditionalEquipmentAdmin)
admin.site.register(Compartimentare, CompartimentareAdmin)
admin.site.register(Photo)