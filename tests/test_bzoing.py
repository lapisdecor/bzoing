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



if __name__ == '__main__':
    unittest.main()
