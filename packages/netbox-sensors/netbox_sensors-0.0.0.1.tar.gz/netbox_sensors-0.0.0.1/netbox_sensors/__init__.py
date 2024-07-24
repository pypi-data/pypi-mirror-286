__author__ = """Óscar Hurtado"""
__email__ = "ohurtadp@sens.solutions"
__version__ = "0.0.0.1"

from extras.plugins import PluginConfig

from .constants import PLUGIN_APPLICATION_BASE_URL, PLUGIN_APPLICATION_NAME
from .version import __version__


class SensPlatformConfig(PluginConfig):
    name = "netbox_sensors"
    base_url = "netbox_sensors"
    verbose_name = "Netbox Sensors Plugin"
    description = "Sens Solutions Platform plugin"
    version = __version__
    author = "Sens Solutions development team"
    author_email = "mcollado@sens.solutions"
    required_settings = []
    default_settings = {}
    middleware = [
        "sens_platform.middleware.CustomDeviceRenderConfigMiddleware",
        "sens_platform.middleware.CustomAuthenticationMiddleware",
    ]
    template_extensions = []

    def ready(self):
        from . import signals

        super().ready()


config = SensPlatformConfig  # noqa
