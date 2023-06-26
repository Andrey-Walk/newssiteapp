from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from news.views import NewsAPIView, DetailNewsAPIView, FileDetailNewsAPIView


urlpatterns = [
    path('', views.index),
    path('api/news/', NewsAPIView.as_view()),
    path('api/news/<int:pk>', DetailNewsAPIView.as_view()),
    path('api/export/news/', FileDetailNewsAPIView.as_view(), name='export')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
