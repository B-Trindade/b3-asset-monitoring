from celery import shared_task


@shared_task
def sharedtask_test():
    print('Celery Shared task has been called.')
    return
