from django.contrib.auth.decorators import login_required
from django.urls import path, re_path
from . import views
from valuationform import views as valuation_view

app_name="dashboard"


urlpatterns = [
    path('', views.dashboardView, name="dashboard"),
    path('add-valuation-old/', views.add_valutation_old, name='add_valuation_old'),
    path('incomplete-valuation/', views.evaluari_incomplete, name='incomplete'), 
    path('incomplete-valuation-map/', views.evaluari_incomplete_map, name='incomplete_map'), 
    path('change-status/<str:status>/<int:id>/', views.change_status, name='change_status'), 
    path('complete-valuation/', views.evaluari_complete, name='complete'),
    path('complete-valuation-map/', views.evaluari_complete_map, name='complete_map'), 
    path('evaluare-details/<int:id>/', views.evaluare_details, name="details"),
    re_path('^pdf/(?P<id>\d+)/$', views.generate_pdf, name='pdf'),

    path('test/', views.test, name='test'),

    # valuationform url call
    path('add-valuation/', valuation_view.add_valuation, name='add_valuation'),
    path('add-valuation/compartimentare/<int:id>/', valuation_view.add_compartment, name='add_compartment'),
    path('add-valuation/custom-field/<int:id>/', valuation_view.add_customfield, name='add_customfield'),
    path('add-valuation/cover-photos/<int:id>/', valuation_view.add_cover_photos, name='add_coverphoto'),
    path('add-valuation/summary/<int:id>/', valuation_view.add_summary, name='add_summary'),
    path('add-valuation/presentation-data/<int:id>/', valuation_view.add_presentation_data, name='add_presentation_data'),
    path('add-valuation/construction/<int:id>/', valuation_view.add_construction, name='add_construction'),
    path('add-valuation/comparabile-date/<int:id>/', valuation_view.subject_comparable, name="sub_comparable"),
    path('add-valuation/anexa/<int:id>/', valuation_view.add_anexa, name='add_anexa'),
    path('comparable-table/add/<int:id>/', valuation_view.add_comptable, name="add_comptable"),
    path('comparable-table/<int:id>/', valuation_view.comparable_table, name="comparable_table"),

    # edit valuation data
    path('edit-valuation/<int:id>/', valuation_view.edit_valuation, name="edit_valuation"),
    path('edit-valuation-summary/<int:id>/', valuation_view.edit_summary, name="edit_summary"),
    path('edit-compartimentare/<int:id>/', valuation_view.edit_compartment, name="edit_compartment"),
    path('edit-custom-fields/<int:id>/', valuation_view.edit_customattrs, name="edit_customattrs"),
    path('edit-presentation-data/<int:id>/', valuation_view.edit_presentation, name="edit_presentation"),
    path('edit-construction/<int:id>/', valuation_view.edit_construction, name="edit_construction"),

    # api url for add valuation 
    path('api/compartment-photos/', valuation_view.compartment_photos, name="compartment_photos"),
    path('api/add-custom-field/', valuation_view.add_custom_field, name="add_custom_field"),
    path('api/customfield-photos/', valuation_view.customfield_photos, name="customfield_photos"),
    path('api/save-cover-photos/', valuation_view.save_cover_photos, name="save_cover_photos"),
    path('api/save-anexa/', valuation_view.save_anexa, name="save_anexa"),
    path('api/evaluare-delete/', views.valuation_form_delete, name='delete'),
    path('api/reorder-image/', views.reorder_cover_image, name='reorder_image'),
    path('api/add-src-doc/', valuation_view.add_source_doc, name='add_src_doc'),

    # comparable properties 
    path('proprietati-comparabile/', views.comparable_properties, name="comparable_list"),
    path('add-comparabile/', valuation_view.add_comparable, name="add_comparable"),
    path('detalii-comparabile/<int:id>/', valuation_view.comparable_details, name="comparable_details"),
    path('edit-comparabile/<int:id>/', valuation_view.edit_comparable, name="edit_comparable"),
    path('api/delete-comparabile/', valuation_view.delete_comparable, name="delete_comparable"),

    # modules
    path('modules/', views.modules_list, name='modules'),
    path('modules/<str:key>', views.go_module, name='go_module_view'),

]