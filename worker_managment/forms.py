import django.forms as fm

from .models import WorkTime


class AddWorkTimeForm(fm.ModelForm):
    class Meta:
        model = WorkTime
        fields = ['date_start', 'date_end', 'status']
        widgets = {
            'date_start':fm.SelectDateWidget()
            }
