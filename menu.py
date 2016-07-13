import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import taskwindow
import tasklistwindow
#import tasks

class BzoingMenu(Gtk.Menu):
    def __init__(self):
        Gtk.Menu.__init__(self)
        self.task_list = []
        self.task_id = -1

        item_new_task = Gtk.MenuItem('New task')
        item_new_task.connect('activate', self.new_task)
        self.append(item_new_task)

        item_see_tasks = Gtk.MenuItem('See tasks')
        item_see_tasks.connect('activate', self.see_tasks)
        self.append(item_see_tasks)

        item_separator = Gtk.SeparatorMenuItem()
        self.append(item_separator)

        item_stop_alarms = Gtk.MenuItem('Stop Alarms')
        item_stop_alarms.connect('activate', self.stop_alarms)
        self.append(item_stop_alarms)

        item_quit = Gtk.MenuItem('Quit')
        item_quit.connect('activate', self.quit)
        self.append(item_quit)

        self.show_all()

    def new_task(self, widget):
        """
        Creates new task window
        """
        my_task_window = taskwindow.TaskWindow(self)

    def see_tasks(self, widget):
        """
        Shows a window with all the tasks and alarms
        """
        my_task_list = tasklistwindow.TaskListWindow(self.task_list)

    def stop_alarms(self, widget):
        """
        Stops all playing alarms
        """
        pass

    def quit(self, widget):
        # TODO save tasks to file
        Gtk.main_quit()
