from django.urls import path, include
from rest_framework import routers, serializers, viewsets
from crudsandthreads import views as ctviews

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'students', ctviews.StudentViewSet)
router.register(r'attendance', ctviews.AttendanceViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('threading_example', ctviews.ThreadingExampleView.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
