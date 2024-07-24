import json
import logging
from typing import Dict, Tuple

import maya
from dcim.models.devices import Device
from dcim.models.sites import Site
from django.contrib.auth.models import Group, User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from netbox.api.viewsets import NetBoxModelViewSet
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.routers import APIRootView
from rest_framework.views import APIView
from sens_platform.models import (
    AttributeMapping,
    Sensor,
    SensorType,
    Transducer,
    TransducerType,
    UserProfile,
)

from .modules.module import FactoryModule
from .serializers import (
    AttributeMappingSerializer,
    GroupSerializer,
    SensorSerializer,
    SensorTypeSerializer,
    TransducerSerializer,
    TransducerTypeSerializer,
    UserProfileSerializer,
    UserSerializer,
)

DEFAULT_TIME_RANGE = maya.timedelta(hours=12)


class SensPlatformRootView(APIRootView):
    """
    Sens API root view
    """

    def get_view_name(self):
        return "Sens platform API"


def get_time_range(pars: Dict, default_delta: int = DEFAULT_TIME_RANGE) -> Tuple:
    """
    Calculate a time range based on the given parameters.

    Parameters
    ----------
    pars : dict
        A dictionary containing the parameters for the time range calculation.
    default_delta : int
        The default time range.

    Returns
    -------
    Tuple
        A tuple containing the calculated time range.

    Raises
    ------
    ValueError
        If the input parameters are not valid.

    Examples
    --------
    >>> pars = {"from": "2023-10-01T00:00:00Z", "to": "2023-10-10T00:00:00Z"}
    >>> get_time_range(pars, 5)
    (datetime.datetime(2023, 10, 1, 0, 0), datetime.datetime(2023, 10, 10, 0, 0))
    """
    if "to" in pars:
        _to = maya.parse(pars["to"])
        _from = maya.parse(pars["from"]) if "from" in pars else (_to - default_delta)
    elif "from" in pars:
        _from = maya.parse(pars["from"])
        _to = maya.parse(pars["to"]) if "to" in pars else (_from + default_delta)
    else:
        _to = maya.now()
        _from = _to - default_delta
    return (_from.datetime(), _to.datetime())


def datetime_str(dt):
    # See "Date Time String Format" in the ECMA-262 specification.
    r = dt.isoformat()
    if dt.microsecond:
        r = r[:23] + r[26:]
    if r.endswith("+00:00"):
        r = r[:-6] + "Z"
    return r


