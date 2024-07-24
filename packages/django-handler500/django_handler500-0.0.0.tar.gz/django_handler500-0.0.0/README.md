### Installation
```bash
$ pip install django-handler500
```

### Features
+   `django.views.debug.technical_500_response` if `request.user.is_superuser`
+   `django.views.defaults.server_error` default

### Examples
`urls.py`
```python
handler500 = "django_handler500.handler500"
```

