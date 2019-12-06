"""this module contains Company views"""

from django.views.generic import ListView, DetailView

from worker_managment.models import Company


class CompanyList(ListView):
    """renders list of companies"""

    template_name = 'worker_managment/companies.html'
    model = Company
    context_object_name = 'companies'


class CompanyDetails(DetailView):
    """renders list of works with aditional informaion"""

    template_name = 'worker_managment/company_details.html'
    model = Company

    def get_context_data(self, object: Company, **kwargs):
        context = super().get_context_data(**kwargs)
        company = object

        context['company'] = company
        context['works'] = company.work_set.all()

        return context
