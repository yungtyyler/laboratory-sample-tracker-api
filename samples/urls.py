from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from .views import RegisterView, SampleViewSet, TaskViewSet, UserDetailView
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

router = DefaultRouter()
router.register(r'samples', SampleViewSet, basename='sample')

# Nested router for /samples/<sample_pk>/tasks
# This creates URLs like:
# /api/samples/1/tasks/
# /api/samples/1/tasks/3/
samples_router = routers.NestedDefaultRouter(router, r'samples', lookup='sample')
samples_router.register(r'tasks', TaskViewSet, basename='sample-tasks')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('user/', UserDetailView.as_view(), name='user-detail'),

    path('', include(router.urls)),
    path('', include(samples_router.urls)),
]