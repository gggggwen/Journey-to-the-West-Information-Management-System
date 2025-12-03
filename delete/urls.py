from django.urls import path, include
from . import  views
urlpatterns = [
    path("", views.get_page_delete_main , name = "delete_mainpage" ),
    path("delete_character/", views.get_page_delete_character, name = "delete_character" ),
    path("delete_character_submit/" , views.delete_character_submit, name = "delete_character_submit" ),
    path("delete_weapon/", views.get_page_delete_weapon, name = "delete_weapon" ),
    path("delete_weapon_submit/", views.delete_weapon_submit, name = "delete_weapon_submit"),
    path("mainpage/", views.main_page, name="main_page"),
]