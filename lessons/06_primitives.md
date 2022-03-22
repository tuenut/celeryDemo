#### Signatures

So, we can use signatures of tasks to pass tasks invocation to another process/application or as argument to another
function.

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

You can create signature with partial arguments and provide rest arguments after in place, like as currying function

```pycon
# incomplete partial: add(?, 2)
>>> s2 = add_request.s(2)

# resolves the partial: add(8, 2)
>>> res = s2.delay(8)
>>> res.get()
10
```

Here you added the argument 8 that was prepended to the existing argument 2 forming a complete signature of add(8, 2).

#### Groups

A group calls a list of tasks in parallel, and it returns a special result instance that lets you inspect the results as
a group, and retrieve the return values in order.

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

First group of tasks will be executed and then list of it results will pass 
to `xsum_request` callback.