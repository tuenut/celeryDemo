### Decomposing

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