# Celery demo project

That project demonstrating setup, use and development with celery step by step.

As broker we use redis. Due some purposes we use redis==3.2.0 for python.

Also, we use loguru for logging.

## Instructions


### First steps with Celery

1) To run redis in docker execute:
```shell
docker run -d --name celery_experiments.redis -p 127.0.0.1:6379:6379 redis:6.2-alpine
```
2) Create _app_ in `tasks.py`, which is _Celery_ instance, setup **redis** as _broker_ and
_result backend_.
3) Create functional task `add` in `tasks.py`.
4) Run celery worker:
```shell
celery -A tasks worker --loglevel=info
```
5) In another terminal run python interpreter and execute:
```pycon
>>> from tasks import add
>>> result = add.delay(4,4)
>>> result.get()
8
```
- 8 - is result which returned by task and stored in _result backend_. 
Because `delay()` runs task asynchronously, result may not accessible immediately 
after you run `delay()` but only after task completed. You can experiment with add
some delay in few seconds to your task before `return result`.
- The `ready()` method returns whether the task has finished processing or not:
```pycon
>>> result.ready()
False
```
- Also, if you don't enable _result backend_ you can't retrieve result from task 
in that way.


### Configuration

There is some ways to configure celery. You can read more in documentation.

We will use `celeryconfig.py`. So let's add some configuration in file and then 
refactor our `tasks.py`.


### Project tree

Ok, let's assume we have some big project (django project for example) where we 
should separate our tasks code from other parts of code.
- We create module `tasks` where we will store any code of our tasks.
- Create `tasks.celery` where place Celery _app_ instance.
- Now move our `add` task to module `tasks.math` and there we will store any 
math-type tasks which we will implement in our project.
- Let's write a few other tasks such as `sub`, `mul` and `divide`.

Now we can still run celery with command
```shell
celery -A tasks worker --loglevel=info
```
because celery looks the Celery app instance in next order:

> With --app=proj:
>    1. an attribute named proj.app, or
>    2. an attribute named proj.celery, or
>    3. any attribute in the module proj where the value is a Celery application, or
> 
> If none of these are found it’ll try a submodule named proj.celery:
>    4. an attribute named proj.celery.app, or
>    5. an attribute named proj.celery.celery, or
>    6. Any attribute in the module proj.celery where the value is a Celery application.
> 
> This scheme mimics the practices used in the documentation – that is, proj:app
> for a single contained module, and proj.celery:app for larger projects.
> -- <cite>Celery docs</cite>

#### Next step

Now let's decompose our logic for reusing due DRY principle.

Create module `libs.math` where we will store our payload functions. That 
functions we will call from task to solve user requests.

Add some log info to that functions, also change log messages level in 
tasks to INFO. Now we can see separately logs from different layers of our code.
INFO messages from tasks and DEBUG from payload functions.

By default, loguru uses stdout as default logs output, so we can see thats logs in 
celery process stdout. Also, because loguru uses different logging mechanism than 
python `logging`, celery logger (which uses `logging`) can't separate loguru output.
So, that is not a problem, just a note. But if we used python `logging` module
we can say to celery which log levels we want to see in stdout with 
`--loglevel=debug` for example.