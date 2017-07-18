#!/usr/bin/env python3

import os
import signal
import datetime
import time
import sys

try:
    import gi
except ImportError:
    raise ImportError("Please sudo apt install python3-gi")

from threading import Thread, Lock

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

gi.require_version('AppIndicator3', '0.1')
from gi.repository import AppIndicator3 as appindicator

from . import config
from . import menu
from . import taskwindow
from . import playme
import subprocess
import pickle
from pkg_resources import resource_filename


active_alarms = []
thread_list = []
tLock = Lock()

filepath = resource_filename(__name__, 'images/' + 'sinoamarelo.svg')


APPINDICATOR_ID = 'bzoing'

class MyBzoing:
    def __init__(self):
        self.task_list = []
        self.tasklist_id = -1
        self.task_window_open = False
        indicator = appindicator.Indicator.new(APPINDICATOR_ID,
                                               os.path.abspath(filepath),
                                               appindicator.IndicatorCategory.APPLICATION_STATUS)
        indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.my_menu = menu.BzoingMenu()
        indicator.set_menu(self.my_menu)
        # retrieve saved tasks from file
        try:
            with open('outfile.p', 'rb') as fp:
                config.list_of_alarms = pickle.load(fp)
            print("tasks loaded from file")
            # remove the pickle file
            os.remove('outfile.p')

        except IOError:
            print("No pending tasks or could't load task list file.")

        Gtk.main()

def sendmessage(message):
    subprocess.Popen(['notify-send', message])
    return

def new_alarm(task_id, name, num_seconds):
    seconds_passed = 0
    while seconds_passed < num_seconds:
        time.sleep(1)
        seconds_passed += 1
        if config.can_quit:
            return
        if config.stop[task_id]:
            return
    print("beep beep!!! it's time to do {} ".format(name))
    sendmessage("Its time for {}".format(name))
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
    # TODO load the postphoned alarms from file and put them on list_of_alarms
    while True:
        # get the new items in list_of_alarms
        # and start threads for them
        if len(config.list_of_alarms) > 0:

            # get alarm from list_of_alarms
            task = config.list_of_alarms.pop(0)
            task_id = task.task_id
            task_desc = task.get_task_desc()
            task_alarm = task.get_alarm()

            # if the alarm is today or tomorrow calculate delta
            today = datetime.datetime.now()
            if task_alarm.year == today.year \
                and task_alarm.month == today.month \
                and task_alarm.day == today.day or task_alarm.day == today.day + 1:
                print("it's today or tomorrow")
                # check the time left until alarm sounds today
                my_delta = (task_alarm - datetime.datetime.now()).total_seconds()
                print("Alarm will sound in {0} seconds".format(my_delta))

                # start thread for today alarm
                config.stop[task_id] = False
                thread_list.append(Thread(target=new_alarm, args=(task_id, task_desc, my_delta)))
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
        if (new_time - current_time).total_seconds() > 10:
            print("computer has been suspended")
            # stop current alarms
            for task in active_alarms:
                with tLock:
                    config.stop[task.task_id] = True
                    # reput stoped tasks on list_of_alarms
                    config.list_of_alarms.append(task)

        # detect if day has changed
        if new_time.day == current_time.day + 1:
            # put today and tomorrow events on the list_of_alarms
            for task in waiting_list[:]:
                if task.task_alarm.year == new_time.year\
                 and task.task_alarm.month == new_time.month\
                 and task.task_alarm.day == new_time.day or task.task_alarm.day == new_time.day + 1:
                    with tLock:
                        # put task on list_of_alarms
                        config.list_of_alarms.append(task)
                        # remove task from waiting_list
                        if task in waiting_list:
                            waiting_list.remove(task)




        # quit monitor
        if config.can_quit == True:
            # merge the active_alarms and the waiting_list
            tosave = active_alarms + waiting_list
            # save the merged tasks
            if len(tosave) > 0:
                with open('outfile.p', 'wb') as fp:
                    pickle.dump(tosave, fp)
                    print("Tasks have been saved")

            print("Goodbye!")
            break


def gui():
    app = MyBzoing()

def start():
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    for sig in [signal.SIGTERM, signal.SIGHUP, signal.SIGQUIT]:
        signal.signal(sig, handler)
    t1 = Thread(target=monitor)
    t2 = Thread(target=gui)
    t1.start()
    t2.start()

def handler(signum=None, frame=None):
    # set config.can_quit to True if system is halting
    config.can_quit = True
    # wait for a bit
    time.sleep(6)
    print("Wait done")
    sys.exit(0)

if __name__ == "__main__":
    start()
