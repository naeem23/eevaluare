from django.urls import path, re_path
from . import views

app_name="dashboard"


urlpatterns = [
    path('', views.dashboardView, name="dashboard"),
    path('incomplete-valuation/', views.evaluari_incomplete, name='incomplete'), 
    path('incomplete-valuation-map/', views.evaluari_incomplete_map, name='incomplete_map'), 
    path('change-status/<int:status>/<int:id>/', views.change_status, name='change_status'), 
    path('complete-valuation-map/', views.evaluari_complete_map, name='complete_map'), 
    path('evaluare-details/<int:id>/', views.evaluare_details, name="details"),
    path('api/evaluare-delete/', views.delete_valuation, name='delete'),
    path('pdf/<int:id>/', views.pdf, name='pdf'),
    
    # comparable properties 
    path('proprietati-comparabile/', views.comparable_properties, name="comparable_list"),
    path('comparabile-map/', views.comparabile_map, name='comparabile_map'), 
    path('api/delete-comparabile/', views.delete_comp_prop, name="delete_comp_prop"),

    # modules
    path('modules/', views.modules_list, name='modules'),
    path('modules/<str:key>', views.go_module, name='go_module_view'),
    path('modules/module/delete/<str:key>/<int:id>', views.delete_module, name='delete_module_view'),
]