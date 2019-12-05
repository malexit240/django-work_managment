from django.urls import path
from django.views.generic import TemplateView

from .views import index, CompanyDetails, WorkersList, WorkerDetails, AddWorkTime, ManagersList, WorkList, WorkDetail, WorkplaceDetail

urlpatterns = [
    path('', TemplateView.as_view(template_name='worker_managment/wmanagment_index.html', ),
         name='wmanagment-root'),
    path('company/', index, name='company-list'),
    path('company/<int:pk>/',
         CompanyDetails.as_view(), name='company-details'),

    path('company/<int:pk>/manager/',
         ManagersList.as_view(), name='managers-in-company'),

    path('company/<int:pk>/work/', WorkList.as_view(), name='works'),
    path('company/<int:company_id>/work/<int:pk>',
         WorkDetail.as_view(), name='work-details'),

    path('company/<int:company_id>/work/<int:work_id>/workplace/<int:pk>',
         WorkplaceDetail.as_view(), name='workplace-details'),

    path('workers/', WorkersList.as_view(), name='workers'),
    path('workers/<int:pk>', WorkerDetails.as_view(), name='worker-details'),

    path('worktime/<int:worker_id>/<int:workplace_id>',
         AddWorkTime.as_view(), name='add-worktime'),
]
