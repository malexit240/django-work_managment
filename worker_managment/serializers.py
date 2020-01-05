"""this module contains serializers for worker_managment models"""

from rest_framework import serializers

from worker_managment.models import (
    Company, Manager, Work, Worker, Workplace, WorkTime)


class ManagerInCompanySerializer(serializers.HyperlinkedModelSerializer):
    """Special serializer for manager"""
    class Meta:
        model = Manager
        fields = ('id', 'name', 'url')


class WorkplaceInWorkSerializer(serializers.HyperlinkedModelSerializer):
    """Special serializer for workplace"""
    class Meta:
        model = Workplace
        fields = ('id', 'name', 'worker', 'url')


class WorkInCompanySerializer(serializers.HyperlinkedModelSerializer):
    """Special serializer for work"""
    workplaces = WorkplaceInWorkSerializer(many=True, read_only=True)

    class Meta:
        model = Work
        fields = ('id', 'name', 'workplaces', 'url')


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for company model"""
    managers = ManagerInCompanySerializer(many=True, read_only=True)
    works = WorkInCompanySerializer(many=True, read_only=False)

    class Meta:
        model = Company
        fields = ('id', 'name', 'managers', 'works')
        read_only_fields = ('id', 'managers')


class ManagerSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for manager model"""
    class Meta:
        model = Manager
        fields = ('id', 'name', 'company')


class WorkerSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for worker model"""
    class Meta:
        model = Worker
        fields = ('id', 'name', 'workplaces')


class WorkSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for work model"""
    class Meta:
        model = Work
        fields = ('id', 'name', 'company', 'workplaces')
        read_only_fields = ('id', 'workplaces')


class WorkplaceSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for workplace model"""
    class Meta:
        model = Workplace
        fields = ('id', 'name', 'work', 'worker')


class WorkTimeSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for worktime model"""
    class Meta:
        model = WorkTime
        fields = ('id', 'date_start', 'date_end',
                  'status', 'worker', 'workplace')
