from django.conf.urls import url, include
from rest_framework import routers

from user.viewsets import UserViewSet, BranchViewSet, BranchScheduleViewSet
from . import views

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, 'User')
router.register(r'branch', BranchViewSet, 'Branch')
router.register(r'branch_schedule', BranchScheduleViewSet, 'BranchSchedule')

urlpatterns = [
    url(r'^api/', include(router.urls), name='api'),
    url(r'^api/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^user_login/', views.user_login, name="user_login"),
    url(r'', views.index, name="index"),
]
