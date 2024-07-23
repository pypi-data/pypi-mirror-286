from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.urls import resolve
from django.utils.module_loading import import_string
from django.utils.safestring import mark_safe


class HTMXModalRedirectMiddleware:
    """
    Handles non-HTMX requests to views that are meant to be displayed in a modal using HTMX.

    If a user directly visits a URL meant for a modal, this middleware renders the specified view
    with a hidden element that automatically opens the modal.

    Required settings:
    - MODAL_VIEWS: A list of URL names that should be treated as modal views.
    - MODAL_REDIRECT_VIEW: A string path to the view function to be used for redirection (e.g., 'app.views.index').
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.redirect_view = self._get_redirect_view()

    def _get_redirect_view(self):
        try:
            return import_string(settings.MODAL_REDIRECT_VIEW)

        except AttributeError as e:
            msg = "MODAL_REDIRECT_VIEW must be set in your Django settings. Example: MODAL_REDIRECT_VIEW = 'myapp.views.home_page'"  # noqa: E501
            raise ImproperlyConfigured(msg) from e

        except ImportError as e:
            msg = f"Could not import {settings.MODAL_REDIRECT_VIEW}. Make sure it's a valid path to a view function."
            raise ImproperlyConfigured(msg) from e

    def __call__(self, request):
        # Check if not an HTMX request and the current view is a modal view (i.e., meant to be displayed in a modal)
        is_modal_view = resolve(request.path_info).url_name in getattr(settings, "MODAL_VIEWS", [])
        if not request.htmx and is_modal_view:

            # Render the fallback view set in MODAL_REDIRECT_VIEW (e.g., 'app.views.index')
            response = self.redirect_view(request)

            # If the response is HTML, inject a loader element to trigger the modal
            if "text/html" in response.get("Content-Type", ""):

                # Create an element with hx-* attributes to request the original URL
                loader_html = f"""
                    <div hx-get="{request.get_full_path()}"
                         hx-trigger="load"
                         hx-target="body"
                         hx-swap="beforeend"
                         hx-push-url="/"
                         hx-on::after-request="this.remove()">
                    </div>
                """

                # Insert the element before the closing </body> tag
                response.content = response.content.decode("utf-8").replace(
                    "</body>",
                    f"{mark_safe(loader_html)}</body>",  # noqa: S308
                )

                # Update the Content-Length header
                response["Content-Length"] = len(response.content)

            # Return the response
            return response

        # For HTMX requests or non-modal views, proceed as normal
        return self.get_response(request)
