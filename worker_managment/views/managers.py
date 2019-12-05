from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, reverse, redirect, reverse
from django.views.generic import ListView, DetailView, FormView

from worker_managment.models import Company, Manager


class ManagersList(DetailView):
    template_name = 'worker_managment/managers.html'
    model = Company

    def get_context_data(self, object: Company):
        context = super().get_context_data()

        context['company'] = object
        context['managers'] = object.manager_set.all()

        return context
