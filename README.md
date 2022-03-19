That project demonstrating setup, use and development with celery step by step.

As broker we use redis. In some purposes we use redis==3.2.0 for python.

Also use loguru for logging.

## Instructions
### Fisrst steps with Celery

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
- Also if you don't enable _result backend_ you can't retrieve result from task 
in that way.

### Configuration
There is some ways to configure celery. You can read more in documentation.

We will use `celeryconfig.py`. So let's add some configuration in file and then 
refactor our `tasks.py`.