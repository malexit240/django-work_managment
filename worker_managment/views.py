"""this module contains views(mostly viewsets) for API"""

import json

from django.http import HttpRequest

from rest_framework import (viewsets, status, permissions)
from rest_framework.decorators import action
from rest_framework.response import Response

from worker_managment.models import (
    Company, Manager, Work, Worker, Workplace, WorkTime)
from worker_managment.serializers import (
    CompanySerializer, ManagerSerializer, WorkSerializer, WorkerSerializer, WorkplaceSerializer, WorkTimeSerializer)
from worker_managment.api_permissions import (IsManager,)


class CompanyViewSet(viewsets.ModelViewSet):
    """ViewSet for company"""
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    permission_classes = (IsManager,)

    @action(detail=True, methods=('post',))
    def add_manager(self, request: HttpRequest, pk):
        json_data = json.loads(request.body.decode('utf-8'))
        if not json_data['pk']:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if Manager.objects.filter(pk=json_data['pk']).exists():
            Manager.objects.filter(pk=json_data['pk']).update(company_id=pk)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ManagerViewSet(viewsets.ModelViewSet):
    """ViewSet for manager"""
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer

    permission_classes = (IsManager,)


class WorkViewSet(viewsets.ModelViewSet):
    """ViewSet for work"""
    queryset = Work.objects.all()
    serializer_class = WorkSerializer

    permission_classes = (IsManager,)


class WorkerViewSet(viewsets.ModelViewSet):
    """ViewSet for worker"""
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer

    permission_classes = (permissions.IsAuthenticated,)


class WorkplaceViewSet(viewsets.ModelViewSet):
    """ViewSet for workplace"""
    queryset = Workplace.objects.all()
    serializer_class = WorkplaceSerializer

    permission_classes = (IsManager,)


class WorkTimeViewSet(viewsets.ModelViewSet):
    """ViewSet for worktime"""
    queryset = WorkTime.objects.all()
    serializer_class = WorkTimeSerializer

    permission_classes = (IsManager,)
