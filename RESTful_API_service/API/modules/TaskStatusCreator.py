from celery.result import AsyncResult


def create_task_status(task_id, task_name):
    info = dict()
    res = AsyncResult(task_id, task_name=task_name)

    if res.state == 'PENDING':
        return False

    info['status'] = res.state
    info['status_info'] = res.info

    return info
