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


class Workplace(NameAndStrMixin):
    """Workplace model"""
    work = m.ForeignKey(Work, on_delete=m.CASCADE)


class Worker(NameAndStrMixin):
    """Worker model"""
    workplace = m.OneToOneField(
        Workplace, on_delete=m.SET_NULL, null=True, default=None, blank=True)
