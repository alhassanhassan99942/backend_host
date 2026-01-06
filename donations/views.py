# from rest_framework.decorators import api_view
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import generics, permissions, viewsets
from geopy.distance import geodesic
from django.db.models import Q
from .models import *
from .serializers import *
from django.contrib.auth import get_user_model


from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Notification
# from .serializers import NotificationSerializer


class DonationCenterListCreateView(generics.ListCreateAPIView):
    queryset = DonationCenter.objects.all()
    serializer_class = DonationCenterSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can view/create centers

@api_view(["GET"])
def nearby_centers(request):
    try:
        user_lat = float(request.query_params.get("lat"))
        user_lng = float(request.query_params.get("lng"))
    except (TypeError, ValueError):
        return Response({"error": "lat and lng are required"}, status=400)

    centers = DonationCenter.objects.all()
    results = []

    for center in centers:
        distance = geodesic((user_lat, user_lng), (center.latitude, center.longitude)).km
        center_data = DonationCenterSerializer(center).data
        center_data["distance_km"] = round(distance, 2)
        results.append(center_data)

    results = sorted(results, key=lambda x: x["distance_km"])
    return Response(results)


# class BloodRequestListCreateView(generics.ListCreateAPIView):
#     queryset = BloodRequest.objects.all().order_by("-request_date")
#     serializer_class = BloodRequestSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(requester=self.request.user)


# User = get_user_model()

User = get_user_model()


class BloodRequestListCreateView(generics.ListCreateAPIView):
    queryset = BloodRequest.objects.all().order_by("-request_date")
    serializer_class = BloodRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(requester=self.request.user)


# class BloodRequestListCreateView(generics.ListCreateAPIView):
#     queryset = BloodRequest.objects.all().order_by("-request_date")
#     serializer_class = BloodRequestSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_create(self, serializer):
#         # 1. Save the blood request
#         blood_request = serializer.save(requester=self.request.user)

#         # 2. Find matching donors
#         donors = User.objects.filter(
#             is_donor=True,
#             blood_group=blood_request.blood_group
#         )

#         # 3. Create notifications
#         notifications = [
#             Notification(
#                 recipient=donor,
#                 title="New Blood Request",
#                 message=(
#                     f"A new {blood_request.blood_group} blood request "
#                     f"has been posted. Location: {blood_request.town}"
#                 ),
#                 blood_group=blood_request.blood_group,
#                 request_id=blood_request.id
#             )
#             for donor in donors
#         ]



#         # 4. Bulk create for performance
#         Notification.objects.bulk_create(notifications)


class DonationListCreateView(generics.ListCreateAPIView):
    queryset = Donation.objects.all().order_by("-date")
    serializer_class = DonationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(donor=self.request.user)

# class QuestionListView(generics.ListAPIView):
#     queryset = Question.objects.all()
#     serializer_class = QuestionSerializer
#     permission_classes = [permissions.AllowAny]

class QuestionListView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class DonorVerificationCreateView(generics.CreateAPIView):
    serializer_class = DonorVerificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)




# class NotificationViewSet(viewsets.GenericViewSet, generics.ListAPIView):
#     """
#     API endpoint for listing and managing user notifications.
#     """
#     serializer_class = NotificationSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         # Only show notifications for the currently logged-in user
#         return Notification.objects.filter(recipient=self.request.user).order_by('-created_at')

#     @action(detail=False, methods=['post'])
#     def mark_all_as_read(self, request):
#         """
#         Marks all unread notifications for the current user as read.
#         """
#         qs = self.get_queryset().filter(is_read=False)
#         updated_count = qs.update(is_read=True)
#         return Response({'message': f'{updated_count} notifications marked as read.'})

#     @action(detail=True, methods=['post'])
#     def mark_as_read(self, request, pk=None):
#         """
#         Marks a specific notification as read.
#         """
#         try:
#             notification = self.get_queryset().get(pk=pk)
#             if not notification.is_read:
#                 notification.is_read = True
#                 notification.save(update_fields=['is_read'])
#                 return Response({'message': 'Notification marked as read.'})
#             return Response({'message': 'Notification was already read.'})
#         except Notification.DoesNotExist:
#             return Response({'detail': 'Notification not found.'}, status=404)

#     @action(detail=False, methods=['get'])
#     def unread_count(self, request):
#         """
#         Returns the count of unread notifications for the user.
#         """
#         count = self.get_queryset().filter(is_read=False).count()
#         return Response({'unread_count': count})
    


User = get_user_model()

class DonorsListView(generics.ListAPIView):
    serializer_class = DonorSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = User.objects.filter(is_donor=True)

        blood_group = self.request.query_params.get('blood_group')
        town = self.request.query_params.get('town')

        if blood_group:
            qs = qs.filter(blood_group=blood_group)

        if town:
            qs = qs.filter(town=town)

        return qs
    
    
class UserNotificationsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(
            recipient=request.user
        ).order_by('-created_at')

        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

    def patch(self, request, pk):
        notification = Notification.objects.get(
            pk=pk,
            recipient=request.user
        )
        notification.is_read = True
        notification.save()
        return Response({"status": "read"})



