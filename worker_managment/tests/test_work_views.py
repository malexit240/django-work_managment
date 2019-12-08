from django.test import TestCase
from django.urls import reverse

from worker_managment.views.work import *
from worker_managment.models import Company, Work, Workplace, Worker


class TestWorkList(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name='Company One')
        Work.objects.create(name='A', company=self.company)
        Work.objects.create(name='B', company=self.company)

    def test_get_work_list(self):
        response = self.client.get(
            reverse('wmanagment:works', kwargs={'pk': self.company.pk}))

        self.assertEqual(response.context['company'], self.company)
        self.assertTrue(response.context['works'])

    def test_add_work_post(self):
        response = self.client.post(
            reverse('wmanagment:works', kwargs={'pk': self.company.pk}), {'name': 'C'})

        self.assertTrue(Work.objects.get(name='C'))


class TestWorkDetails(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name='Company One')
        self.work = Work.objects.create(name='A', company=self.company)
        Workplace.objects.create(name='A', work=self.work)
        Workplace.objects.create(name='B', work=self.work)

    def test_get_work_details(self):
        response = self.client.get(
            reverse('wmanagment:work-details', kwargs={'company_id': self.company.pk, 'pk': self.work.pk}))

        self.assertEqual(response.context['work'], self.work)
        self.assertTrue(response.context['workplaces'])

    def test_add_workplace_post(self):
        response = self.client.post(
            reverse('wmanagment:work-details', kwargs={'company_id': self.company.pk, 'pk': self.work.pk}), {'name': 'C'})

        self.assertTrue(Workplace.objects.get(name='C'))


class TestWorkplaceDetails(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name='Company One')
        self.work = Work.objects.create(name='A', company=self.company)
        self.worker = Worker.objects.create(name='A')
        self.workplace = Workplace.objects.create(name='A', work=self.work)

    def test_get_workplace_details(self):
        response = self.client.get(
            reverse('wmanagment:workplace-details', kwargs={'company_id': self.company.pk, 'work_id': self.work.pk, 'pk': self.workplace.pk}))

        self.assertEqual(response.context['work'], self.work)
        self.assertEqual(response.context['workplace'], self.workplace)

    def test_update_workpalce_info_post(self):
        response = self.client.post(
            reverse('wmanagment:workplace-details', kwargs={
                    'company_id': self.company.pk, 'work_id': self.work.pk, 'pk': self.workplace.pk}),
            {'worker': self.worker.pk, 'status': 3})

        self.assertEqual(Workplace.objects.get(
            pk=self.workplace.pk).worker, self.worker)
        self.assertEqual(Workplace.objects.get(pk=self.workplace.pk).status, 3)
