from django.urls import path

from vehicle import views

app_name = 'vehicle'
urlpatterns = [
    path('vehicles/', views.VehicleListView.as_view(), name='vehicle_list'),
    path('vehicles/create/', views.VehicleCreateView.as_view(), name='vehicle_create'),
    path('vehicles/<int:pk>/', views.VehicleDetailView.as_view(), name='vehicle_detail'),
    path('vehicles/<int:pk>/edit/', views.VehicleUpdateView.as_view(), name='vehicle_update'),
    path('vehicles/<int:pk>/delete/', views.VehicleDeleteView.as_view(), name='vehicle_delete'),
    path('vehicle-types/', views.VehicleTypeListView.as_view(), name='vehicletype_list'),
    path('vehicle-types/create/', views.VehicleTypeCreateView.as_view(), name='vehicletype_create'),
    path('vehicle-types/<int:pk>/', views.VehicleTypeUpdateView.as_view(), name='vehicletype_update'),
    path('vehicle-types/<int:pk>/delete/', views.VehicleTypeDeleteView.as_view(), name='vehicletype_delete'),
]
