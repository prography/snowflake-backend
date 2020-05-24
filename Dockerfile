FROM 333636352495.dkr.ecr.ap-northeast-2.amazonaws.com/snowflake_base_v2:latest
WORKDIR /app
COPY . /app/
RUN rm -rf /app/snowflake/static && mkdir /app/snowflake/static
# supervisor setting
RUN python manage.py collectstatic --noinput

# setup all the configfiles
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

COPY deployment/nginx-snowflake.conf /etc/nginx/sites-available/default
COPY deployment/supervisord.conf /etc/supervisor/

EXPOSE 80
CMD ["supervisord", "-n"]