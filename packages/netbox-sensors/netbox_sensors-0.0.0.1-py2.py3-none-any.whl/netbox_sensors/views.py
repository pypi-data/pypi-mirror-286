import json
import time
import traceback

from dcim.models.devices import Device
from dcim.views import DeviceRenderConfigView
from django.contrib import messages
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _
from django.views import View
from jinja2.exceptions import TemplateError
from netbox.views import generic
from sens_platform.utils.utils import clone_models
from utilities.views import ViewTab, register_model_view

from .constants import DEVICE_SCHEMATIC
from .filters import (
    AttributeMappingFilterSet,
    DeviceToolFilterSet,
    SensorFilterSet,
    SensorTypeFilterSet,
    TransducerFilterSet,
    TransducerTypeFilterSet,
)
from .forms import (
    AttributeMappingForm,
    SensorForm,
    SensorImportForm,
    SensorTypeForm,
    SensorTypeImportForm,
    TransducerForm,
    TransducerImportForm,
    TransducerTypeForm,
    TransducerTypeImportForm,
)
from .models import AttributeMapping, Sensor, SensorType, Transducer, TransducerType
from .tables import (
    AttributeMappingTable,
    CustomDevicesTable,
    SensorTable,
    SensorTypeTable,
    TransducerTable,
    TransducerTypeTable,
)


class SensorTypeView(generic.ObjectView):
    queryset = SensorType.objects.all()

    def get_extra_context(self, request, instance):
        table = SensorTable(instance.sensor_type.all())
        table.configure(request)

        transducer_type_table = TransducerTypeTable(
            instance.transducer_sensor_type.all()
        )

        return {"sensors_table": table, "transducer_type_table": transducer_type_table}


class SensorTypeListView(generic.ObjectListView):
    queryset = SensorType.objects.annotate(nb_sensors=Count("sensor_type"))
    filterset = SensorTypeFilterSet
    table = SensorTypeTable


class SensorTypeEditView(generic.ObjectEditView):
    queryset = SensorType.objects.all()
    form = SensorTypeForm


class SensorTypeBulkImportView(generic.BulkImportView):
    queryset = SensorType.objects.all()
    model_form = SensorTypeImportForm


class SensorTypeDeleteView(generic.ObjectDeleteView):
    queryset = SensorType.objects.all()


class SensorView(generic.ObjectView):
    queryset = Sensor.objects.all()

    def get_extra_context(self, request, instance):
        sensor_types_table = SensorTypeTable(instance.type.all())
        table = TransducerTable(instance.sensor.all())
        table.configure(request)

        return {"transducer_table": table, "sensor_types_table": sensor_types_table}


class SensorListView(generic.ObjectListView):
    queryset = Sensor.objects.all()
    filterset = SensorFilterSet
    table = SensorTable
    actions = ("add", "import", "export", "bulk_delete")


class SensorEditView(generic.ObjectEditView):
    queryset = Sensor.objects.all()
    form = SensorForm


class SensorBulkDeleteView(generic.BulkDeleteView):
    queryset = Sensor.objects.all()
    filterset = SensorFilterSet
    table = SensorTable


class SensorDeleteView(generic.ObjectDeleteView):
    queryset = Sensor.objects.all()


class TransducerTypeView(generic.ObjectView):
    queryset = TransducerType.objects.all()

    def get_extra_context(self, request, instance):
        table = TransducerTable(instance.transducer_type.all())
        table.configure(request)

        return {
            "transducers": table,
        }


class TransducerTypeListView(generic.ObjectListView):
    queryset = TransducerType.objects.all()
    filterset = TransducerTypeFilterSet
    table = TransducerTypeTable


class TransducerTypeEditView(generic.ObjectEditView):
    queryset = TransducerType.objects.all()
    form = TransducerTypeForm


class TransducerTypeDeleteView(generic.ObjectDeleteView):
    queryset = TransducerType.objects.all()


class TransducerView(generic.ObjectView):
    queryset = Transducer.objects.all()


class AttributeMappingView(generic.ObjectView):
    queryset = AttributeMapping.objects.all()


class TransducerListView(generic.ObjectListView):
    queryset = Transducer.objects.all()
    filterset = TransducerFilterSet
    table = TransducerTable
    actions = ("add", "import", "export", "bulk_delete")


class AttributeMappingListView(generic.ObjectListView):
    queryset = AttributeMapping.objects.all()
    filterset = AttributeMappingFilterSet
    table = AttributeMappingTable
    actions = ("add",)


class TransducerEditView(generic.ObjectEditView):
    queryset = Transducer.objects.all()
    form = TransducerForm


class AttributeMappingEditView(generic.ObjectEditView):
    queryset = AttributeMapping.objects.all()
    form = AttributeMappingForm


class TransducerDeleteView(generic.ObjectDeleteView):
    queryset = Transducer.objects.all()


class AttributeMappingDeleteView(generic.ObjectDeleteView):
    queryset = AttributeMapping.objects.all()


