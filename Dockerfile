FROM snowflake_base:latest
WORKDIR /app
RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "--threads", "2","snowflake.wsgi:application"]
