from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, reverse, redirect, reverse
from django.views.generic import ListView, DetailView, FormView

from worker_managment.models import Company, Work, Workplace
from ..forms import AddWorkForm, AddWorkplaceForm, HireWorkerForm


class WorkList(DetailView):
    template_name = 'worker_managment/works.html'
    model = Company

    def get_context_data(self, object: Company):
        context = super().get_context_data()

        context['works'] = object.work_set.all()
        context['form'] = AddWorkForm()

        return context

    def post(self, request: HttpRequest, pk: int):
        Work.objects.create(name=request.POST.get('name'), company_id=pk)
        return redirect(reverse('works', kwargs={'pk': pk}))


class WorkDetail(DetailView):
    template_name = 'worker_managment/work_details.html'
    model = Work

    def get_context_data(self, object: Work):
        context = super().get_context_data()

        context['workplaces'] = object.workplace_set.all()
        context['form'] = AddWorkplaceForm()

        return context

    def post(self, request: HttpRequest, company_id: int, pk: int):
        Workplace.objects.create(name=request.POST.get('name'), work_id=pk)
        return redirect(reverse('work-details', kwargs={'company_id': company_id, 'pk': pk}))


class WorkplaceDetail(DetailView):
    template_name = 'worker_managment/workplace_details.html'
    model = Workplace

    def get_context_data(self, object: Work):
        context = super().get_context_data()
        context['form'] = HireWorkerForm()

        return context

    def post(self, request: HttpRequest, company_id: int, work_id: int, pk: int):
        Workplace.objects.filter(pk=pk).update(worker_id=request.POST.get(
            'worker'), status=request.POST.get('status'))
        return redirect(reverse('workplace-details',
                                kwargs={'company_id': company_id, 'work_id': work_id, 'pk': pk}))
