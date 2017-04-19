"""
test_bzoing
----------------------------------
Tests for `bzoing` module.
"""

import nose


from bzoing import bzoing, tasks

import datetime

def test_task():
    a = tasks.Task(1, "lalala")
    assert a.task_id == 1
    assert a.task_desc == "lalala"
    assert a.alarm_date == None

def run_bzoing():
    bzoing.main()
    print("bzoing has run")
    assert 1 == 1
