"""this module contains Work views"""

from django.http import HttpRequest
from django.shortcuts import reverse, redirect
from django.views.generic import FormView

from worker_managment.models import Company, Work, Workplace
from ..forms import AddWorkForm, AddWorkplaceForm, HireWorkerForm


class WorkList(FormView):
    """renders list of works with workplaces in same company"""

    template_name = 'worker_managment/works.html'
    form_class = AddWorkForm
    model = Company

    def get_context_data(self):
        context = super().get_context_data()

        context['company'] = Company.objects.get(pk=self.kwargs['pk'])
        context['works'] = context['company'].work_set.all()

        return context

    def form_valid(self, request: HttpRequest):
        form = self.get_form()

        Work.objects.create(name=form.data['name'],
                            company_id=self.kwargs['pk'])

        return redirect(reverse('wmanagment:works', kwargs=self.kwargs))


class WorkDetail(FormView):
    """renders work details"""

    template_name = 'worker_managment/work_details.html'
    model = Work
    form_class = AddWorkplaceForm

    def get_context_data(self):
        context = super().get_context_data()
        context['work'] = Work.objects.get(pk=self.kwargs['pk'])
        context['workplaces'] = context['work'].workplace_set.all()

        return context

    def form_valid(self, request: HttpRequest):
        form = self.get_form()

        Workplace.objects.create(
            name=form.data['name'], work_id=self.kwargs['pk'])

        redirect_kwargs = {'company_id': self.kwargs['company_id'],
                           'pk': self.kwargs['pk']}

        return redirect(reverse(viewname='wmanagment:work-details',
                                kwargs=redirect_kwargs))


class WorkplaceDetail(FormView):
    """renders workplace details"""

    template_name = 'worker_managment/workplace_details.html'
    form_class = HireWorkerForm
    model = Workplace

    def get_context_data(self):
        context = super().get_context_data()
        context['workplace'] = Workplace.objects.get(pk=self.kwargs['pk'])
        context['work'] = context['workplace'].work

        return context

    def form_valid(self, request: HttpRequest):
        work_id = self.kwargs['work_id']
        pk = self.kwargs['pk']

        form = self.get_form()

        worker_id = form.data['worker']
        status = form.data['status']

        kwargs = {}

        if work_id:
            kwargs['worker_id'] = worker_id
        if status:
            kwargs['status'] = status

        Workplace.objects.filter(pk=pk).update(**kwargs)

        return redirect(reverse(viewname='wmanagment:workplace-details',
                                kwargs=self.kwargs))
