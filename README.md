# Open Data & Data Ethics - Covid-19 Dashboard

## How to run

```cd``` into the project directory and run:

```bash
docker build -f Dockerfile .
```

and then run:

```bash
docker-compose up
```

And navigate to http://0.0.0.0:8000/.

See also:
- https://docs.docker.com/compose/django/

## Troubleshooting

If you get the message ```DisallowedHost at /``` or similar then add your domain to ```core/settings.py```:

```python
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.technikum-wien.at', 'your-new-domain']
```

## Credits

- Bootstrap https://getbootstrap.com/
- Bootstrap Admin  
- Python https://www.python.org/
- Django https://www.djangoproject.com/
- Plotly https://plotly.com/python/
- Appseed (Template generator): https://appseed.us/
- Argon Template: https://appseed.us/admin-dashboards/django-dashboard-argon
