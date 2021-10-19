from django.urls import path, re_path
from . import views

app_name="valuation"


urlpatterns = [
    path('initial-form/', views.initial_form, name="initial_form"),
    path('add-summary/<int:id>/', views.add_summary, name="add_summary"),
    path('add-construction/<int:id>/', views.add_construction, name="add_construction"),
    path('add-presentation/<int:id>/', views.add_presentation, name="add_presentation"),

    path('select-comparable/<int:id>/', views.select_comparable, name="select_comparable"),
    path('add-comparable/<int:id>/', views.add_comparable, name="add_comparable"),

    # api call
    path('api/get-city/', views.get_city, name="get_city"),
    path('api/search-comparable/', views.search_comparable, name='search_comparable'),
    path('api/save-photos/', views.save_photos, name="save_photos"),
]