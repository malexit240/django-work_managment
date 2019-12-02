from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, reverse
from django.views.generic import ListView, DetailView, FormView

from worker_managment.models import Worker
from ..forms import AddWorkTimeForm


class WorkersList(ListView):
    template_name = 'worker_managment/workers.html'
    model = Worker
    context_object_name = 'workers'


class WorkerDetails(DetailView):
    template_name = 'worker_managment/worker_details.html'
    model = Worker

    def get_context_data(self, object: Worker, **kwargs):
        context = super().get_context_data(**kwargs)

        context['worker'] = object
        context['workplaces'] = object.workplace_set.all()

        return context


class AddWorkTime(FormView):
    template_name = 'worker_managment/add_worktime.html'
    form_class = AddWorkTimeForm
    succsess_url = '/'

    def form_invalid(self, form):
        return super().form_valid(form)
