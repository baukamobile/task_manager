from celery import Celery
app = Celery(
    'proj',
    broker='amqp://'
    backend='rpc://',
    include=['proj.tasks']
)
app.cond.update(
    result_expires=3600,
)
if __name__ == '__main__':
    app.start()