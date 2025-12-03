from django.urls import path, include
from . import  views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("mainpage/", views.main_page, name="main_page"),
    path("", views.get_page_read_main , name = "read_mainpage" ),
    path("read_character", views.get_page_read_character, name = "read_character" ),
    path("read_single_character/<int:id>", views.read_single_character, name = "read_single_character" ),
    path("read_calamity", views.get_page_read_calamity, name = "read_calamity" ),
    path("read_chapter", views.get_page_read_chapter, name = "read_chapter" ),
    path("read_single_chapter/<int:chapter_number>/", views.read_single_chapter, name="read_single_chapter"),
    path("read_relationship", views.get_page_read_relationship, name = "read_relationship" ),
]

# 仅在开发模式下服务媒体文件（DEBUG=True 时）
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)