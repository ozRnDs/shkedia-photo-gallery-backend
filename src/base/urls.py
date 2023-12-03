from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),

    path('about', views.about, name="about"),
    path('login/', views.login_page, name="login"),

    path('albums/<int:page_number>', views.albums, name="albums"),
    path('album/<str:album_name>/<int:page_number>', views.view_album, name="album_view"),
    
    path('media/<str:album_name>/<int:page_number>/<str:media_id>', views.view_media, name="media_view"),
]