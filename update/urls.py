from django.urls import path, include
from . import  views

urlpatterns = [
    path("mainpage/", views.main_page, name="main_page"),
    path("", views.get_page_update_main , name = "update_mainpage" ),
    path("update_character/", views.get_page_update_character, name = "update_character" ),
    path("update_character_img/", views.update_character_img, name="update_character_img"),
    path("update_character_introduction/", views.update_character_introduction, name="update_character_introduction"),
    path("update_weapon/", views.get_page_update_weapon, name = "update_weapon" ),
    path("update_weapon_submit/", views.update_weapon_submit, name = "update_weapon_submit"),
    path("update_location", views.get_page_update_location, name = "update_location" ),
    path("update_location_submit/", views.update_location_submit, name = "update_location_submit" ),
]