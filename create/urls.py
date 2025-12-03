from django.urls import path, include
from . import  views
urlpatterns = [
    path("mainpage/", views.main_page, name="main_page"),
    path("", views.get_page_create_main , name = "create_mainpage" ),
    path("create_character/", views.get_page_create_character, name = "create_character" ),
    path("create_character_submit/" , views.create_character_submit, name = "create_character_submit" ),
    path("create_weapon/", views.get_page_create_weapon, name = "create_weapon" ),
    path("create_weapon_submit/", views.create_weapon_submit, name = "create_weapon_submit")
]