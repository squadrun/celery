from time import sleep

import celery.utils
from celery import Task, shared_task, signature
from celery.canvas import Signature
from t.integration.tasks import *  # noqa
from t.integration.tasks import replaced_with_me


@shared_task
def noop(*args, **kwargs) -> None:
    return celery.utils.noop(*args, **kwargs)


@shared_task
def long_running_task(seconds: float = 1, verbose: bool = False) -> bool:
    from celery import current_task
    from celery.utils.log import get_task_logger

    logger = get_task_logger(current_task.name)

    logger.info('Starting long running task')

    for i in range(0, int(seconds)):
        sleep(1)
        if verbose:
            logger.info(f'Sleeping: {i}')

    logger.info('Finished long running task')

    return True


@shared_task(bind=True)
def replace_with_task(self: Task, replace_with: Signature = None):
    if replace_with is None:
        replace_with = replaced_with_me.s()
    return self.replace(signature(replace_with))