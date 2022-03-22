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