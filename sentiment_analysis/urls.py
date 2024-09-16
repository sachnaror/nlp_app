from django.urls import path

from .views import url_input

urlpatterns = [
    path('', url_input, name='url_input'),
]
