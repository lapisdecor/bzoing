#!/usr/bin/env python3

from bzoing.tasks import Bzoinq, Monitor
import time

def start():
    # start the tasklist (Bzoinq)
    my_tasklist = Bzoinq()

    # start the Monitor
    my_monitor = Monitor(my_tasklist)
    my_monitor.start()

    # add a task
    my_tasklist.create_task()

    # wait a bit and stop the monitor
    time.sleep(5)
    my_monitor.stop() 


if __name__ == "__main__":
    start()
