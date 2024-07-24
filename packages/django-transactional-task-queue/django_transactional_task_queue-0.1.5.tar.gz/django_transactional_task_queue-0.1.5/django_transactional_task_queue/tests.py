from unittest import TestCase

from django_transactional_task_queue.celery import shared_task
from django_transactional_task_queue.models import Task
from django.db import transaction


@shared_task
def dummy(*args, **kwargs):
    pass


class PersonTestCase(TestCase):
    def test_dummy(self):
        dummy.delay(1,2,c=3,d=4)

    def test_exec(self):
        for x in range(1_000):
            dummy.delay(x=x)

        import time
        start = time.time()

        n = 0
        while True:
            task = Task.next_task()
            if not task:
                break
            else:
                self._execute_one(task)
                n += 1
        end = time.time()

        print(end-start)
        print(n)
        print(n/(end-start))

    def _execute_one(self, task):
        with transaction.atomic():
            args = [str(arg) for arg in task.args]
            args += [str(key) + "=" + str(value) for key, value in task.kwargs.items()]
            task.lock()

            try:
                task.execute()

                task.delete()
            except Exception as exc:
                task.fail()
        
