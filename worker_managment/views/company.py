from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from worker_managment.models import Company


def index(request):
    """renders list of companies"""
    return render(request,
                  'worker_managment/index.html',
                  context={'companies': Company.objects.all()},
                  status=200)


class CompanyDetails(DetailView):
    """renders list of works with aditional informaion"""

    template_name = 'worker_managment/details.html'
    model = Company

    def get_context_data(self, object: Company, **kwargs):
        context = super().get_context_data(**kwargs)
        company = object

        # works = [{
        #     'name': work.name,
        #     'workplaces': work.workplace_set.all(), }
        #     for work in company.work_set.all()]

        context['company'] = company
        context['works'] = company.work_set.all()

        return context
