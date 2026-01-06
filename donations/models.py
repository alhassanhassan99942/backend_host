from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
import uuid
from django.db import models
from django.conf import settings

BLOOD_GROUPS = [
        ("A+", "A+"), ("A-", "A-"),
        ("B+", "B+"), ("B-", "B-"),
        ("AB+", "AB+"), ("AB-", "AB-"),
        ("O+", "O+"), ("O-", "O-"),
]

u_list = [
    "Low",
    "Medium",
    "High",
]

class DonationCenter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    town = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    

    def __str__(self):
        return self.name
class BloodRequest(models.Model):
   
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blood_requests"
    )
    
    URGENCY_CHOICES = [
        ('Critical', 'Critical'),
        ('Urgent', 'Urgent'),
        ('Normal', 'Normal'),
    ]
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    urgency = models.CharField(max_length=20, choices=URGENCY_CHOICES, default='Normal')
    # urgency_level = models.CharField(choices=u_list)
    # urgency = models.CharField(_(""), max_length=50)
    description = models.CharField(max_length=250, default='a des')
    quantity_needed = models.PositiveIntegerField(help_text="In units (ml)")
    hospital_name = models.CharField(max_length=255)
    hospital_address = models.CharField(max_length=255)
    request_date = models.DateTimeField(auto_now_add=True)
    fulfilled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.blood_group} requested by {self.requester.id}"

class Donation(models.Model):
    

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Case 1: Donation at a registered center
    center = models.ForeignKey(
        "donations.DonationCenter",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="donations"
    )

    # Case 2: Donation at an unregistered center
    unregistered_center_name = models.CharField(max_length=255, null=True, blank=True)
    unregistered_center_location = models.CharField(max_length=255, null=True, blank=True)
    unregistered_center_contact = models.CharField(max_length=50, null=True, blank=True)

    date = models.DateTimeField(auto_now_add=True)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    town = models.CharField(max_length=50, default="Douala")
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        if self.center:
            return f"{self.donor.username} donated at {self.center.name}"
        return f"{self.donor.username} donated at {self.unregistered_center_name or 'Unknown Center'}"


class Question(models.Model):
    text = models.CharField(max_length=255)
    options = models.JSONField()  # e.g. ["Yes", "No", "Maybe"]
    correct_option = models.IntegerField(default=0)
    key_question = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class DonorVerification(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    answers = models.JSONField()  # {"question_id": "selected_option"}

    # 🔹 Three verification images
    id_document = models.ImageField(upload_to='verifications/id_documents/')
    user_photo = models.ImageField(upload_to='verifications/user_photos/')
    
    selfie_with_id = models.ImageField(upload_to='verifications/selfies/')

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.status}"




User = get_user_model()

class Notification(models.Model):
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    title = models.CharField(max_length=200)
    message = models.TextField()
    blood_group = models.CharField(max_length=5, default="A+") 
    request_id = models.IntegerField(default=1)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.recipient.username}"


# class Notification(models.Model):
#     """
#     Model for storing in-app notifications.
#     """
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     recipient = models.ForeignKey(
#         settings.AUTH_USER_MODEL, 
#         on_delete=models.CASCADE, 
#         related_name='notifications'
#     )
#     title = models.CharField(max_length=100)
#     message = models.TextField()
#     is_read = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     # Optional: Link to a specific object (e.g., BloodRequest)
#     target_blood_request = models.ForeignKey(
#         BloodRequest, 
#         on_delete=models.SET_NULL, 
#         null=True, 
#         blank=True
#     )
    
    
#     class Meta:
#         ordering = ['-created_at']

#     def __str__(self):
#         return f"Notification for {self.recipient.username}: {self.title}"