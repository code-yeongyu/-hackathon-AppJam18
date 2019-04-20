from rest_framework import serializers
from custom_account.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("id", "name", "group")
