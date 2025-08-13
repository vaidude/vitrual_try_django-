from django.urls import path
from .views import *

urlpatterns = [
    path('', dress_search, name='dress_search'),
    path('dress-search/', dress_search, name='dress_search'),
    path('try-on/', try_on_page, name='try_on_page'),
]