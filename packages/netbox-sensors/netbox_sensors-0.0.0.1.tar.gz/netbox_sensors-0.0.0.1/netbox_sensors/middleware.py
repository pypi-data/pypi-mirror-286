import re

from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import resolve, reverse


class CustomDeviceRenderConfigMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/dcim/devices/") and request.path.endswith(
            "/render-config/"
        ):
            # Extract the pk from the current path
            match = re.search(r"/dcim/devices/(\d+)/render-config/$", request.path)
            if match:
                pk = match.group(1)
                new_path = f"/plugins/sens-platform/device-render-config/{pk}/"
                # Avoid cyclic redirection
                if request.path != new_path:
                    return HttpResponseRedirect(new_path)
        return self.get_response(request)


class CustomAuthenticationMiddleware:
    """
    Listening for the Home load to verify if the user is registered, if not
    registered, it is redirected to login.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        url_is_home = resolve(request.path_info).url_name == "home"
        if url_is_home and not request.user.is_authenticated:
            return redirect("login")
        return self.get_response(request)
