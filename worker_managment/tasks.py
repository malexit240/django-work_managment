"""this module contains celery tasks such as search new workers from another source, fill statistics about workers and sending alerts by email"""

import datetime as dt
from pytz import utc
from requests import request
import logging as log
import smtplib
from django.core.mail import send_mass_mail

from Wmanagment.celery_app import app
from .models import Work, Worker, Statistics, Workplace


@app.task
def search_workers():
    """added to DB new workers from typicode.com/users"""

    response = request('GET', 'https://jsonplaceholder.typicode.com/users')

    new_workers = [workers['name'] for workers in response.json()]

    for worker in new_workers:
        if not len(Worker.objects.filter(name=worker)):
            Worker.objects.create(name=worker)

    return Worker.objects.all()


def get_work_time_on_workplace_in_range(workplace: Workplace, date_start: dt.date, date_end: dt.date):
    """returns work time in hours for worker on workplace"""

    work_hours = 0
    for worktime in workplace.worker.worktime_set.all():
        if worktime.workplace == workplace:
            if worktime.date_end > date_start and worktime.date_end < date_end:
                work_hours += (worktime.date_end -
                               worktime.date_start).total_seconds() / 60.0 / 60.0
    return work_hours


@app.task
def send_email_about_overworking(worker_id, work_id, hours):
    """sends emails to managers with alert about worker overwork"""

    worker = Worker.objects.get(pk=worker_id)
    work = Work.objects.get(pk=work_id)
    message = ('Wmanagment. Overwork', '%(worker)s works on %(work)s %(hours)s hours already' % {'worker': worker.name, 'work': work.name, 'hours': hours},
               'wmanagment@company.com',
               [manager.email for manager in work.company.manager_set.all()]
               )

    send_mass_mail(datatuple=(message,))


@app.task
def fill_statistics_for_workers():
    """adds new data to statistics table about worker work times for week"""

    date_week_end = dt.datetime.combine(
        dt.date.today(), dt.datetime.min.time(), tzinfo=utc)
    date_week_start = date_week_end - dt.timedelta(days=7)

    works = Work.objects.all()
    for work in works:
        for workplace in work.workplace_set.all():
            hour_per_week = get_work_time_on_workplace_in_range(
                workplace, date_week_start, date_week_end)
            Statistics.objects.create(worker=workplace.worker, hour_per_week=hour_per_week, workplace=workplace,
                                      date_week_start=date_week_start, date_week_end=date_week_end)
            if hour_per_week > work.time_limit or True:
                send_email_about_overworking.delay(
                    workplace.worker.id, work.id, hour_per_week)
