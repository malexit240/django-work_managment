from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from worker_managment.models import Company


def index(request):
    """renders list of companies"""
    return render(request,
                  'worker_managment/index.html',
                  context={'companies': Company.objects.all()},
                  status=200)


def details(request, company_id: int):
    """renders list of works with aditional informaion"""
    company = Company.objects.get(pk=company_id)

    works = [{
        'name': work.name,
        'workplaces': work.workplace_set.all(), }
        for work in company.work_set.all()]

    return render(request,
                  'worker_managment/details.html',
                  context={'company': company,
                           'works': works},
                  status=200)
