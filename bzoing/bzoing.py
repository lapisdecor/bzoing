#!/usr/bin/env python3

from bzoing.tasks import Bzoinq, Monitor
import time

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

from pkg_resources import resource_filename
from . import share
import signal
import sys

gi.require_version('AppIndicator3', '0.1')
from gi.repository import AppIndicator3 as appindicator

import os
import pickle
from . import setalarmwindow
from . import seetasks


filepath = resource_filename(__name__, 'images/' + "sinoamarelo.svg")
APPINDICATOR_ID = 'bzoing'


class BzoingMenu(Gtk.Menu):
    def __init__(self):
        Gtk.Menu.__init__(self)

        item_new_task = Gtk.MenuItem('New task')
        item_new_task.connect('activate', self.new_task)
        self.append(item_new_task)

        item_see_tasks = Gtk.MenuItem('See tasks')
        item_see_tasks.connect('activate', self.see_tasks)
        self.append(item_see_tasks)

        item_see_past_tasks = Gtk.MenuItem("See past tasks")
        item_see_past_tasks.connect('activate', self.see_past_tasks)
        self.append(item_see_past_tasks)

        item_separator = Gtk.SeparatorMenuItem()
        self.append(item_separator)

        item_quit = Gtk.MenuItem('Quit')
        item_quit.connect('activate', self.quit)
        self.append(item_quit)

        self.show_all()

    def new_task(self, widget):
        """
        Creates new task window
        """
        alarm_window = setalarmwindow.SetAlarmWindow(self)


    def see_tasks(self, widget):
        """
        Shows a window with all the tasks and alarms
        """
        see_tasks_window = seetasks.SeeTasks(self)

    def see_past_tasks(self, widget):
        """
        Shows a window with all the done tasks
        """
        see_past_window = seetasks.SeePastTasks(self)


    def quit(self, widget):
        Gtk.main_quit()


class Gui:
    def __init__(self):
        self.indicator = appindicator.Indicator.new(APPINDICATOR_ID,
                                           os.path.abspath(filepath),
                                           appindicator.IndicatorCategory.APPLICATION_STATUS)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.my_menu = BzoingMenu()
        self.indicator.set_menu(self.my_menu)


# def handler(signum = None, frame = None):
#     """Handles computer shutdown"""
#     Gtk.main_quit()
#     share.tasklist.save_tasks()
#     share.my_monitor.stop()
#     time.sleep(1)
#     print("Tasks have been saved")
#     sys.exit(0)


def start():
    # catch shutdown
    # for sig in [signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGQUIT]:
    #     signal.signal(sig, handler)


    # from https://stackoverflow.com/questions/26388088/python-gtk-signal-handler-not-working/
    def InitSignal(gui):
        def signal_action(signal):
            if signal is 1:
                print("Caught signal SIGHUP(1)")
            elif signal is 2:
                print("Caught signal SIGINT(2)")
            elif signal is 15:
                print("Caught signal SIGTERM(15)")
            #gui.cleanup()
            #gui.quit(None)
            #share.tasklist.save_tasks()
            #share.my_monitor.stop()
            Gtk.main_quit()

        def idle_handler(*args):
            print("Python signal handler activated.")
            GLib.idle_add(signal_action, priority=GLib.PRIORITY_HIGH)

        def handler(*args):
            print("GLib signal handler activated.")
            signal_action(args[0])

        def install_glib_handler(sig):
            unix_signal_add = None

            if hasattr(GLib, "unix_signal_add"):
                unix_signal_add = GLib.unix_signal_add
            elif hasattr(GLib, "unix_signal_add_full"):
                unix_signal_add = GLib.unix_signal_add_full

            if unix_signal_add:
                print("Register GLib signal handler: %r" % sig)
                unix_signal_add(GLib.PRIORITY_HIGH, sig, handler, sig)
            else:
                print("Can't install GLib signal handler, too old gi.")

        SIGS = [getattr(signal, s, None) for s in "SIGINT SIGTERM SIGHUP".split()]
        for sig in filter(None, SIGS):
            print("Register Python signal handler: %r" % sig)
            signal.signal(sig, idle_handler)
            GLib.idle_add(install_glib_handler, sig, priority=GLib.PRIORITY_HIGH)


    # start the tasklist (Bzoinq)
    share.tasklist = Bzoinq()

    # start the Monitor
    share.my_monitor = Monitor(share.tasklist)
    share.my_monitor.start()

    # start the gui and pass tasklist to the gui so we can create tasks
    # from the gui
    gui = Gui()
    InitSignal(gui)
    Gtk.main()

    # save tasks
    share.tasklist.save_tasks()

    # stop the monitor
    share.my_monitor.stop()

    # goodbye message
    print("Bye!")


if __name__ == "__main__":
    start()
