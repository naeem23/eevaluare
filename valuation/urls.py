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
    path('add-anexa/<int:id>/', views.add_anexa, name="add_anexa"),

    # api call
    path('api/get-city/', views.get_city, name="get_city"),
    path('api/search-comparable/', views.search_comparable, name='search_comparable'),
    path('api/save-photos/', views.save_photos, name="save_photos"),
    path('api/add-source/', views.add_source, name='add_source'),
]