import logging
from time import sleep

from nrt_time_utils.time_utils import TimeUtil, MINUTE_MS

from nrt_threads_utils.threads_pool_manager.enums import QueuePlacementEnum
from nrt_threads_utils.threads_pool_manager.tasks import ThreadTask
from nrt_threads_utils.threads_pool_manager.threads_pool_manager import \
    ThreadsPoolManager
from tests.threads_pool_manager.threads_pool_manager_test_base import \
    SleepSecPriorityThreadBase


class Sleep3600SecPriority1Thread(SleepSecPriorityThreadBase):

    def __init__(self):
        super().__init__(60 * 60, 1)


class Sleep1200SecPriority2Thread(SleepSecPriorityThreadBase):

    def __init__(self):
        super().__init__(20 * 60, 2)


EXECUTORS_POOL_SIZE = 30000

THREADS_AMOUNT_1 = 200000
THREADS_AMOUNT_2 = 2000


def test_threads_pool_manager_strict_priority_performance():

    threads_pool_manager = ThreadsPoolManager(executors_pool_size=EXECUTORS_POOL_SIZE)
    threads_pool_manager.max_executors_extension_pool_size = 100

    try:
        logging.info('Starting threads pool manager')

        threads_pool_manager.start()

        for i in range(THREADS_AMOUNT_1):
            t_1 = Sleep3600SecPriority1Thread()
            t_2 = Sleep1200SecPriority2Thread()

            task_id_1 = f'task_id_1_{i}'
            task_id_2 = f'task_id_2_{i}'

            __print_adding_tasks_id(task_id_1, task_id_2, i)

            threads_pool_manager.add_task(
                ThreadTask(t_1), task_id=task_id_1, priority=1)
            threads_pool_manager.add_task(
                ThreadTask(t_2), task_id=task_id_2, priority=2)

            __verify_in_adding_tasks_loop(task_id_1, task_id_2, threads_pool_manager)

        sleep(10 * 60)

        for i in range(THREADS_AMOUNT_2):
            t_1 = Sleep3600SecPriority1Thread()
            t_2 = Sleep1200SecPriority2Thread()

            task_id_1 = f'task_id_2_1_{i}'
            task_id_2 = f'task_id_2_2_{i}'

            __print_adding_tasks_id(task_id_1, task_id_2, i)

            threads_pool_manager.add_task(
                ThreadTask(t_1), task_id=task_id_1, priority=1)
            threads_pool_manager.add_task(
                ThreadTask(t_2), task_id=task_id_2, priority=2)

            __verify_in_adding_tasks_loop(task_id_1, task_id_2, threads_pool_manager)

        timeout_ms = 10 * MINUTE_MS

        __wait_and_verify_no_active_tasks(timeout_ms, threads_pool_manager)
    finally:
        logging.info('Shutting down threads pool manager')
        threads_pool_manager.shutdown()
        logging.info('Joining threads pool manager')
        threads_pool_manager.join()
        logging.info('Threads pool manager joined')


def test_threads_pool_manager_avoid_starvation_priority_performance():

    threads_pool_manager = ThreadsPoolManager(executors_pool_size=EXECUTORS_POOL_SIZE)
    threads_pool_manager.max_executors_extension_pool_size = 100
    threads_pool_manager.avoid_starvation_amount = 100

    try:
        threads_pool_manager.start()

        for i in range(THREADS_AMOUNT_1):
            t_1 = Sleep3600SecPriority1Thread()
            t_2 = Sleep1200SecPriority2Thread()

            task_id_1 = f'task_id_1_{i}'
            task_id_2 = f'task_id_2_{i}'

            __print_adding_tasks_id(task_id_1, task_id_2, i)

            threads_pool_manager.add_task(
                ThreadTask(t_1),
                task_id=task_id_1,
                priority=1,
                queue_placement=QueuePlacementEnum.AVOID_STARVATION_PRIORITY)
            threads_pool_manager.add_task(
                ThreadTask(t_2),
                task_id=task_id_2,
                priority=2,
                queue_placement=QueuePlacementEnum.AVOID_STARVATION_PRIORITY)

            __verify_in_adding_tasks_loop(task_id_1, task_id_2, threads_pool_manager)

        sleep(10 * 60)

        for i in range(THREADS_AMOUNT_2):
            t_1 = Sleep3600SecPriority1Thread()
            t_2 = Sleep1200SecPriority2Thread()

            task_id_1 = f'task_id_2_1_{i}'
            task_id_2 = f'task_id_2_2_{i}'

            __print_adding_tasks_id(task_id_1, task_id_2, i)

            threads_pool_manager.add_task(
                ThreadTask(t_1),
                task_id=task_id_1,
                priority=1)
            threads_pool_manager.add_task(
                ThreadTask(t_2),
                task_id=task_id_2,
                priority=2,
                queue_placement=QueuePlacementEnum.AVOID_STARVATION_PRIORITY)

            __verify_in_adding_tasks_loop(task_id_1, task_id_2, threads_pool_manager)

        timeout_ms = 10 * MINUTE_MS

        __wait_and_verify_no_active_tasks(timeout_ms, threads_pool_manager)
    finally:
        logging.info('Shutting down threads pool manager')
        threads_pool_manager.shutdown()
        logging.info('Joining threads pool manager')
        threads_pool_manager.join()
        logging.info('Threads pool manager joined')


def __verify_in_adding_tasks_loop(
        task_id_1: str, task_id_2: str, threads_pool_manager:  ThreadsPoolManager):

    assert threads_pool_manager.queue_size >= 0
    assert threads_pool_manager.get_task(task_id=task_id_1), \
        f'{task_id_1} not found'
    assert threads_pool_manager.get_task(task_id=task_id_2), \
        f'{task_id_2} not found'
    assert threads_pool_manager.is_task_exists(task_id=task_id_1)
    assert threads_pool_manager.is_task_exists(task_id=task_id_2)
    assert threads_pool_manager.queue is not None
    assert threads_pool_manager.executors_extension_pool_size >= 0
    assert threads_pool_manager.finished_tasks is not None
    assert threads_pool_manager.metrics is not None
    assert threads_pool_manager.active_tasks_amount >= 0


def __wait_and_verify_no_active_tasks(
        timeout_ms: int, threads_pool_manager:  ThreadsPoolManager):

    logging.info('Waiting and verifying no active tasks')

    is_finished = False

    start_time_ms = TimeUtil.get_current_date_ms()

    while not TimeUtil.is_timeout_ms(start_time_ms, timeout_ms) and not is_finished:
        if threads_pool_manager.active_tasks_amount == 0:
            is_finished = True

        sleep(10)

    logging.info(f'Queue size: {threads_pool_manager.queue_size}')
    logging.info(f'Active tasks amount: {threads_pool_manager.active_tasks_amount}')

    assert is_finished
    assert threads_pool_manager.queue_size == 0


def __print_adding_tasks_id(task_id_1: str, task_id_2: str, i: int):
    if i % 1000 == 0:
        logging.info(f'Adding tasks: {task_id_1}, {task_id_2}')
    else:
        logging.debug(f'Adding tasks: {task_id_1}, {task_id_2}')
