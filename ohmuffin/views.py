from rest_framework import viewsets, permissions
from rest_framework.decorators import action

from ohmuffin.models import Profile, Interest
from ohmuffin.serializers import ProfileSerializer, InterestSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows profiles to be viewed or edited.
    """
    queryset = Profile.objects.all().order_by('-created')
    serializer_class = ProfileSerializer
    permission_classes = [permissions.AllowAny]


class InterestViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows profiles to be viewed or edited.
    """
    queryset = Interest.objects.all().order_by('-created')
    serializer_class = InterestSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=["POST"])
    def preferences(self, request, *args, **kwargs):
        import pudb; pudb.set_trace()
        return "z"

