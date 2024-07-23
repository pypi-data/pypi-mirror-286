# django-htmx-modal-redirect

`django-htmx-modal-redirect` is a Django middleware that seamlessly handles direct access to URLs intended for HTMX modal views. It ensures a smooth user experience by automatically opening the modal content when a user directly visits a URL meant to be displayed in a modal.

## Features

- Automatically detects non-HTMX requests to modal views
- Renders a fallback view (e.g., your main page) with injected HTMX code
- Triggers the modal to open automatically after the page loads
- Easy to configure and integrate into existing Django projects

## Installation

Install the package using pip:

```bash
pip install django-htmx-modal-redirect
```

## Configuration

1. Add `'htmx_modal_redirect.middleware.HTMXModalRedirectMiddleware'` to your `MIDDLEWARE` setting in `settings.py`:

```python
MIDDLEWARE = [
    # ...
    'django_htmx_modal_redirect.middleware.HTMXModalRedirectMiddleware',
    # ...
]
```

2. Configure the required settings in your `settings.py`:

```python
# List of URL names that should be treated as modal views
MODAL_VIEWS = ['user_profile', 'item_details']

# Path to the view function to be used for redirection (fallback view)
MODAL_REDIRECT_VIEW = 'myapp.views.home_page'
```

## How it works

1. When a user directly accesses a URL that's meant to be displayed in a modal (as defined in `MODAL_VIEWS`):
   - The middleware intercepts the request
   - It renders the fallback view specified in `MODAL_REDIRECT_VIEW`
   - It injects HTMX code to automatically trigger the modal

2. For HTMX requests or non-modal views, the middleware does nothing, allowing normal request handling.

## Example

Let's say you have a modal view for user profiles:

```python
# urls.py
urlpatterns = [
    path('user/<int:user_id>/', views.user_profile, name='user_profile'),
    # ...
]

# settings.py
MODAL_VIEWS = ['user_profile']
MODAL_REDIRECT_VIEW = 'myapp.views.home_page'
```

Now, if a user visits `/user/123/` directly:
1. The middleware detects this is a modal view
2. It renders the `home_page` view
3. It injects HTMX code to automatically open the user profile modal

The user sees the home page briefly before the modal with the user profile opens automatically.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.