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

Now let's move our code from standalone demo to django demo...