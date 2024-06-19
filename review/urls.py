from django.urls import path
from django.conf.urls.static import static

from ShevaAPI import settings
from .views import ReviewListView, ReviewCreateView, ReviewDeleteView

urlpatterns = [
    path('list/', ReviewListView.as_view(), name='review-list'),
    path('reviews/create', ReviewCreateView.as_view(), name='review-create'),
    path('reviews/delete/<int:pk>', ReviewDeleteView.as_view(), name='review-delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


app_name = "review"
