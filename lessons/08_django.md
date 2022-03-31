## Using celery tasks with Django

There is some difference when we are using celery with django. We need 
`celery.py` in django project dir, where we should instantiate app:
```
- proj/
  - manage.py
  - proj/
    - __init__.py
    - **celery.py**
    - settings.py
    - urls.py
```
And then import app in `proj/proj/__init__.py`. This ensures that the app is 
loaded when Django starts so that the @shared_task decorator (mentioned later) 
will use it.

So, let's install django==3.2 and do steps above.
```shell
cd src/
django-admin startproject celery_demo
cd celery_demo/
```

### Create django apps

Let's implement three django apps according to our previous use cases: 
receiving weather, handle user content(images), send notifications to users and 
our math-tasks examples.
```shell
python3 manage.py startapp weather
python3 manage.py startapp pictures
python3 manage.py startapp notification
python3 manage.py startapp math_demo
```

### Create tasks
Now let's move our code from standalone demo to django demo...

### Create views
Next we write some views and templates to create UI and visualize results for 
math_demo.

Run django dev server and in other console run celery worker. 
Make sure the redis server is running on 127.0.0.1.
```shell
python3 manage.py runserver 127.0.0.1:8000
celery -A celery_demo worker --loglevel=info
```
> In that case we run celery worker for default queue. Due to our math tasks 
> has no routing, it will be handled by that worker.

Now open http://127.0.0.1:8000/math/ in your browser and try to perform some 
requests on page. You will get results of operations after you click on button
`Calculate`. 

Next stop celery worker and try again. After one second waiting you will get 
message on page `Task still executing...` and result is None. That happens 
because task was putted in queue, but no worker executed it. Now if you run 
celery worker again, you will see in console, that worker found a task and 
executed it. Update your result page and you get task result.

On next step we run our app with docker-compose, and we will be testing other 
tasks, routed to separated queues.
