from django.urls import path, re_path
from . import views

app_name="valuation"


urlpatterns = [
    path('initial-form/', views.initial_form, name="initial_form"),
    path('add-summary/<int:id>/', views.add_summary, name="add_summary"),
    path('add-construction/<int:id>/', views.add_construction, name="add_construction"),
    path('add-presentation/<int:id>/', views.add_presentation, name="add_presentation"),
    path('add-market-analysis/<int:id>/', views.add_market_analysis, name="add_market_analysis"),
    path('select-comparable/<int:id>/', views.select_comparable, name="select_comparable"),
    path('add-comparable/<int:id>/', views.add_comparable, name="add_comparable"),
    path('edit-comparable/<int:id>/', views.edit_comparable, name="edit_comparable"),
    path('edit-valuation/<int:id>/', views.edit_initial_data, name="edit_initial"),

    path('test/', views.test, name="test"),

    # milton
    path('add-anexa1/<int:id>/', views.add_anexa1, name="add_anexa1"),
    path('add-anexa2/<int:id>/', views.add_anexa2, name="add_anexa2"),
    path('add-anexa3/<int:id>/', views.add_anexa3, name="add_anexa3"),
    path('add-anexa4/<int:id>/', views.add_anexa4, name="add_anexa4"),
    path('delete/file/', views.delete_file, name="delete_file"), # ajax to delete file
    path('screenshot/file/', views.screenshot_html, name="screenshot_html"), # ajax to screen shot

    # api call
    path('api/get-city/', views.get_city, name="get_city"),
    path('api/search-comparable/', views.search_comparable, name='search_comparable'),
    path('api/save-photos/', views.save_photos, name="save_photos"),
    path('api/add-source/', views.add_source, name='add_source'),
    path('api/reorder-photos/', views.reorder_photos, name='reorder_photos'),
    path('api/delete-photos/', views.delete_photos, name='delete_photos'),
    path('api/delete-image/', views.delete_image, name='delete_image'),
    path('api/delete-suprafete/', views.delete_suprafete, name='delete_suprafete'),
    path('api/update-sources/', views.update_sources, name='update_sources'),
    path('api/delete-sources/', views.delete_source, name='delete_source'),
    path('api/delete-custom/', views.delete_custom_field, name='delete_custom'),

    # comparable property url 
    path('add-comparabile/', views.add_comp_prop, name="add_comp_prop"),
    path('detalii-comparabile/<int:id>/', views.comp_prop_details, name="comp_prop_details"),
    path('api/property-files/', views.porperty_files, name="porperty_files"),
    path('api/delete/property-files/', views.delete_porperty_files, name="delete_prop_files"),
]