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
> 
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

### Canvas: Designing Work-flows
#### Signatures

So, we can use signatures of tasks to pass tasks invocation to  another 
process/application or as argument to another function.

> A signature wraps the arguments and execution options of a single task 
> invocation in such a way that it can be passed to functions or even serialized 
> and sent across the wire.
> 
> -- <cite>Celery docs</cite>

```pycon
>>> add_request.signature((2, 2), countdown=10)
tasks.add_request(2, 2)

# There’s also a shortcut using star arguments:
>>> add.s(2, 2)
tasks.add_request(2, 2)
```

You can create signature with partial arguments and provide rest arguments after
in place, like as currying function

```pycon
# incomplete partial: add(?, 2)
>>> s2 = add_request.s(2)

# resolves the partial: add(8, 2)
>>> res = s2.delay(8)
>>> res.get()
10
```
Here you added the argument 8 that was prepended to the existing argument 2 
forming a complete signature of add(8, 2).

#### Groups

A group calls a list of tasks in parallel, and it returns a special result 
instance that lets you inspect the results as a group, and retrieve the return 
values in order.

```pycon
>>> from celery import group
>>> from tasks import add_request

>>> group(add_request.s(i, i) for i in range(10))().get()
[0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

# Partial group
>>> g = group(add_request.s(i) for i in range(10))
>>> g(10).get()
[10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
```

#### Chains

Tasks can be linked together so that after one task returns the other is called:

```pycon
>>> from celery import chain
>>> from tasks import add_request, mul_request

# (4 + 4) * 8
>>> chain(add_request.s(4, 4) | mul_request.s(8))().get()
64

# or a partial chain:
# (? + 4) * 8
>>> g = chain(add_request.s(4) | mul_request.s(8))
>>> g(4).get()

# Chains can also be written like this:
>>> (add_request.s(4, 4) | mul_request.s(8))().get()
64
```

#### Chords

A chord is a group with a callback(which will apply to result of group):

```pycon
>>> from celery import chord
>>> from tasks import add_request, xsum_request

>>> tasks_chord = chord((add_request.s(i, i) for i in range(10)), xsum_request.s())
>>> tasks_chord.delay().get(timeout=1)
90
```

Firstlty group of tasks will be executed and then list of it results will pass 
to `xsum_request` callback.