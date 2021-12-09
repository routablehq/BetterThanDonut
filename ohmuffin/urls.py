from django.urls import include, path
from rest_framework import routers

from ohmuffin import views

router = routers.DefaultRouter()
router.register(r'interest', views.InterestViewSet)
router.register(r'profile', views.ProfileViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
]
