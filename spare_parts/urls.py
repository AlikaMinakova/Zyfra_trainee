from django.urls import path

from . import views

app_name = 'spare_part'
urlpatterns = [
    # SparePartType
    path('spare-part-types/', views.SparePartTypeListView.as_view(), name='spare_part_type_list'),  # +
    path('spare-part-types/create/', views.SparePartTypeCreateView.as_view(), name='spare_part_type_create'),  # +
    path('spare-part-types/<int:pk>/', views.SparePartTypeUpdateView.as_view(), name='spare_part_type_update'),  # +
    path('spare-part-types/<int:pk>/delete/', views.SparePartTypeDeleteView.as_view(), name='spare_part_type_delete'),
    # +

    # SparePart
    path('spare-parts/', views.SparePartListView.as_view(), name='spare_part_list'),  # +
    path('spare-parts/create/', views.SparePartCreateView.as_view(), name='spare_part_create'),  # +
    path('spare-parts/<int:pk>/', views.SparePartDetailView.as_view(), name='spare_part_detail'),  # +
    path('spare-parts/<int:pk>/edit/', views.SparePartUpdateView.as_view(), name='spare_part_update'),  # +
    path('spare-parts/<int:pk>/delete/', views.SparePartDeleteView.as_view(), name='spare_part_delete'),  # +

    # Attribute
    path('attributes/', views.AttributeListView.as_view(), name='attribute_list'),  # +
    path('attributes/create/', views.AttributeCreateView.as_view(), name='attribute_create'),  # +
    path('attributes/<int:pk>/', views.AttributeUpdateView.as_view(), name='attribute_update'),  # +
    path('attributes/<int:pk>/delete/', views.AttributeDeleteView.as_view(), name='attribute_delete'),  # +
]
