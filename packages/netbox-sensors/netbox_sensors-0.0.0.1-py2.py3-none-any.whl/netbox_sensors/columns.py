from dataclasses import dataclass
from typing import Dict, Optional
from urllib.parse import quote

import django_tables2 as tables
from django.template import Context, Template
from django.urls import reverse
from django.utils.safestring import mark_safe

# from utilities.utils import get_viewname
from utilities.views import get_viewname


@dataclass
class ActionsItem:
    title: str
    icon: str
    permission: Optional[str] = None
    css_class: Optional[str] = "secondary"


class CustomActionsColumn(tables.Column):
    """
    A dropdown menu which provides edit, delete, and changelog links for
    an object. Can optionally include additional buttons rendered from
    a template string.

    :param actions: The ordered list of dropdown menu items to include
    :param extra_buttons: A Django template string which renders
        additional buttons preceding the actions dropdown
    :param split_actions: When True, converts the actions dropdown
        menu into a split button with first action as the
        direct button link and icon (default: True)
    """

    attrs = {"td": {"class": "text-end text-nowrap noprint"}}
    empty_values = ()
    _actions: Dict = {
        "edit": ActionsItem("Edit", "pencil", "change", "warning"),
        "delete": ActionsItem("Delete", "trash-can-outline", "delete", "danger"),
        "template": ActionsItem("Download template", "download", "delete", "danger"),
        "duplicate": ActionsItem("Duplicate", "plus", "delete", "danger"),
    }
    _url_actions: Dict = {
        "template": "/plugins/sens-platform/custom-devices-download-template/",
        "duplicate": "/plugins/sens-platform/custom-devices-duplicate/",
        "delete": "/plugins/sens-platform/custom-devices-delete/",
    }

    def __init__(
        self,
        *args,
        actions=(
            "edit",
            "delete",
            "template",
            "duplicate",
        ),
        extra_buttons="",
        split_actions=True,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.extra_buttons = extra_buttons
        self.split_actions = split_actions

        # Determine which actions to enable
        self._actions = {name: self._actions[name] for name in actions}

    def header(self):
        return ""

    def render(self, record, table, **kwargs):
        # Skip dummy records (e.g. available VLANs) or those with no actions
        if not getattr(record, "pk", None) or not self._actions:
            return ""

        model = table.Meta.model
        request = getattr(table, "context", {}).get("request")
        url_appendix = (
            f"?return_url={quote(request.get_full_path())}" if request else ""
        )
        html = ""

        # Compile actions menu
        button = None
        dropdown_class = "secondary"
        dropdown_links = []

        for idx, (action, attrs) in enumerate(self._actions.items()):
            if action in ["template", "duplicate", "delete"]:
                url_appendix += f"&pk={record.pk}"
                url = f"{self._url_actions[action]}"
            else:
                url = reverse(get_viewname(model, action), kwargs={"pk": record.pk})
            # Render a separate button if a) only one action exists, or
            # b) if split_actions is True
            if len(self._actions) == 1 or (self.split_actions and idx == 0):
                dropdown_class = attrs.css_class
                button = (
                    f'<a class="btn btn-sm btn-{attrs.css_class}" '
                    f'href="{url}{url_appendix}" type="button">'
                    f'<i class="mdi mdi-{attrs.icon}"></i></a>'
                )

            # Add dropdown menu items
            else:
                dropdown_links.append(
                    f'<li><a class="dropdown-item" href="{url}{url_appendix}">'
                    f'<i class="mdi mdi-{attrs.icon}"></i> {attrs.title}</a></li>'
                )

        # Create the actions dropdown menu
        if button and dropdown_links:
            html += (
                f'<span class="btn-group dropdown">'
                f"  {button}"
                f'  <a class="btn btn-sm btn-{dropdown_class} dropdown-toggle" type="button" '
                f'data-bs-toggle="dropdown" style="padding-left: 2px">'
                f'  <span class="visually-hidden">Toggle Dropdown</span></a>'
                f'  <ul class="dropdown-menu">{"".join(dropdown_links)}</ul>'
                f"</span>"
            )
        elif button:
            html += button
        elif dropdown_links:
            html += (
                f'<span class="btn-group dropdown">'
                f'  <a class="btn btn-sm btn-secondary dropdown-toggle" type="button" '
                f'data-bs-toggle="dropdown">'
                f'  <span class="visually-hidden">Toggle Dropdown</span></a>'
                f'  <ul class="dropdown-menu">{"".join(dropdown_links)}</ul>'
                f"</span>"
            )

        # Render any extra buttons from template code
        if self.extra_buttons:
            template = Template(self.extra_buttons)
            context = getattr(table, "context", Context())
            context.update({"record": record})
            html = template.render(context) + html

        # Issue B703: mark_safe is required to render HTML tags
        return mark_safe(html)
