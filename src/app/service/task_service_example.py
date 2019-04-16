"""
An example service created by Alex
"""
from time import sleep
from src.factory import make_celery

CELERY = make_celery()


def reverser(characters):
    """
    An example service function that reverses a string
    :param argument_1: string to reverse
    :return:
    """
    return characters[::-1]


@CELERY.task(name="tasks.reverse_string")
def long_running_task(characters):
    """ Just like `alex-reverser` but it takes 150 more seconds """
    sleep(150)
    return reverser(characters)
