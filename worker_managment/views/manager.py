"""this module contains Manager views"""

from django.views.generic import DetailView

from worker_managment.models import Company


class ManagersList(DetailView):
    """renders list of managers in same company"""

    template_name = 'worker_managment/managers.html'
    model = Company

    def get_context_data(self, object: Company):
        context = super().get_context_data()

        context['company'] = object
        context['managers'] = object.manager_set.all()

        return context
