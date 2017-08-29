#!/usr/bin/env python3

from bzoing.tasks import Bzoinq, Monitor
import time
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from pkg_resources import resource_filename
from . import share
import signal
import sys


filepath = resource_filename(__name__, 'images/' + "sinoamarelo.svg")


class Gui(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_icon_from_file(filepath)
        self.connect('destroy', self.quit_window)
        self.show_all()

    def quit_window(self, window):
        """Quits the window"""
        self.destroy()
        Gtk.main_quit()


def handler(signum = None, frame = None):
    """Handles computer shutdown"""
    if len(share.tasklist.get_task_list()) > 0:
        with open('outfile.p', 'wb') as fp:
                    pickle.dump(share.tasklist.get_task_list(), fp)
    print("Tasks have been saved")
    sys.exit(0)


def start():
    # catch shutdown
    for sig in [signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGQUIT]:
        signal.signal(sig, handler)


    # start the tasklist (Bzoinq)
    share.tasklist = Bzoinq()

    # start the Monitor
    my_monitor = Monitor(share.tasklist)
    my_monitor.start()

    # start the gui and pass tasklist to the gui so we can create tasks
    # from the gui
    gui = Gui()
    Gtk.main()

    # stop the monitor
    my_monitor.stop()

    # goodbye message
    print("Bye!")


if __name__ == "__main__":
    start()
