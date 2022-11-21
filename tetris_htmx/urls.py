from django.urls import path, include

from tetris_htmx import views

urlpatterns = [
    path("", views.index, name="index"),
]
