"""this module contains urls for wmanagment app"""

from django.urls import path
from django.views.generic import TemplateView

from .views import *

app_name = 'wmanagment'

urlpatterns = [
    path('', TemplateView.as_view(template_name='worker_managment/index.html', ),
         name='index'),
    path('company/', CompanyList.as_view(), name='company-list'),
    path('company/<int:pk>/',
         CompanyDetails.as_view(), name='company-details'),

    path('company/<int:pk>/manager/',
         ManagersList.as_view(), name='managers-in-company'),

    path('company/<int:pk>/work/', WorkList.as_view(), name='works'),
    path('company/<int:company_id>/work/<int:pk>',
         WorkDetail.as_view(), name='work-details'),

    path('company/<int:company_id>/work/<int:work_id>/workplace/<int:pk>',
         WorkplaceDetail.as_view(), name='workplace-details'),

    path('workers/', WorkersList.as_view(), name='worker-list'),
    path('workers/<int:pk>', WorkerDetails.as_view(), name='worker-details'),

    path('worktime/<int:worker_id>/<int:workplace_id>',
         AddWorkTime.as_view(), name='add-worktime'),
]
