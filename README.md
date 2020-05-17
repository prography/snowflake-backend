# Development
### local 환경에서 test db 대상 실행
```
python manage.py runserver --settings=snowflake.settings.local
```
### local 환경에서 remote db 대상 실행
```
python manage.py runserver --settings=snowflake.settings.production
```