from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
# from rest_framework import serializers



class DonationCenterSerializer(serializers.ModelSerializer):
    distance_km = serializers.FloatField(read_only=True)

    class Meta:
        model = DonationCenter
        fields = "__all__"


# class BloodRequestSerializer(serializers.ModelSerializer):
#     requester = serializers.ReadOnlyField(source="requester.username")

#     class Meta:
#         model = BloodRequest
#         fields = "__all__"
#         read_only_fields = ("id", "request_date", "fulfilled")

class BloodRequestSerializer(serializers.ModelSerializer):
    # Fetch details directly from the related 'requester' user
    requester_email = serializers.ReadOnlyField(source='requester.email')
    # Replace 'phone_number' with the actual field name in your User model
    requester_phone = serializers.ReadOnlyField(source='requester.phone_number') 
    requester_name = serializers.ReadOnlyField(source='requester.username') # or first_name

    class Meta:
        model = BloodRequest
        fields = "__all__"
        read_only_fields = ("id","requester", "request_date", "fulfilled")

# class DonationSerializer(serializers.ModelSerializer):
#     donor = serializers.ReadOnlyField(source="donor.username")

#     class Meta:
#         model = Donation
#         fields = "__all__"
#         read_only_fields = ("id", "date")


class DonationSerializer(serializers.ModelSerializer):
    center_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Donation
        fields = [
            "id", "donor",
            "center", "center_name",   # allow user to provide center name
            "unregistered_center_name", "unregistered_center_location", "unregistered_center_contact",
            "date", "blood_group"
        ]
        read_only_fields = ["id", "donor", "date", "center"]

    def validate(self, data):
        if not data.get("center_name") and not data.get("unregistered_center_name"):
            raise serializers.ValidationError(
                "You must provide either a known center name or unregistered center details."
            )
        return data

    def create(self, validated_data):
        center_name = validated_data.pop("center_name", None)

        if center_name:
            try:
                center = DonationCenter.objects.get(name__iexact=center_name.strip())
                validated_data["center"] = center
            except DonationCenter.DoesNotExist:
                validated_data["unregistered_center_name"] = center_name

        return super().create(validated_data)
    

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text', 'options', 'key_question']


class DonorVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonorVerification
        fields = [
            'id', 'user', 'answers',
            'id_document', 'user_photo', 'selfie_with_id',
            'status', 'submitted_at'
        ]
        read_only_fields = ['status', 'submitted_at', 'user']

    def create(self, validated_data):
        user = self.context['request'].user
        return DonorVerification.objects.create(user=user, **validated_data)


class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Notification model.
    """
    class Meta:
        model = Notification
        fields = [
            'id', 'title', 'message', 
            'is_read', 'created_at', 
            'target_blood_request'
        ]
        read_only_fields = ['id', 'created_at']



User = get_user_model()

class DonorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'blood_group',
            'town',
            'phone_number',
        ]

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'