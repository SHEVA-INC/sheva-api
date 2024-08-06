from django.urls import path
from django.conf.urls.static import static

from ShevaAPI import settings
from .views import ReviewListView, ReviewCreateView, ReviewDeleteView, DeleteReviewView

urlpatterns = [
    path('list/', ReviewListView.as_view(), name='review-list'),
    path('create', ReviewCreateView.as_view(), name='review-create'),
    path('delete/<int:pk>', ReviewDeleteView.as_view(), name='review-delete'),
    path('delete/admin/<int:review_id>', DeleteReviewView.as_view(), name='admin_delete_review'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


app_name = "review"
