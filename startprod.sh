# Starting production servers...
uv run manage.py purgerequests 1 months

uv run gunicorn mysite.wsgi:application
