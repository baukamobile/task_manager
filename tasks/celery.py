from celery import Celery

app = Celery(
    'tasks',
    broker='redis://127.0.0.1:6379/0',
    backend='redis://127.0.0.1:6379/0'
)

app.conf.update(
    task_routes={
        'tasks.add': {'queue': 'default'}
    }
)

@app.task
def add(x, y):
    return x + y
