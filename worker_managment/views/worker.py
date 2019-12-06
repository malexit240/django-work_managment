"""this module contains Worker views"""

from django.http import HttpRequest
from django.shortcuts import reverse, redirect
from django.views.generic import ListView, DetailView, FormView

from worker_managment.models import Worker, WorkTime
from ..forms import AddWorkTimeForm


class WorkersList(ListView):
    """renders list of workers"""

    template_name = 'worker_managment/workers.html'
    model = Worker
    context_object_name = 'workers'


class WorkerDetails(DetailView):
    """renders worker details"""

    template_name = 'worker_managment/worker_details.html'
    model = Worker

    def get_context_data(self, object: Worker, **kwargs):
        context = super().get_context_data(**kwargs)

        context['workplaces'] = object.get_workplaces()

        return context


class AddWorkTime(FormView):
    """renders form to add worktime to worker his workplaces history"""

    template_name = 'worker_managment/add_worktime.html'
    form_class = AddWorkTimeForm

    def form_valid(self, request: HttpRequest):
        form = self.get_form()

        WorkTime.objects.create(date_start=form.data['date_start'],
                                date_end=form.data['date_end'],
                                status=form.data['status'],
                                worker_id=self.kwargs['worker_id'],
                                workplace_id=self.kwargs['workplace_id'])

        return redirect(reverse(viewname='wmanagment:worker-details',
                                kwargs={"pk": self.kwargs['worker_id']}))
