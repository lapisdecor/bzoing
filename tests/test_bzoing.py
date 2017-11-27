"""
test_bzoing
----------------------------------
Tests for `bzoing` module.
"""

import unittest

from bzoing.tasks import Bzoinq, Monitor

import time


class TestTasksAndMonitor(unittest.TestCase):

    def test_creating_task(self):
        a = Bzoinq()
        a.create_task()
        self.assertTrue(len(a.task_list) == 1)

    def test_delete_task(self):
        a = Bzoinq()
        a.create_task()
        the_id = a.task_list[0].id
        a.remove_task(the_id)
        self.assertTrue(len(a.task_list) == 0)

    def test_monitor(self):
        import datetime
        a = Bzoinq()
        b = Monitor(a)
        b.start()
        first_time = datetime.datetime.now() + datetime.timedelta(seconds=10)
        a.create_task("My test task", alarm=first_time)
        # sleep a bit to see if alarm works
        time.sleep(15)
        # check the if task was removed from task list
        self.assertTrue(len(a.task_list) == 0)
        # kill Monitor
        b.stop()


if __name__ == '__main__':
    unittest.main()
