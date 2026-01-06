from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("nearby-centers/", views.nearby_centers, name="nearby_centers"),
    path("blood-requests/", views.BloodRequestListCreateView.as_view(), name="blood_requests"),
    path("donations/", views.DonationListCreateView.as_view(), name="donations"),
    path("centers/", views.DonationCenterListCreateView.as_view(), name="donation-centers"),
     path('questions/', views.QuestionListView.as_view(), name='question-list'),
    path('verify/', views.DonorVerificationCreateView.as_view(), name='verify'),
    path('donors/', views.DonorsListView.as_view(), name='donors'),
    # path('notification/', views.NotificationViewSet.as_view(), name='notification' )
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


