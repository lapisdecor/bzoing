#!/usr/bin/env python3

import os
import subprocess
import sys

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gio

from . import share
from .tasks import Bzoinq, Monitor
from . import setalarmwindow
from . import seetasks


APPLICATION_ID = 'com.gatochalupa.bzoing'


class BzoingApplication(Gtk.Application):
    def __init__(self):
        super().__init__(application_id=APPLICATION_ID)
        self._tray = None

    def do_startup(self):
        Gtk.Application.do_startup(self)

        new_task = Gio.SimpleAction(name='new-task')
        new_task.connect('activate', self.new_task)
        self.add_action(new_task)

        see_tasks = Gio.SimpleAction(name='see-tasks')
        see_tasks.connect('activate', self.see_tasks)
        self.add_action(see_tasks)

        see_past_tasks = Gio.SimpleAction(name='see-past-tasks')
        see_past_tasks.connect('activate', self.see_past_tasks)
        self.add_action(see_past_tasks)

        quit_action = Gio.SimpleAction(name='quit')
        quit_action.connect('activate', self.quit_app)
        self.add_action(quit_action)

        self.hold()

    def do_activate(self):
        if share.tasklist is None:
            share.tasklist = Bzoinq()
            self._monitor = Monitor(share.tasklist)
            self._monitor.start()
            self._start_tray()

    def do_shutdown(self):
        Gtk.Application.do_shutdown(self)
        if share.tasklist is not None:
            share.tasklist.save_tasks()
        if getattr(self, '_monitor', None) is not None:
            self._monitor.stop()
        if self._tray is not None:
            try:
                self._tray.terminate()
                self._tray.wait(timeout=5)
            except Exception:
                pass

    def _start_tray(self):
        tray_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tray.py')
        self._tray = subprocess.Popen([sys.executable, tray_script])

    def new_task(self, action, parameter):
        window = setalarmwindow.SetAlarmWindow(self)
        window.present()

    def see_tasks(self, action, parameter):
        window = seetasks.SeeTasks(self)
        window.present()

    def see_past_tasks(self, action, parameter):
        window = seetasks.SeePastTasks(self)
        window.present()

    def quit_app(self, action, parameter):
        self.quit()


def start():
    app = BzoingApplication()
    app.run(sys.argv)
    print("Bye!")


if __name__ == "__main__":
    start()