class TransducerBulkDeleteView(generic.BulkDeleteView):
    queryset = Transducer.objects.all()
    filterset = TransducerFilterSet
    table = TransducerTable


class TransducerTypeBulkImportView(generic.BulkImportView):
    queryset = TransducerType.objects.all()
    model_form = TransducerTypeImportForm


class TransducerBulkImportView(generic.BulkImportView):
    queryset = Transducer.objects.all()
    model_form = TransducerImportForm


class SensorBulkImportView(generic.BulkImportView):
    queryset = Sensor.objects.all()
    model_form = SensorImportForm


class CustomDevicesListView(generic.ObjectListView):
    queryset = Device.objects.all()
    filterset = DeviceToolFilterSet
    table = CustomDevicesTable
    actions = ("bulk_delete",)


class CustomActionView(View):
    @staticmethod
    def get(request, *args, **kwargs) -> HttpResponse:
        response_data = {"message": "Request processed correctly."}
        return JsonResponse(response_data)


class CustomDevicesDownloadTemplateView(View):
    """
    View to download templates (json type) of a Device with all its sensors, with
    message format for rabbitmq.
    """

    @staticmethod
    def _functionality_support(device: object) -> object:
        try:
            DEVICE_SCHEMATIC["payload"] = {}
            DEVICE_SCHEMATIC["name"] = device.name
            DEVICE_SCHEMATIC["dev_id"] = device.id
            DEVICE_SCHEMATIC["serial"] = device.serial
            DEVICE_SCHEMATIC["ts"] = time.strftime(
                "%Y-%m-%d %H:%M:%S %z", time.localtime(time.time())
            )
            DEVICE_SCHEMATIC["type"] = 1
            DEVICE_SCHEMATIC["type_version"] = 1
            DEVICE_SCHEMATIC["slug"] = device.site.slug

            servers = device.get_config_context()
            if "broker-servers" in list(servers):
                DEVICE_SCHEMATIC["broker-servers"] = servers["broker-servers"]
            else:
                DEVICE_SCHEMATIC["broker-servers"] = []

            if "dns-servers" in list(servers):
                DEVICE_SCHEMATIC["dns-servers"] = servers["dns-servers"]
            else:
                DEVICE_SCHEMATIC["dns-servers"] = []

            if "ntp_servers" in list(servers):
                DEVICE_SCHEMATIC["ntp_servers"] = servers["ntp_servers"]
            else:
                DEVICE_SCHEMATIC["ntp_servers"] = []

            sensors = Sensor.objects.filter(device_id=device.id)

            for sensor in sensors:
                sensor_schematic = {sensor.name: {"sensor_id": sensor.id}}
                if sensor.sensitivity_code:
                    sensor_schematic[sensor.name].update(
                        {"sc": float(sensor.sensitivity_code)}
                    )
                transducers = Transducer.objects.filter(sensor_id=sensor.id)
                for transducer in transducers:
                    sensor_schematic[sensor.name].update({transducer.name: 0})
                DEVICE_SCHEMATIC["payload"].update(sensor_schematic)
            json_data = json.dumps(DEVICE_SCHEMATIC, indent=4)
            return json_data
        except Exception as ex:
            response_data = {"error": f"{ex}"}
            return JsonResponse(response_data, status=400)

    def get(self, request, *args, **kwargs) -> HttpResponse:
        # if not request.user.is_superuser:
        #     return HttpResponse("Forbidden", status=403)

        try:
            device: object
            rendered_config = None
            device_id = request.GET.get("pk", None)
            serial = request.GET.get("serial", None)
            application_date = time.strftime(
                "%Y-%m-%d %H:%M:%S %z", time.localtime(time.time())
            )
            if device_id is None and serial:
                device = Device.objects.get(serial=serial)
            elif device_id and serial is None:
                device = Device.objects.get(id=device_id)
            else:
                response_data = {
                    "error": "One of the two parameters is mandatory: device id (device_id) "
                    "or serial number (serial)"
                }
                return JsonResponse(response_data, status=400)

            if device.config_template is None:
                rendered_config = self._functionality_support(device=device)
            else:
                context_data = device.get_config_context()
                context_data.update({"device": device})
                sensors = Sensor.objects.filter(device=device)
                context_data.update({"sensors": sensors})
                if config_template := device.get_config_template():
                    try:
                        rendered_config = config_template.render(context=context_data)
                        rendered_config = json.loads(rendered_config)
                        rendered_config["ts"] = time.strftime(
                            "%Y-%m-%d %H:%M:%S %z", time.localtime(time.time())
                        )
                        rendered_config = json.dumps(rendered_config)
                    except TemplateError as e:
                        messages.error(
                            request,
                            f"An error occurred while rendering the template: {e}",
                        )
                        rendered_config = traceback.format_exc()
            response = HttpResponse(
                json.loads(json.dumps(rendered_config, indent=4)),
                content_type="application/json",
            )
            response["Content-Disposition"] = (
                f"attachment; filename={device.site.slug}_{device.name}_"
                f"{application_date}.json"
            )
            return response
        except Exception as ex:
            response_data = {"error": f"{ex}"}
            return JsonResponse(response_data, status=400)


