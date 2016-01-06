#!/usr/bin/env python3

import os
import signal
from gi.repository import Gtk
from gi.repository import AppIndicator3 as appindicator

import tasks

APPINDICATOR_ID = 'bzoing'


class MyBzoing:
    def __init__(self):
        self.task_list = []
        indicator = appindicator.Indicator.new(APPINDICATOR_ID,
                                           os.path.abspath('sinoamarelo.svg'),
                                           appindicator.IndicatorCategory.APPLICATION_STATUS)
        indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        indicator.set_menu(self.build_menu())
        Gtk.main()

    def build_menu(self):
        """
        Builds all the menus
        :rtype: object
        """
        menu = Gtk.Menu()
        item_new_task = Gtk.MenuItem('New task')
        item_new_task.connect('activate', self.new_task)
        menu.append(item_new_task)

        item_see_tasks = Gtk.MenuItem('See tasks')
        item_see_tasks.connect('activate', self.see_tasks)
        menu.append(item_see_tasks)

        item_separator = Gtk.SeparatorMenuItem()
        menu.append(item_separator)

        item_stop_alarms = Gtk.MenuItem('Stop Alarms')
        item_stop_alarms.connect('activate', self.stop_alarms)
        menu.append(item_stop_alarms)

        item_quit = Gtk.MenuItem('Quit')
        item_quit.connect('activate', self.quit)
        menu.append(item_quit)

        menu.show_all()
        return menu

    def new_task(self, _):
        window_task = Gtk.Window(title='Create Task')
        window_task.connect('destroy', self.quit_window)

        vbox = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)
        hbox = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 6)

        task_label = Gtk.Label()
        task_label.set_text('Task: ')
        hbox.pack_start(task_label, False, False, 2)

        task_field = Gtk.Entry()
        hbox.pack_start(task_field, False, False, 2)

        vbox.pack_start(hbox, False, False, 6)

        button_alarm = Gtk.Button()
        button_alarm.set_label("Alarm")
        button_alarm.connect("clicked", self.on_alarm_clicked)
        vbox.pack_start(button_alarm, False, False, 2)

        button_ok = Gtk.Button()
        button_ok.set_label("Ok")
        passvalues = [window_task, task_field]
        button_ok.connect("clicked", self.on_task_ok, passvalues)
        vbox.pack_start(button_ok, 0, 0, 2)

        window_task.add(vbox)
        window_task.show_all()

        return window_task

    def see_tasks(self, _):
        """
        Shows a window with all the tasks and alarms
        :param _:
        :return:
        """
        window = Gtk.Window(title="List of tasks")
        box = Gtk.Box(spacing=6)
        box.set_orientation(Gtk.Orientation.VERTICAL)
        window.add(box)

        list_of_gtk_labels = []

        for each_task in self.task_list:
            # creates one Gtk.Label for each item in the list_of_tasks
            list_of_gtk_labels.append(Gtk.Label(each_task.get_task_desc()))

        for label in list_of_gtk_labels:
            box.pack_start(label)

        window.show_all()



    def stop_alarms(self, _):
        """
        Stops all playing alarms
        :param _:
        :return:
        """
        pass

    def on_alarm_clicked(self, _):
        """
        Shows a window to define the alarm
        :param _:
        :return: datetime object
        """
        window_alarm = Gtk.Window(title="Define alarm")
        # TODO show calendar and time fields and start alarm (implement alarm using threading?)
        alarm = 0
        window_alarm.show_all()
        return alarm

    def on_task_ok(self, widget, passvalues):
        print(passvalues[1].get_text())
        # TODO implement create task from task data
        # add_task(data)
        # TODO update task list window
        passvalues[0].destroy()

    def quit_window(self,window):
        window.destroy()

    def quit(self, widget):
        Gtk.main_quit()


def main():
    app = MyBzoing()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
