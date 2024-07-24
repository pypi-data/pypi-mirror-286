from django.urls import include, path
from netbox.api.routers import NetBoxRouter

from . import views

router = NetBoxRouter()
router.APIRootView = views.SensPlatformRootView

# router.register("users", views.UserViewSet)
router.register("profiles", views.UserProfileViewSet)
router.register("sensors", views.SensorViewSet)
router.register("sensor-types", views.SensorTypeViewSet)
router.register("transducer", views.TransducerViewSet)
router.register("transducer-types", views.TransducerTypeViewSet)
router.register(
    "attribute-mapping", views.AttributeMappingViewSet, basename="attribute_mapping"
)

app_name = "sens_platform"
urlpatterns = [
    path("site-utilities/", views.SiteUtilities.as_view(), name="site-utilities"),
    path("modules/", views.ModulesView.as_view(), name="modules"),
    path(
        "custom-update-sensor-serial/",
        views.CustomUpdateSensorSerialsView.as_view(),
        name="custom_update_sensor_serial",
    ),
    path("", include(router.urls)),
]
