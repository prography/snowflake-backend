FROM 333636352495.dkr.ecr.ap-northeast-2.amazonaws.com/snowflake_base:latest
WORKDIR /app
RUN python manage.py collectstatic --noinput
EXPOSE 80
CMD ["gunicorn", "--bind", "80:8000", "--workers", "2", "--threads", "2","snowflake.wsgi:application"]