class CustomDeviceUpdatesView(View):
    """
    View created to extend actions on the Netbox "Device" model. To make
    modifications to the model from Sens Solutions services.
    """

    @staticmethod
    def get(request, *args, **kwargs) -> HttpResponse:
        if not request.user.is_superuser:
            return HttpResponse("Forbidden", status=403)

        device: object
        device_id = request.GET.get("pk", None)
        serial = request.GET.get("serial", None)
        if device_id is None or serial is None:
            response_data = {
                "error": "To update the 'Serial' it is mandatory to "
                "provide the 'ID' and 'Serial' of a device."
            }
            return JsonResponse(response_data, status=400)

        try:
            device = Device.objects.get(id=device_id)
            device.serial = serial
            device.save()
        except Exception as ex:
            response_data = {
                "error": "To update the 'Serial' it is mandatory to "
                "provide the 'ID' and 'Serial' of a device."
            }
            return JsonResponse(response_data, status=400)
        response_data = {"message": "Request processed correctly."}
        return JsonResponse(response_data)


class CustomDevicesDuplicateView(View):
    """View to duplicate a Device with all its sensors and transducers."""

    def get(self, request, *args, **kwargs) -> None:
        if not request.user.is_superuser:
            return HttpResponse("Forbidden", status=403)

        device_id = request.GET["pk"]
        device = Device.objects.get(id=device_id)
        device_cloned = clone_models(
            model_name="device",
            instance=device,
            fields={
                "serial": f"CLONED-{time.time()}".replace(".", ""),
                "name": f"CLONED-{device.name}-{time.time()}".replace(".", ""),
            },
        )
        messages.success(
            request,
            _(
                f"Duplicate device, sensors and transducers. Device Name: {device_cloned.name}"
            ),
        )
        return redirect("/plugins/sens-platform/custom-devices-list/")


class CustomDevicesDeleteView(View):
    """View to duplicate a Device with all its sensors and transducers."""

    def get(self, request, *args, **kwargs) -> None:
        if not request.user.is_superuser:
            return HttpResponse("Forbidden", status=403)

        device_id = request.GET["pk"]
        device = Device.objects.get(id=device_id)
        name_device = device.name
        Transducer.objects.filter(sensor__device__id=device_id).delete()
        Sensor.objects.filter(device__id=device_id).delete()
        device.delete()
        messages.success(
            request,
            _(f"Delete device, sensors and transducers. Device Name: {name_device}"),
        )
        return redirect("/plugins/sens-platform/custom-devices-list/")


class CustomDeviceRenderConfigView(DeviceRenderConfigView):
    def get(self, request, **kwargs):
        instance = self.get_object(**kwargs)
        context = self.get_extra_context(request, instance)

        # If a direct export has been requested, return the rendered template content as a
        # downloadable file.
        if request.GET.get("export"):
            response = HttpResponse(context["rendered_config"], content_type="text")
            filename = f"{instance.name or 'config'}.txt"
            response["Content-Disposition"] = f'attachment; filename="{filename}"'
            return response

        # Add sensors to the context
        context["sensors"] = Sensor.objects.filter(device=instance)

        return render(
            request,
            self.get_template_name(),
            {
                "object": instance,
                "tab": self.tab,
                **context,
            },
        )

    def get_extra_context(self, request, instance):
        # Compile context data
        context_data = instance.get_config_context()
        context_data.update({"device": instance})
        sensors = Sensor.objects.filter(device=instance)
        context_data.update({"sensors": sensors})

        # Render the config template
        rendered_config = None
        if config_template := instance.get_config_template():
            try:
                rendered_config = config_template.render(context=context_data)
            except TemplateError as e:
                messages.error(
                    request, f"An error occurred while rendering the template: {e}"
                )
                rendered_config = traceback.format_exc()

        return {
            "config_template": config_template,
            "context_data": context_data,
            "rendered_config": rendered_config,
        }


@register_model_view(Device, "device-sensors")
class DeviceSensorsView(generic.ObjectView):
    queryset = Device.objects.all()
    template_name = "sens_platform/sensors_per_device.html"
    tab = ViewTab(
        label=_("Sensors"),
        badge=lambda obj: Sensor.objects.filter(device=obj).count(),
        weight=2100,
        permission="dcim.view_sensorsperdevice",
        hide_if_empty=True,
    )

    def get_object(self, **kwargs):
        # Get the original object
        device = super().get_object(**kwargs)

        # Return the object as a Device
        return Device.objects.get(pk=device.pk)

    def get_extra_context(self, request, instance):
        # Compile context data
        sensors = Sensor.objects.filter(device=self.kwargs["pk"])
        for sensor in sensors:
            sensor.transducers = Transducer.objects.filter(sensor=sensor)
        return {"sensors": sensors, "device": instance}
