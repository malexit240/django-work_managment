import django.forms as fm

from .models import WorkTime, Work, Workplace


class AddWorkTimeForm(fm.ModelForm):
    class Meta:
        model = WorkTime
        fields = ['date_start', 'date_end', 'status']


class AddWorkForm(fm.ModelForm):
    class Meta:
        model = Work
        fields = ['name']


class AddWorkplaceForm(fm.ModelForm):
    class Meta:
        model = Workplace
        fields = ['name']


class HireWorkerForm(fm.ModelForm):
    class Meta:
        model = Workplace
        fields = ['worker', 'status']
