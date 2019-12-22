"""this module contains Company views"""

from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group

from worker_managment.models import Company
import logging as log


class CompanyList(LoginRequiredMixin, ListView):
    """renders list of companies

    this view requires authenticated user
    """

    template_name = 'worker_managment/companies.html'
    model = Company
    context_object_name = 'companies'


class CompanyDetails(PermissionRequiredMixin, DetailView):
    """renders list of works with aditional informaion

    this view requires permission to view company
    """

    permission_required = ['worker_managment | company | Can view company']

    template_name = 'worker_managment/company_details.html'
    model = Company

    def get_context_data(self, object: Company, **kwargs):
        context = super().get_context_data(**kwargs)
        company = object

        context['company'] = company
        context['works'] = company.work_set.all()

        return context
