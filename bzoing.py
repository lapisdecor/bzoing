#!/usr/bin/env python3

import os
import signal
import gi
import datetime

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

gi.require_version('AppIndicator3', '0.1')
from gi.repository import AppIndicator3 as appindicator

import menu

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
        my_menu = menu.BzoingMenu()
        indicator.set_menu(my_menu)
        # TODO retrieve saved tasks from file
        Gtk.main()

def main():
    app = MyBzoing()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
