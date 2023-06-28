from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from news.views import NewsModelViewSet, FileDetailNewsAPIView


urlpatterns = [
    path('', views.index),
    path('api/news/', NewsModelViewSet.as_view({'get': 'list'})),
    path('api/news/<int:pk>', NewsModelViewSet.as_view({'get': 'retrieve'})),
    path('api/export/news/', FileDetailNewsAPIView.as_view(), name='export')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