class MultipleFieldLookupMixin(object):
    """
    Apply this mixin to any view or viewset to get multiple field filtering
    based on an `alternative_lookup_field` attribute, instead of the default
    single field filtering.
    """

    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            queryset = self.get_queryset()  # Get the base queryset
            queryset = self.filter_queryset(queryset)  # Apply any filter backends
            filter = {self.alternative_lookup_field: self.kwargs[self.lookup_field]}
            obj = get_object_or_404(queryset, **filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj


# class UserViewSet(MultipleFieldLookupMixin, viewsets.ReadOnlyModelViewSet):
#     """List of users."""
#
#     permission_classes = [IsAuthenticated]
#
#     queryset = UserProfile.objects.all().order_by("-date_joined")
#     serializer_class = UserSerializer
#     alternative_lookup_field = "username"
#
#     """
#     def filter_queryset(self, queryset):
#         user = self.request.user
#         if user.is_superuser or user.is_staff:
#             return queryset
#         elif user.userprofile.staff:
#             queryset = UserProfile.objects.filter(org=user.userprofile.org)
#             return User.objects.filter(id__in=queryset.values('user'))
#         else:
#             return queryset.filter(username=user.username)
#
#     """
#
#     def retrieve(self, request, pk=None):
#         """Detailed user information by id or username (swagger only allows ID)"""
#         return super().retrieve(request, pk=pk)


class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """List of user profiles"""

    permission_classes = [IsAuthenticated]

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    @action(methods=["POST"], detail=True, url_path="web-config")
    def set_web_config(self, request, pk=None):
        """Set user web preferences (usage by web application only)"""
        qs = self.get_queryset()
        profile = qs.get(user_id=pk)
        profile.web_config = json.dumps(request.data)
        profile.save()
        return HttpResponse()

    def filter_queryset(self, queryset):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return queryset
        elif user.userprofile.staff:
            return UserProfile.objects.filter(org=user.userprofile.org)
        else:
            return queryset.filter(user=user)

    def retrieve(self, request, *args, **kwargs):
        """Detailed user profile information"""
        return super().retrieve(request, *args, **kwargs)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """List of groups"""

    permission_classes = [IsAuthenticated]

    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def filter_queryset(self, queryset):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return queryset
        return queryset.none()


class SensorTypeViewSet(NetBoxModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = SensorType.objects.prefetch_related("tags").annotate(
        nb_sensors=Count("sensor_type")
    )
    serializer_class = SensorTypeSerializer


class SensorViewSet(NetBoxModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = Sensor.objects.prefetch_related("tags")
    serializer_class = SensorSerializer

    def get_queryset(self):
        """Grouping request filters."""
        sensors: object = None
        slug = self.request.query_params.get("site")
        if slug and slug != "undefined":
            site_id = Site.objects.get(slug=slug).id
            devices = Device.objects.filter(site_id=site_id)
            devices = [device.id for device in devices]
            sensors = Sensor.objects.filter(device_id__in=devices)
        else:
            sensors = []
        return sensors

    @action(detail=True)
    def values(self, request, pk):
        sensor = self.get_object()
        serializer = self.get_serializer(sensor, many=False)
        trange = get_time_range(request.query_params)
        reply = {
            "sensor": serializer.data,
            "from": trange[0],
            "to": trange[1],
            "stats": {},
            "data": [],
        }
        return Response(reply)


class TransducerTypeViewSet(NetBoxModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = TransducerType.objects.prefetch_related("tags").annotate(
        nb_transducer=Count("transducer_type")
    )
    serializer_class = TransducerTypeSerializer

    def get_queryset(self):
        """Grouping request filters."""
        transducer_type: object = None
        slug = self.request.query_params.get("site")
        sensor_id = self.request.query_params.get("sensor_id")
        if slug:
            site_id = Site.objects.get(slug=slug).id
            devices = Device.objects.filter(site_id=site_id)
            devices = [device.id for device in devices]
            sensors = Sensor.objects.filter(device_id__in=devices)
            sensor_types = [sensor.type_id for sensor in sensors]
            transducer_type = TransducerType.objects.filter(
                sensor_type_id__in=sensor_types
            )
        elif sensor_id:
            sensors = Sensor.objects.filter(id=sensor_id)
            type_ids = [sensor.type_id for sensor in sensors]
            transducer_type = TransducerType.objects.filter(sensor_type_id__in=type_ids)
        return transducer_type


class AttributeMappingViewSet(NetBoxModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = Sensor.objects.prefetch_related("tags")
    serializer_class = AttributeMappingSerializer


class TransducerViewSet(NetBoxModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = Transducer.objects.prefetch_related("tags")
    serializer_class = TransducerSerializer

    def get_queryset(self):
        """Grouping request filters."""
        transducers: object = None
        slug = self.request.query_params.get("site")
        sensor_id = self.request.query_params.get("sensor_id")
        if slug:
            site_id = Site.objects.get(slug=slug).id
            devices = Device.objects.filter(site_id=site_id)
            devices = [device.id for device in devices]
            sensors = Sensor.objects.filter(device_id__in=devices)
            sensors = [sensor.id for sensor in sensors]
            transducers = Transducer.objects.filter(sensor_id__in=sensors).distinct()
        elif sensor_id:
            transducers = Transducer.objects.filter(sensor_id=sensor_id).distinct()
        return transducers


class ModulesView(APIView):
    """Endpoint for the request of modules according to the configuration received."""

    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        try:
            name_module = request.data["name"]
            settings = request.data["settings"]
            factory = FactoryModule(name=name_module, settings=settings)
            structure = factory.build_module()
            return Response({name_module: structure})
        except Exception as ex:
            logger = logging.getLogger("netbox.sens_platform")
            logger.error(f"There ir no data. Detail: {ex}")
            return Response(
                {
                    "status": "error",
                    "error_details": f"{ex}",
                }
            )


class SiteUtilities(APIView):
    """
    An API endpoint through which rmq2sql can obtain a slug-organization.
    """

    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        try:
            dev_id = request.data["dev_id"]
            slug = Site.objects.get(id=Device.objects.get(id=dev_id).site_id).slug
            return Response({"slug": slug})
        except ObjectDoesNotExist as err:
            return Response(status=400, data={"error": err})
        except Exception as ex:
            return Response(status=400, data={"error": "Método no permitido"})


class CustomUpdateSensorSerialsView(APIView):
    """
    View for updating serial numbers of the different sensors that are
    part of a device.
    """

    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, *args, **kwargs) -> HttpResponse:
        try:
            serial_numbers = request.data

            if "dev_serial_num" not in serial_numbers:
                return Response(status=400, data={"error": "Solicitud incorrecta."})

            dev_serial_num = serial_numbers["dev_serial_num"]

            sensors = Sensor.objects.filter(device__serial=dev_serial_num)
            for sensor in sensors:
                if sensor.name in ["ULPSMCO", "ULPSMO3"]:
                    continue
                if sensor.name in serial_numbers["payload"]:
                    sn = serial_numbers["payload"][sensor.name]["serial_num"]
                    sensor.serial = sn
                    sensor.save()
            response = HttpResponse(status=200, content_type="application/json")
            return response
        except Exception as ex:
            return Response(status=400, data={"error": "Método no permitido"})
