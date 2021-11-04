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
    
    # api
    path('api/evaluare-delete/', views.delete_valuation, name='delete'),
    
    # comparable properties 
    path('proprietati-comparabile/', views.comparable_properties, name="comparable_list"),
]