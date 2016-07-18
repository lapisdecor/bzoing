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
import taskwindow
import playme

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
    print("beep beep!!! it's time to do {} ".format(name))
    # remove alarm from active_alarms
    with tLock:
        active_alarms.pop()
    # play sound
    my_sound = playme.Playme()
    my_sound.play()

def monitor():
    """monitors the list_of_alarms"""
    n = 0
    waiting_list = []
    today = datetime.datetime.now()
    # TODO load the postphoned alarms from file and put them on list_of_alarms
    # TODO if day has changed get from the waiting_list and put on the list_of_alarms
    while True:
        # get the new items in list_of_alarms
        # and start threads for them
        if len(config.list_of_alarms) > 0:

            # get alarm from list_of_alarms
            task = config.list_of_alarms.pop(0)
            task_desc = task[0]
            task_alarm = task[1]

            # if the alarm is today calculate delta
            if task_alarm.year == today.year \
                and task_alarm.month == today.month \
                and task_alarm.day == today.day:
                print("it's today")
                # check the time left until alarm sounds today
                my_delta = (task_alarm - datetime.datetime.now()).total_seconds()
                print("Alarm will sound in {0} seconds".format(my_delta))

                # start thread for today alarm
                thread_list.append(Thread(target=new_alarm, args=(task_desc, my_delta)))
                thread_list[-1].start()
                #print("thread_list = " , thread_list)

                #  put it on active_alarms
                with tLock:
                    active_alarms.append(task)

            # if the alarm is not today, postphone to a waiting list
            else:
                waiting_list.append(task)
                print("Current tasks on waiting_list", waiting_list)


        # check if computer was suspended
        current_time = datetime.datetime.now()
        time.sleep(1)
        new_time = datetime.datetime.now()
        if (new_time - current_time).total_seconds() > 5:
            print("computer has been suspended")
            # TODO check due alarms
            # TODO put stop active alarms and reput them on list_of_alarms

        # quit monitor
        if config.can_quit == True:
            # TODO save the active_alarms
            # TODO save the waiting_list
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
