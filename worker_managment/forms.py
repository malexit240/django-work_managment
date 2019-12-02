from django.forms import forms, ModelForm

from .models import WorkTime


class AddWorkTimeForm(ModelForm):
    class Meta:
        model = WorkTime
        fields = ['date_start', 'date_end', 'status']

    def add_worktime():
