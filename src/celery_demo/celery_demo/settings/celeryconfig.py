CELERY_BROKER_URL = 'redis://127.0.0.1'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1'

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TIMEZONE = 'UTC'
CELERY_ENABLE_UTC = True
CELERY_RESULT_EXPIRES = 360
CELERY_TASK_DEFAULT_QUEUE = 'default'
CELERY_TASK_ROUTES = {
    "tasks.datahandle.*": "datahandle",
    "tasks.datasource.*": "datasource",
    "tasks.notification.*": "notification"
}
CELERY_RESULT_EXTENDED = True
