
# # donations/views.py (or where request is created)

# # from notifications.models import Notification
# from django.contrib.auth import get_user_model

# User = get_user_model()

# def create_blood_request(request):
#     serializer = BloodRequestSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     blood_request = serializer.save(requester=request.user)

#     donors = User.objects.filter(
#         isDonor=True,
#         blood_group=blood_request.blood_group
#     )

#     for donor in donors:
#         Notification.objects.create(
#             recipient=donor,
#             title="New Blood Request",
#             message=f"A {blood_request.blood_group} blood request was posted near you.",
#             blood_group=blood_request.blood_group,
#             request_id=blood_request.id
#         )

#     return Response(serializer.data, status=201)

