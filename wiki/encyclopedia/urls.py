from django.urls import path

from . import views

# app_name = 'encyclopedia'
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.render_entry, name="render_entry"),
    path("random_entry/", views.random_entry, name="random_entry"),
    path("search_results/<str:search_term>", views.search_results, name="search_results"),
    path("new_entry/", views.new_entry, name="new_entry"),
    path("edit_entry/<str:title>", views.edit_entry, name="edit_entry")
]
