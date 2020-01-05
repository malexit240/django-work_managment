"""this module contains urls for wmanagment app"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from worker_managment import views
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'company', views.CompanyViewSet)
router.register(r'manager', views.ManagerViewSet)
router.register(r'work', views.WorkViewSet)
router.register(r'worker', views.WorkerViewSet)
router.register(r'workplace', views.WorkplaceViewSet)
router.register(r'worktime', views.WorkTimeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', obtain_auth_token, name='api_token_auth'),

]
