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
