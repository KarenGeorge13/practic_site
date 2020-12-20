from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.views.defaults import page_not_found

urlpatterns = [
    path('', index, name='home'),
    path('news/<int:news_id>/', view_news, name='news'),
    path('news/add_comment/<int:news_id>/<int:user_id>/', add_comment, name='add_comment'),
    path('register/', register, name='register'),
    path('authen/', authen, name='authen'),
    path('logout/', user_logout, name='logout'),
    path('profiles/<int:user_id>/', user_profile, name='profile'),
    path('edit_profile/<int:user_id>/', edit_profile, name='edit_profile'),
    path('add_news/<int:user_id>/', add_news, name='add_news'),
    path('edit_news/<int:news_id>/<int:user_id>/', edit_news, name='edit_news'),
    path('delete_news/<int:news_id>/<int:user_id>/', delete_news, name='delete_news'),
    path('search/', search, name='search')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
