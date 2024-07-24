from extras.plugins import PluginMenuButton, PluginMenuItem
from sens_platform.utils.utils import link
from utilities.choices import ButtonColorChoices

sensor_type_buttons = [
    PluginMenuButton(
        title="Add",
        link=link("sensortype_add"),
        icon_class="mdi mdi-plus-thick",
        color=ButtonColorChoices.GREEN,
    ),
    PluginMenuButton(
        title="Import",
        link=link("sensortype_import"),
        icon_class="mdi mdi-upload",
        color=ButtonColorChoices.CYAN,
    ),
]

sensor_buttons = [
    PluginMenuButton(
        title="Add",
        link=link("sensor_add"),
        icon_class="mdi mdi-plus-thick",
        color=ButtonColorChoices.GREEN,
    ),
    PluginMenuButton(
        title="Import",
        link=link("sensor_import"),
        icon_class="mdi mdi-upload",
        color=ButtonColorChoices.CYAN,
    ),
]

transducer_type_buttons = [
    PluginMenuButton(
        title="Add",
        link=link("transducertype_add"),
        icon_class="mdi mdi-plus-thick",
        color=ButtonColorChoices.GREEN,
    ),
    PluginMenuButton(
        title="Import",
        link=link("transducertype_import"),
        icon_class="mdi mdi-upload",
        color=ButtonColorChoices.CYAN,
    ),
]

transducer_buttons = [
    PluginMenuButton(
        title="Add",
        link=link("transducer_add"),
        icon_class="mdi mdi-plus-thick",
        color=ButtonColorChoices.GREEN,
    ),
    PluginMenuButton(
        title="Import",
        link=link("transducer_import"),
        icon_class="mdi mdi-upload",
        color=ButtonColorChoices.CYAN,
    ),
]

attribute_mapping_buttons = [
    PluginMenuButton(
        title="Add",
        link=link("attributemapping_add"),
        icon_class="mdi mdi-plus-thick",
        color=ButtonColorChoices.GREEN,
    ),
]

menu_items = (
    PluginMenuItem(
        link=link("custom_devices_list"),
        link_text="Device Tools",
    ),
    PluginMenuItem(
        link=link("sensortype_list"),
        link_text="Sensor types",
        buttons=sensor_type_buttons,
    ),
    PluginMenuItem(
        link=link("sensor_list"),
        link_text="Sensors",
        buttons=sensor_buttons,
    ),
    PluginMenuItem(
        link=link("transducertype_list"),
        link_text="Transducer types",
        buttons=transducer_type_buttons,
    ),
    PluginMenuItem(
        link=link("transducer_list"),
        link_text="Transducer",
        buttons=transducer_buttons,
    ),
    PluginMenuItem(
        link=link("attributemapping_list"),
        link_text="Attribute mapping",
        buttons=attribute_mapping_buttons,
    ),
)
