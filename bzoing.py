#!/usr/bin/env python3

import os
import signal
import datetime
import time
import gi
from threading import Thread, Lock

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

gi.require_version('AppIndicator3', '0.1')
from gi.repository import AppIndicator3 as appindicator

import config
import menu


list_of_alarms = []
active_alarms = []
thread_list = []
tLock = Lock()


APPINDICATOR_ID = 'bzoing'

class MyBzoing:
    def __init__(self):
        self.task_list = []
        self.tasklist_id = -1
        self.task_window_open = False
        indicator = appindicator.Indicator.new(APPINDICATOR_ID,
                                               os.path.abspath('sinoamarelo.svg'),
                                               appindicator.IndicatorCategory.APPLICATION_STATUS)
        indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.my_menu = menu.BzoingMenu()
        indicator.set_menu(self.my_menu)
        # TODO retrieve saved tasks from file
        Gtk.main()

def new_alarm(name, num_seconds):
    time.sleep(num_seconds)
    print("beep beep!!! {} is over".format(name))
    # remove alarm from active_alarms
    with tLock:
        active_alarms.pop()

def monitor():
    """monitors the list_of_alarms"""
    n = 0
    while True:
        # get the new items in list_of_alarms
        # and start threads for them
        if len(list_of_alarms) > 0:
            # start thread for alarm
            thread_list.append(Thread(target=new_alarm, args=(list_of_alarms[0])))
            thread_list[-1].start()
            # remove alarm from list_of_alarms and put it on active_alarms
            with tLock:
                a = list_of_alarms.pop(0)
                active_alarms.append(a)
            print("alarm {} was set to active".format(a))
            print(list_of_alarms)

        # check if computer was suspended
        current_time = datetime.datetime.now()
        time.sleep(1)
        new_time = datetime.datetime.now()
        if (new_time - current_time).total_seconds() > 5:
            print("computer has been suspended")

        # quit monitor
        if config.can_quit == True:
            print("Goodbye!")
            break


def gui():
    app = MyBzoing()

def main():
    t1 = Thread(target=monitor)
    t2 = Thread(target=gui)
    t1.start()
    t2.start()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
