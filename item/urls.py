from django.urls import path
from . import views

app_name = 'items'

urlpatterns = [
    path('', views.hello),
    path('api/v1/items', views.get_items, name='items'),
]
