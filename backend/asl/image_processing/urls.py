from django.urls import path

from . import views

urlpatterns = [
    # ex: /image_processing/
    path('', views.index, name='index'),
    # ex: /image_processing/5/
    path('<int:image_id>/', views.detail, name='detail'),
    # ex: /image_processing/upload/
    path('upload/', views.upload, name='upload'),
    # ex: /image_processing/5/delete/
    path('<int:image_id>/delete/', views.delete, name='delete'),
]
