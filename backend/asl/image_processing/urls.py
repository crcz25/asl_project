from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from image_processing.views import template_views
from image_processing.views import api_views

urlpatterns = [
    # ex: /image_processing/
    path('', template_views.index, name='index'),
    # ex: /image_processing/5/
    path('<int:image_id>/', template_views.detail, name='detail'),
    # ex: /image_processing/upload/
    path('upload/', template_views.upload, name='upload'),
    # ex: /image_processing/5/delete/
    path('<int:image_id>/delete/', template_views.delete, name='delete'),
    # For API
    # ex: /image_processing/api/
    path('api/', api_views.ImageList.as_view(), name='api_list'),
    # ex: /image_processing/api/5/
    path('api/<int:pk>/', api_views.ImageDetail.as_view(), name='api_detail'),
    # ex: /image_processing/api/detect
    path('api/detect/', api_views.ImageDetect.as_view(), name='api_detect'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
