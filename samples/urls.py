from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from .views import RegisterView, SampleViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'samples', SampleViewSet, basename='sample')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('', include(router.urls)),
]