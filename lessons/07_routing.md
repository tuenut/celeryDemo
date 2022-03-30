## Routing Tasks

Celery has named queues. You can route some tasks to one queue, other to 
second queue. Name the queues according to their meaning.

For example in your app you have several classes of tasks divided by their 
purpose:
- **Data source**. Tasks which harvest some information, weather for example.
- **Data handle**. That tasks handling your data in background, compress images 
for example.
- **Notification**. That tasks send some notifications to your users.

You can create three queues `datasource`, `datahandling` and `notification` and
route your tasks to that queues. Then, when you start celery workers you can say 
from which queue who should take the tasks for each of them. If you have many 
users you may want to run many workers to handle `notification`-queue, one 
worker for `datasource`, cause you get weather not often and only from one 
source, and some workers for `datahandling`, cause users sometimes upload 
pictures to your service.

Also, you can start your workers for each queue on different servers to separate
load. We will demonstrate it with **docker-compose**.

First we make a few tasks for purposes described above.

- `tasks.datahandle.compressimage.compress_image` - task emulates image 
compression. Can randomly fail with `FileNotFound`.
- `tasks.datasource.weather.get_weather_today` - task emulates weather request. 
- `tasks.notification.slack.notify_user_in_slack` - task emulates send some 
notification for user.

Now we should use `celeryconfig.py` to configure tasks routing to queues with 
global pattern.

In next step we should write simple `Dockerfile`, where we use python:3.10-alpine 
as base image and install requirements in our new image. Then we will describe 
celery workers, which handles queues as docker-compose services in 
`docker-compose.yml`.

To run our services execute 
```shell
docker-compose up -d --remove-orphans
```
To see that the services are running, you need to execute `docker-compose ps` 
and you will see something like that:
```
                  Name                                 Command               State    Ports  
---------------------------------------------------------------------------------------------
celery_experiments_datahandle-workers_1     celery -A tasks worker --l ...   Up              
celery_experiments_datasource-workers_1     celery -A tasks worker --l ...   Up              
celery_experiments_default-queue_1          celery -A tasks worker --l ...   Up              
celery_experiments_notification-workers_1   celery -A tasks worker --l ...   Up              
celery_experiments_redis_1                  docker-entrypoint.sh redis ...   Up      6379/tcp

```

To check that our setup works, in one console run command to see and follow 
containers logs:
```shell
docker-compose logs -f datahandle-workers datasource-workers notification-workers default-queue
```
In other console we should connect in some container of our services, for example:
```shell
docker exec -it celery_experiments_default-queue_1 sh
# in container exec next
cd /opt/app/
python3
```
In python console we run few tasks:
```pycon
>>> from tasks import notify_user_in_slack, get_weather_today
>>> notify_user_in_slack.delay("Bob")
<AsyncResult: 7a933060-1a8c-4b45-bc2c-b78adb504518>
>>> get_weather_today.delay()
<AsyncResult: 439b5f00-862a-46fe-af86-1c16b80b8e6a>
```
And in first console we should see something like that:
```
notification-workers_1  | [2022-03-30 07:31:32,517: INFO/MainProcess] Received task: tasks.notification.slack.notify_user_in_slack[7a933060-1a8c-4b45-bc2c-b78adb504518]  
notification-workers_1  | 2022-03-30 07:31:32.517 | INFO     | tasks.notification.slack:notify_user_in_slack:16 - Start sending notification to slack for user <Bob>.
notification-workers_1  | 2022-03-30 07:31:36.221 | INFO     | tasks.notification.slack:notify_user_in_slack:20 - Task completed.
notification-workers_1  | [2022-03-30 07:31:36,225: INFO/ForkPoolWorker-8] Task tasks.notification.slack.notify_user_in_slack[7a933060-1a8c-4b45-bc2c-b78adb504518] succeeded in 3.7077495829435065s: None
datasource-workers_1    | [2022-03-30 07:33:06,285: INFO/MainProcess] Received task: tasks.datasource.weather.get_weather_today[439b5f00-862a-46fe-af86-1c16b80b8e6a]  
datasource-workers_1    | 2022-03-30 07:33:06.286 | INFO     | tasks.datasource.weather:get_weather_today:16 - Start receiving weather data.
datasource-workers_1    | 2022-03-30 07:33:06.286 | DEBUG    | libs.weather:get_weather:36 - Start getting weather for <today>.
datasource-workers_1    | 2022-03-30 07:33:06.286 | DEBUG    | libs.weather:_connect_to_weather_provider:9 - Connecting to weateher provider...
datasource-workers_1    | 2022-03-30 07:33:06.387 | DEBUG    | libs.weather:_connect_to_weather_provider:13 - Connection established.
datasource-workers_1    | 2022-03-30 07:33:06.387 | DEBUG    | libs.weather:_get_data:22 - Getting data...
datasource-workers_1    | 2022-03-30 07:33:08.389 | DEBUG    | libs.weather:_get_data:30 - Data received.
datasource-workers_1    | 2022-03-30 07:33:08.389 | INFO     | tasks.datasource.weather:get_weather_today:20 - Task completed
datasource-workers_1    | [2022-03-30 07:33:08,392: INFO/ForkPoolWorker-8] Task tasks.datasource.weather.get_weather_today[439b5f00-862a-46fe-af86-1c16b80b8e6a] succeeded in 2.106564264977351s: {'weather': 'rain', 'temperature': 0}
```
As we can see, _weather-task_ was executed by worker handles `datasource` queue in 
container `datasource-workers_1`, and _notification-task_ was executed by 
"notification" worker in container `notification-workers_1`.