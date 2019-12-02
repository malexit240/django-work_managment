"""this module contains worker_managment app models"""

from django.db import models as m


class NameAndStrMixin(m.Model):
    """Mixin that adds name field to model and overrides __str__ method to return name as result"""
    name = m.CharField(max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Company(NameAndStrMixin):
    """Company model"""
    pass


class Manager(NameAndStrMixin):
    """Manager model"""
    company = m.ForeignKey(Company, on_delete=m.CASCADE)  # ???


class Work(NameAndStrMixin):
    """Work model"""
    company = m.ForeignKey(Company, on_delete=m.CASCADE)


class Worker(NameAndStrMixin):
    """Worker model"""
    pass


class Workplace(NameAndStrMixin):
    """Workplace model"""
    work = m.ForeignKey(Work, on_delete=m.CASCADE)
    worker = m.ForeignKey(Worker, on_delete=m.SET_NULL,
                          null=True, default=None, blank=True)
    status = m.IntegerField(default=1,
                            choices=[(1, 'New'), (2, 'Approved'), (3, 'Cancelled'), (4, 'Finished')])


class WorkTime(m.Model):
    """WorkTime model"""
    date_start = m.DateTimeField(null=True, blank=True, default=None)
    date_end = m.DateTimeField(null=True, blank=True, default=None)
    status = m.IntegerField(default=1,
                            choices=[(1, 'New'), (2, 'Approved'), (3, 'Cancelled')])
    worker = m.ForeignKey(Worker, on_delete=m.CASCADE)
    workplace = m.OneToOneField(Workplace, on_delete=m.SET_NULL, null=True)
