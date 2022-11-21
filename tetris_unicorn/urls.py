from django.urls import path

from tetris_unicorn import views

urlpatterns = [
    path("", views.index, name="index"),
]
