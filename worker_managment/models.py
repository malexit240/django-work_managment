"""this module contains worker_managment app models"""

from django.db import models as m
from django.contrib.auth.models import User


class NameAndStrMixin(m.Model):
    """Mixin that adds name field to model and overrides __str__ method
    to return name as result"""

    name = m.CharField(max_length=64, verbose_name='name')

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class StatusMixin:
    """Mixin that adds get_readable_status method to class"""

    def get_readable_status(self):
        """returns string value in pair (int, str) from STATUS field"""
        return self.STATUS[self.status][1]

    class Meta:
        abstract = True


class Company(NameAndStrMixin):
    """Company model"""
    pass


class Manager(NameAndStrMixin):
    """Manager model"""

    company = m.ForeignKey(Company, on_delete=m.CASCADE,
                           related_name='managers')


class Work(NameAndStrMixin):
    """Work model"""

    company = m.ForeignKey(Company, related_name='works', on_delete=m.CASCADE)


class Worker(NameAndStrMixin):
    """Worker model"""

    def get_workplaces(self):
        """returns list of current and past workplaces"""

        current_workplaces = list(self.workplace_set.all())

        workplaces_with_worktime = [
            wt.workplace for wt in self.worktime_set.all()]

        for workplace in workplaces_with_worktime:
            setattr(workplace, 'worktime', workplace.worktime_set.get(
                worker_id=self.pk))

        return list(set(workplaces_with_worktime) | set(current_workplaces))


class Workplace(NameAndStrMixin, StatusMixin):
    """Workplace model"""

    work = m.ForeignKey(Work, on_delete=m.CASCADE, related_name='workplaces')
    worker = m.ForeignKey(Worker, on_delete=m.SET_NULL,
                          null=True, default=None, blank=True, related_name='workplaces')

    STATUS = [(0, ('New')),
              (1, ('Approved')),
              (2, ('Cancelled')),
              (3, ('Finished'))]

    status = m.IntegerField(default=0,
                            choices=STATUS)


class WorkTime(m.Model, StatusMixin):
    """WorkTime model"""

    class Meta:
        unique_together = (('worker', 'workplace'),)

    date_start = m.DateTimeField(null=True, verbose_name=(
        'start date'), blank=True, default=None)
    date_end = m.DateTimeField(null=True, verbose_name=(
        'end date'), blank=True, default=None)

    STATUS = [(0, ('New')),
              (1, ('Approved')),
              (2, ('Cancelled'))]

    status = m.IntegerField(
        default=0, verbose_name=('status'), choices=STATUS)

    worker = m.ForeignKey(Worker, on_delete=m.CASCADE)
    workplace = m.ForeignKey(Workplace, on_delete=m.SET_NULL, null=True)
