import datetime
from itertools import chain
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import views
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from . import models
from . import serializers


class OrganisationViewSet(viewsets.ModelViewSet):
    queryset = models.Organisations.objects.all()
    serializer_class = serializers.OrganisationsSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if not self.request.user.is_staff:
            self.queryset = models.Organisations.objects.filter(profiles=self.request.user.profile)
        return super().get_queryset()


class LocalisationViewSet(viewsets.ModelViewSet):
    queryset = models.Localisation.objects.all()
    serializer_class = serializers.LocalisationSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = ()

    def get_queryset(self):
        if not self.request.user.is_staff:
            private_localisations = self.queryset.filter(
                profile=self.request.user.profile
            )
            organisation_localisations = self.queryset.filter(
                organisation__profiles=self.request.user.profile
            )
            self.queryset = private_localisations | organisation_localisations
        return super().get_queryset()


    @action(detail=True, methods=['get'], permission_classes=(IsAuthenticated,))
    def consumption(self, request, *args, **kwargs):
        start_date = datetime.date.fromisoformat(request.query_params.get('start_date'))
        end_date = datetime.date.fromisoformat(request.query_params.get('end_date'))
        obj = self.get_object()
        return Response({
            'result': obj.get_consumption(start_date, end_date),
            'start_date': start_date,
            'end_date': end_date,
            'id': obj.id,
        }, status=HTTP_200_OK)

    @action(detail=True, methods=['get'], permission_classes=(IsAuthenticated,))
    def propositions(self):
        return Response(self.get_object().get_offers(), status=HTTP_200_OK)

class RoomViewSet(viewsets.ModelViewSet):
    queryset = models.Room.objects.all()
    serializer_class = serializers.RoomSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = ()

    def get_queryset(self):
        if not self.request.user.is_staff:
            private_localisations = self.queryset.filter(
                localisation__profile=self.request.user.profile
            )
            organisation_localisations = self.queryset.filter(
                localisation__organisation__profiles=self.request.user.profile
            )
            self.queryset = private_localisations | organisation_localisations
        return super().get_queryset()

    @action(detail=True, methods=['get'], permission_classes=(IsAuthenticated,))
    def consumption(self, request, *args, **kwargs):
        start_date = datetime.date.fromisoformat(request.query_params.get('start_date'))
        end_date = datetime.date.fromisoformat(request.query_params.get('end_date'))
        obj = self.get_object()
        return Response({
            'result': obj.get_consumption(start_date, end_date),
            'start_date': start_date,
            'end_date': end_date,
            'id': obj.id,
        }, status=HTTP_200_OK)

    @action(detail=True, methods=['get'], permission_classes=(IsAuthenticated,))
    def propositions(self):
        return Response(self.get_object().get_offers(), status=HTTP_200_OK)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = models.Group.objects.all()
    serializer_class = serializers.GroupSerializer
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods=['get'], permission_classes=(IsAuthenticated,))
    def consumption(self, request, *args, **kwargs):
        start_date = datetime.date.fromisoformat(request.query_params.get('start_date'))
        end_date = datetime.date.fromisoformat(request.query_params.get('end_date'))
        obj = self.get_object()
        return Response({
            'result': obj.get_consumption(start_date, end_date),
            'start_date': start_date,
            'end_date': end_date,
            'id': obj.id,
        }, status=HTTP_200_OK)

    def get_queryset(self):
        if not self.request.user.is_staff:
            private_localisations = self.queryset.filter(
                devices__localisation__localisation__profile=self.request.user.profile
            )
            organisation_localisations = self.queryset.filter(
                devices__localisation__localisation__organisation__profiles=self.request.user.profile
            )
            self.queryset = private_localisations | organisation_localisations
        return super().get_queryset()


class DeviceTypeViewSet(viewsets.ModelViewSet):
    queryset = models.DeviceType.objects.all()
    serializer_class = serializers.DeviceTypeSerializer
    permission_classes = (IsAdminUser,)


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = models.Device.objects.all()
    serializer_class = serializers.DeviceSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = ()

    def get_queryset(self):
        if not self.request.user.is_staff:
            private_localisations = self.queryset.filter(
                localisation__localisation__profile=self.request.user.profile
            )
            organisation_localisations = self.queryset.filter(
                localisation__localisation__organisation__profiles=self.request.user.profile
            )

            self.queryset = private_localisations | organisation_localisations
        return super().get_queryset()

    @action(detail=True, methods=['get'], permission_classes=(IsAuthenticated,))
    def consumption(self, request, *args, **kwargs):
        start_date = datetime.date.fromisoformat(request.query_params.get('start_date'))
        end_date = datetime.date.fromisoformat(request.query_params.get('end_date'))
        obj = self.get_object()
        return Response({
            'result': obj.get_consumption(start_date, end_date),
            'start_date': start_date,
            'end_date': end_date,
            'id': obj.id,
        }, status=HTTP_200_OK)

    @action(detail=True, methods=['get'], permission_classes=(IsAuthenticated,))
    def propositions(self):
        return Response(self.get_object().get_offer(), status=HTTP_200_OK)


class MonthViewSet(viewsets.ModelViewSet):
    queryset = models.Month.objects.all()
    serializer_class = serializers.MonthSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'date'
    filter_backends = ()

    def get_queryset(self):
        self.queryset = self.queryset.filter(device=self.kwargs['device_pk'])
        return super().get_queryset()



class DayViewSet(viewsets.ModelViewSet):
    queryset = models.Day.objects.all()
    serializer_class = serializers.DaySerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'date'
    filter_backends = ()

    def get_queryset(self):
        self.queryset = self.queryset.filter(month__device=self.kwargs['device_pk'])
        return super().get_queryset()


class SpecsFetchView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, url: str):
        return Response({
            "device_type": models.DeviceType.objects.get(name='fridge').pk,
            "consumption": 29,
            "energy_class": 'E',
            "device_name": 'Samsung RB34T652EBN',
        }, status=HTTP_200_OK)
