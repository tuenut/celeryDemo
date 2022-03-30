broker_url = 'redis://localhost'
result_backend = 'redis://localhost'

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'UTC'
enable_utc = True
result_expires = 360
task_default_queue = 'default'
task_routes = {
    "tasks.datahandle.*": "datahandle",
    "tasks.datasource.*": "datasource",
    "tasks.notification.*": "notification"
}
