from django.shortcuts import render
from django.http import HttpResponse,HttpRequest
from django.shortcuts import render, reverse,redirect,reverse
from django.views.generic import ListView, DetailView, FormView

from worker_managment.models import Worker,WorkTime,Workplace
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
        context['worktimes'] = object.worktime_set.all()
        context['worktimes'] = object.workspace_set.all()

        return context


class AddWorkTime(FormView):
    template_name = 'worker_managment/add_worktime.html'
    form_class = AddWorkTimeForm
    succsess_url = '/'

    def post(self,request:HttpRequest,worker_id,workplace_id):
        form_args = request.POST
        WorkTime.objects.create(date_start=form_args.get('date_start'),date_end=form_args.get('date_get'),status=form_args.get('status'),worker_id=worker_id,workplace_id=workplace_id)
        return redirect(reverse('worker-details',kwargs={"pk":worker_id}))
