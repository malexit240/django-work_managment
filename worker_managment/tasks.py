import datetime as dt
from pytz import utc
from requests import request
import logging as log
import smtplib
from email.message import EmailMessage

#from Wmanagment.celery_app import app
from .models import Work, Worker, Statistics, Workplace


# @app.task
def search_workers():
    response = request('GET', 'https://jsonplaceholder.typicode.com/users')

    new_workers = [workers['name'] for workers in response.json()]

    for worker in new_workers:
        if not len(Worker.objects.filter(name=worker)):
            Worker.objects.create(name=worker)

    return Worker.objects.all()


def get_work_time_on_workplace_in_range(workplace: Workplace, date_start: dt.date, date_end: dt.date):
    work_hours = 0
    for worktime in workplace.worker.worktime_set.all():
        if worktime.workplace == workplace:
            if worktime.date_end > date_start and worktime.date_end < date_end:
                work_hours += (worktime.date_end -
                               worktime.date_start).total_seconds() / 60.0 / 60.0
    return work_hours


# @app.task
def fill():
    log.warning('Task executed')


def fill_statistics_for_workers():
    date_week_end = dt.datetime.combine(
        dt.date.today(), dt.datetime.min.time(), tzinfo=utc)
    date_week_start = date_week_end - dt.timedelta(days=7)

    works = Work.objects.all()
    for work in works:
        for workplace in work.workplace_set.all():
            Statistics.objects.create(worker=workplace.worker, hour_per_week=get_work_time_on_workplace_in_range(workplace, date_week_start, date_week_end), workplace=workplace,
                                      date_week_start=date_week_start, date_week_end=date_week_end)


def send_email():
    msg = EmailMessage()
    msg.set_content('Worker has worked over than limit')

    with smtplib.SMTP('localhost') as s:
        s.send_message(msg)
