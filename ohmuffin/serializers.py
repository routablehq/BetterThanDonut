from rest_framework import serializers

from ohmuffin.models import Profile, Interest


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "created", "modified", "first_name", "last_name", "interests"]
        read_only_fields = ["id", "created", "modified"]


class InterestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Interest
        fields = ["id", "created", "modified", "name"]
        read_only_fields = ["id", "created", "modified"]
